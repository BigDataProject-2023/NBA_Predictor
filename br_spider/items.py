# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BasicGameData(scrapy.Item):
    """Class for basic game stats."""
    date = scrapy.Field()
    weekday = scrapy.Field()
    home_team = scrapy.Field()
    home_score = scrapy.Field()
    away_team = scrapy.Field()
    away_score = scrapy.Field()
    attendance = scrapy.Field()
    overtime = scrapy.Field()
    remarks = scrapy.Field()

class DetailedGameData(scrapy.Item):
    """Class for detailed game stats."""
    date = scrapy.Field()
    team = scrapy.Field()
    player = scrapy.Field()
    role = scrapy.Field()
    stats = scrapy.Field()