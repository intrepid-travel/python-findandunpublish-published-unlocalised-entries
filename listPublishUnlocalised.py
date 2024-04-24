'''
Lists out all published entries of all available content types 
in all available languages that are published in a defined languaages, while being unlocalised.

Step by step execution of the script:
* We first use the Management API to find all content types and all locales on the main branch.
* We then iterate over all the content types and locales on the defined environment using the Delivery API.
    * With the exception, we don't run over entries of the `publishedLocale`.
* When we find an entry in locale n that is actually published in the `publishedLocale` we write that entry to a CSV file.

This script only reads information from the stack - does not change anything.

oskar.eiriksson@contentstack.com
2024-04-20

'''

import os
import cma
import cda
import config

# The environment to check in - Change it to your publishing environment in Contentstack
environment = os.getenv('CS_ENVIRONMENT', None)
if not environment:
    config.logging.critical('{}Environment name Missing as an Environment Variable. Exiting Script.{}'.format(config.RED, config.END))
    exit()

'''
The locale you will check for in the published entries (In this case the master locale).
If you have a locale that is not the master but still a defined fallback for some third level locales, 
you might want to run this script again with that non-master locale.
'''
publishedLocale = 'en-us'

# Getting all locales on the stack
locales = []
for l in cma.getAllLanguages()['locales']:
    if l['code'] != publishedLocale:
        locales.append(l['code'])

# Getting all content types on the stack
contentTypes = []
for c in cma.getAllContentTypes()['content_types']:
    contentTypes.append(c['uid'])

entriesFoundsArr = []
counter = 0
for contentType in contentTypes:
    for locale in locales:
        entries = cda.getAllEntries(contentType, locale, environment)
        if entries:
            for entry in entries['entries']:
                if entry['locale'] == publishedLocale:
                    counter += 1
                    config.logging.info('{yellow}Entry found published in {publishedLocale} in locale {locale}: {entryUID}, of content type {contentType}{end}'.format(yellow=config.YELLOW, publishedLocale=publishedLocale, locale=locale, entryUID=entry['uid'], contentType=contentType, end=config.END))
                    entriesFoundsArr.append({'title': entry['title'], 'uid': entry['uid'], 'contentType': contentType, 'locale': locale})

config.logging.info('{BOLD} Finished logging all entries found. Total count: {counter}{END}'.format(BOLD=config.BOLD, counter=counter, END=config.END))
config.logging.info('Writing entries to a CSV file.')

csvContent = 'Content Type;Title;Entry UID;Locale\n'

for entry in entriesFoundsArr:
    csvContent = csvContent + entry['contentType'] + ';' + entry['title'] + ';' + entry['uid'] + ';' + entry['locale'] + '\n'

f='EntriesList_PublishedIn' + publishedLocale + '.csv' 
with open(f, 'w') as filetowrite:
    filetowrite.write(csvContent)

config.logging.info('{GREEN}Entries found listed in {f}{END}'.format(GREEN=config.GREEN, f=f, END=config.END))

