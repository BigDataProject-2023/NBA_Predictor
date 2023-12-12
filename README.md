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

## Dataset
- `odds data` : Odds data collecting with sbrscrape, scraping FanDuel odds data ➡️ test.py
  ```sh
    python3 test.py
  year = ["2023", "2024"] , season = ["2023-24"] ➡️ change year with when you want to discover
  ```
  in odds data, you can access tomorrow's betting info. ➡️ bet_api.py, accessable with your own key {https://api.the-odds-api.com/v4/sports}
- `season data` : Seasonal data collecting with https://www.basketball-reference.com/leagues/NBA_{self.season}_games.html site.➡️ br_spider.py
  ```sh
    scrapy crawl basketball-reference -a season=2020 ➡️ crawl command, change season args with when you want.
  ```
- `merged data` : merge odds data & season data with [date, home, away] ➡️ data_preprocess.py

## Result
![result-have to update..](/result.png)
