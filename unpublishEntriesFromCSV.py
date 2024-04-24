'''
Reads CSV file created by the listPublishUnlocalised.py script.

Iterates over it and unpublishes every entry from the defined environment.

Make sure to review the CSV file before executing script.

Warning: This script makes changes to your stack. It unpublishes all unlocalised entries found in the CSV. 

2024-04-20
oskar.eiriksson@contentstack.com

'''
import os
import cma
import config


environment = os.getenv('CS_ENVIRONMENT', None)
if not environment:
    config.logging.critical('{}Environment name Missing as an Environment Variable. Exiting Script.{}'.format(config.RED, config.END))
    exit()

fName = 'EntriesList_PublishedInen-us.csv' # File we want to read

with open(fName) as f:
    next(f)
    for line in f:
        entry = line.split(';')
        contentType = entry[0]
        uid = entry[1]
        locale = entry[2]
        title = entry[3].replace('\n', '')
        config.logging.info('Unpublishing entry {title}, of content type: {contentType}, in locale: {locale} from environment: {environment}'.format(title=title, contentType=contentType, locale=locale, environment=environment))
        cma.unpublishEntry(contentType, uid, environment, locale)
    