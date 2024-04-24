# python-unpublish-unlocalised

This set of scripts uses both the Content Management and Content Delivery APIs from Contentstack. Functions found in `cma/` and `cda/` folders.

Scripts in this repository:
1. List Published Unlocalised entries - `listPublishUnlocalised.py` (Finds all entries that are published from a single locale to any locale where unlocalised. Writes the result to a readable CSV file.)
2. Unpublish all entries found in CSV - `unpublishEntriesFromCSV.py` (Reads the CSV file from step 1 and unpublishes all of them.)

*NOT OFFICIALLY SUPPORTED BY CONTENTSTACK*

## Prerequisites:
* Contentstack Account.
* Install Python 3 (Developed using Python 3.9.1 on Macbook).
* Install Python package:
  * `pip install requests`

## Define environmental variables
e.g. `variables.env` file:
```
CS_REGION=NA (Either NA or EU)
CS_APIKEY=blt972.....
CS_MANAGEMENTOKEN=cs....
CS_DELIVERYTOKEN=cs....
CS_BRANCH=cs....
CS_USERNAME=someone@something.com (Not needed in this project)
CS_PASSWORD=password (Not needed in this project)

export CS_REGION CS_APIKEY CS_MANAGEMENTOKEN CS_DELIVERYTOKEN CS_USERNAME CS_PASSWORD CS_BRANCH
```
and run `source variables.env` in the terminal.

