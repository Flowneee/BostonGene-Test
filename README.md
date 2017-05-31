# Test for BostonGene company

## Description
This program runs server that calculates MD5 hash of documents, avaliable via URL. Program consists of MongoDB, Celery and Django, and running in Docker containers.

## Prerequisites
 - Docker 1.10.0+
 - Compose 1.6.0+

## Installation
Simply clone this repository and run `docker-compose up` in repo's root directory. Server will be avaliable at port 8000.

## Usage
1. To initiate process, send POST request with desired URL in content and with "Content-Type:text/plain" to URL "\<address\>/". Response will have status code **202** and contain (in content) quoted string with GUID, which associated with request. Using CURL:

`$ curl --data "http://2ch.hk" -X POST --header "Content-Type:text/plain" "127.0.0.1:8000/"`

2. After getting GUID, you can access to result of request. To do this, send GET request to URL "\<address\>/\<GUID\>/" (GUID without quotes and note the slash at the end). Answer can be:
- **200**: process completed succesfull. Result of calculation stored in content as quoted string;
- **409**: process not completed.
- **400**: internal error. Traceback stored in content.

 Using CURL:

`$ curl "127.0.0.1:8000/f8260b23-951e-4fe1-af1c-b4c48bf241a5/"`

Also program can be used via web interface, located at "\<address\>/"
