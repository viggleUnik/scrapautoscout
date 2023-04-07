# Scrapeautoscout 

This is a webscrapper from the largest pan-European online car market.

## Usage

The script runs and creates two new directories where json files with 
the information extracted from the website will be saved. These can later be used to extract
more specific information about the cars

## Installation 
To install this package you have to download it:
```shell
pip install scrapautoscout
```
 **After installation, you can run it locally with default parameters by command:**

```shell
 scrapautoscout 
 ```   

 **Or you can see this list of parameters:** 
```shell
scrapautoscout --help
```

 + --LOCATION LOCATION - 'local' or 's3'
 + --DIR_CACHE DIR_CACHE - Where to save artifacts. Default: 'cache' (relative to project root)
 + --AWS_PROFILE_NAME AWS_PROFILE_NAME - AWS profile name
 + --AWS_S3_BUCKET AWS_S3_BUCKET - AWS S3 bucket
 + --MAKERS MAKERS [MAKERS ] - List of makers delimited by space
 + --LOGS_LEVEL LOGS_LEVEL - Log level, e.g. 'debug', 'info', 'error'

**After this you can run it with specified parameters, example:**

```shell
scrapautoscout --LOCATION 's3' 
```
