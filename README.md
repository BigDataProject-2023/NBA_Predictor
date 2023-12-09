# Basketball-Reference Webcrawler

Scrapy-based webcrawler which collects all data for a specific NBA season from [basketball-reference.com](https://www.basketball-reference.com/).

## Prerequisites
Requires the [scrapy](https://scrapy.org/) and [pandas](https://pandas.pydata.org/) python packages to be installed.

## Usage
The webcrawler can be started from the project directory using the command
```sh
scrapy crawl basketball-reference -a season=2020
```
where the season for which data should be collected is given by the  ```season``` argument (default is current season).
