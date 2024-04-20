import os
from sys import exit
from time import sleep
import requests
import config

regionMap = {
    'NA': 'https://cdn.contentstack.io/',
    'na': 'https://cdn.contentstack.io/',
    'EU': 'https://eu-cdn.contentstack.com/',
    'eu': 'https://eu-cdn.contentstack.com/'
}

try:
    region = regionMap[os.getenv('CS_REGION', None)]
except KeyError:
    config.logging.warning('{}No Region defined - Defaulting to North America.{}'.format(config.YELLOW, config.END))
    region = 'https://cdn.contentstack.io/'

apiKey = os.getenv('CS_APIKEY', None)
if not apiKey:
    config.logging.critical('{}Stack API Key Missing as an Environment Variable. Exiting Script.{}'.format(config.RED, config.END))
    exit()

deliveryToken = os.getenv('CS_DELIVERYTOKEN', None)
if not deliveryToken:
    config.logging.critical('{}Delivery Token Missing as an Environment Variable. Exiting Script.{}'.format(config.RED, config.END))
    exit()

deliveryTokenHeader = {
    'access_token': deliveryToken,
    'api_key': apiKey,
    'Content-Type': 'application/json'
}

def logUrl(url):
    '''
    Logging out for debug purposes the constructed URL for any function
    '''
    config.logging.debug('-------')
    config.logging.debug('The CDA URL:')
    config.logging.debug(url)
    config.logging.debug('-------')

def iterateURL(url, skip=0):
    return url + '&skip={}'.format(skip)

def typicalGetIterate(url, dictKey='entries', environment=None, contentType=None, locale=None):
    '''
    Re-usable function to GET objects that might have more than 100 items in it
    '''
    result = []
    skip = 0
    count = 1 # Just making sure we check at least once. Setting the real count value in while loop
    if environment:
        url = url + '&environment={}'.format(environment)
    logUrl(url)
    originalURL = url
    while skip <= count:
        url = iterateURL(originalURL, skip)
        logUrl(url)
        res = requests.get(url, headers=deliveryTokenHeader)
        if res.status_code in (200, 201):
            if 'count' in res.json(): # Did get a KeyError once... when there was nothing there.
                count = res.json()['count'] # Setting the real value of count here
            else:
                count = 0
            config.logging.debug('{}Response Now: {} {}'.format(config.YELLOW, res.json(), config.END))
            result = result + res.json()[dictKey]
            config.logging.debug('{}Result as of Now: {} {}'.format(config.YELLOW, result, config.END))
            skip += 100
        else:
            config.logging.error('{red}All {key} Export: Failed getting {key}{end}'.format(red=config.RED, key=dictKey, end=config.END))
            config.logging.error('{}URL: {}{}'.format(config.RED, url, config.END))
            config.logging.error('{}HTTP Status Code: {}{}'.format(config.RED, res.status_code, config.END))
            config.logging.error('{red}Error Message: {txt}{end}'.format(red=config.RED, txt=res.text, end=config.END))
            return None
    if result:
        return {dictKey: result, 'count': count}
    config.logging.info('No {} results in content type {} and locale {}.'.format(dictKey, contentType, locale))
    return None

def getAllEntries(contentType, locale, environment, query=None):
    '''
    Gets all entries in the Delivery API
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}/entries?locale={language_code}&include_workflow={boolean_value}&include_publish_details={boolean_value}
    if environment:
        fetches only entries published in that environment
    if query:
        finds entries based on that query
    '''
    url = '{region}v3/content_types/{contentType}/entries?locale={locale}&include_count=true'.format(region=region, contentType=contentType, locale=locale)
    if query:
        url = url + '&query={}'.format(query)
    return typicalGetIterate(url, 'entries', environment, contentType, locale)