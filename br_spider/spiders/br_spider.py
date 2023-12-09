"""Gather game and player data from basketball-reference.com"""
# -*- coding: utf-8 -*-
import scrapy
import datetime as dt
from ..items import BasicGameData, DetailedGameData

class BRDataSpider(scrapy.Spider):
    name = "basketball-reference"
    
    def __init__(self, season=None, *args, **kwargs):
        super(BRDataSpider, self).__init__(*args, **kwargs)  # pass all arguments to standart class
        self.season = season if season is not None else dt.date.today().strftime("%Y")
        self.start_urls = [f'https://www.basketball-reference.com/leagues/NBA_{self.season}_games.html']
        
    def parse(self, response):
        """Parsing page links for this season."""
        season_pages = response.xpath("//div[@class='filter']/*/a")  # selects all anchors for months of the season
        yield from response.follow_all(season_pages, callback=self.parse_game_data)  # generate requests for all pages automatically
        
    def _extract_datetime(self, raw_date, read_format="%a, %b %d, %Y %I:%M%p", save_format="%Y-%m-%dT%H:%M:%S"):
        """Extract date or time in ISO-format. Check python datetime docs for formating options."""
        date = dt.datetime.strptime(raw_date, read_format)
        return date.strftime(save_format)
    
    def parse_game_data(self, response):
        """Parsing game data from a single page."""
        games = response.xpath("//*/table[@id='schedule']/tbody/*")  # select all games data in the table
        for game in games:
            # data is arranged on different levels, check HTML structure of table on website
            date = game.xpath("*[@data-stat='date_game']/a/text()").get()
            time_raw = game.xpath("*[@data-stat='game_start_time']/text()").get()
            if time_raw is not None:  # seasons before 2000 do not list game time
                splt = time_raw.split(':')
                time = splt[0].zfill(2)+':'+splt[1]+'m'  # adding full am/pm note and padding zeros
            else:
                time = '12:00am'
            date_time = ' '.join([date, time])
            h_team = game.xpath("*[@data-stat='home_team_name']/a/text()").get()
            h_score = game.xpath("*[@data-stat='home_pts']/text()").get()
            a_team = game.xpath("*[@data-stat='visitor_team_name']/a/text()").get()
            a_score = game.xpath("*[@data-stat='visitor_pts']/text()").get()
            attendance = games[0].xpath("*[@data-stat='attendance']/text()").get()
            if attendance is not None:  # older seasons do not always list attendance
                attendance = attendance.replace(",", '')
            overtime = game.xpath("*[@data-stat='overtimes']/text()").get()
            notes = game.xpath("*[@data-stat='game_remarks']/text()").get()

            # scrape basic game information from page
            yield BasicGameData(date=self._extract_datetime(date_time),
                                weekday=self._extract_datetime(date_time, save_format="%A"),  # %A means weekday
                                home_team=h_team,
                                home_score=h_score,
                                away_team=a_team,
                                away_score=a_score,
                                attendance=attendance,
                                overtime=overtime,
                                remarks=notes,
                                )
            
            # yield request for additional detailed game data
            game_details = game.xpath("*/a[text()='Box Score']")
            yield from response.follow_all(game_details, callback=self.parse_game_details)
            
    def parse_game_details(self, response):
        """Parsing more detailed information for each game."""
        date_time = response.xpath("//*/*[@class='scorebox_meta']/div/text()").get()  # reading date/time
        if ":" in date_time:
            date_time = self._extract_datetime(date_time, read_format="%I:%M %p, %B %d, %Y")
        else:
            date_time = self._extract_datetime('12:00 am, '+date_time, read_format="%I:%M %p, %B %d, %Y")
        info_tables = response.xpath("//div[@class='table_container' and contains(@id, 'game-basic')]")  # gathering tables
        
        # cycle through home/away tables
        for table in info_tables:
            team = table.xpath("*/caption/text()").get().split("(")[0].strip()  # extract team name
            player_rows = table.xpath("*/*/tr[th[@scope='row']]")[:-1]  # last row is game total stats, skipping it
            # loop through all players, first five are starters
            for i, player in enumerate(player_rows):
                if 'Starters' in table.xpath("*/*/tr/th/text()").extract():
                    role = 'Starter' if i < 5 else 'Reserve'
                else:
                    role = None
                name = player.xpath("*/a/text()").get()
                stats = {stat.attrib['data-stat'].upper(): stat.xpath("text()").get() for stat in player.xpath("td")}
                
                # scrape player specific game data 
                yield DetailedGameData(date=date_time,
                                       team=team,
                                       player=name,
                                       role=role,
                                       stats=stats,
                                       )
                
                
            
            
            
            
        
        
        
        
        
            
            
            