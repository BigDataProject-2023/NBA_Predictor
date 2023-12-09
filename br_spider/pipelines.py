# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import CsvItemExporter
import pandas as pd


class BRDataSpiderPipeline:
    """Storing basic game data and detailed game data in different files."""
    SaveTypes = ['basic', 'detailed']

    def open_spider(self, spider):  # save basic and detailed data in separate files
        self.files = {id: open(f'season_{spider.season}_{id}.csv', 'wb') for id in self.SaveTypes}
        self.exporters = {id: CsvItemExporter(self.files[id]) for id in self.SaveTypes}
        # adjust ordering of .csv file columns
        self.exporters['basic'].fields_to_export = ['date', 'weekday', 'home_team', 'home_score', 'away_team',
                                                    'away_score', 'attendance', 'overtime', 'remarks']
        self.exporters['detailed'].fields_to_export = ['date', 'team', 'player', 'role', 'MP', 'FG', 
                                                       'FGA', 'FG_PCT', 'FG3', 'FG3A', 'FG3_PCT', 'FT',
                                                       'FTA', 'FT_PCT', 'ORB', 'DRB', 'TRB', 'AST', 'STL',
                                                       'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS']
        for exp in self.exporters.values():  # start exporters up
            exp.start_exporting()

    def close_spider(self, spider):
        for id in self.SaveTypes:
            self.exporters[id].finish_exporting()
            self.files[id].close()
        # read data once more and sort chronologically
        for id in self.SaveTypes:
            data = pd.read_csv(f'season_{spider.season}_{id}.csv')
            data.sort_values(by=['date'], inplace=True)
            data.to_csv(f'season_{spider.season}_{id}.csv', index=False)
            
    def _item_type(self, item):
        return type(item).__name__.replace('GameData','').lower()  # BasicGameData -> basic
    
    def _pre_proccess(self, item):
        # pre-proccess detailed game data
        save_dat = {**item['stats']}
        item.pop('stats')
        save_dat.update(item)
        if 'REASON' in save_dat.keys():
            save_dat = None  # drop row if player did not play
        else:  # convert minutes played to float
            min = save_dat['MP']
            if min is not None:
                save_dat['MP'] = float(min.split(':')[0])+float(min.split(':')[0])/60

        return save_dat

    def process_item(self, item, spider):
        item_id = self._item_type(item)
        assert item_id in self.SaveTypes  # make sure item_id is valid
        if item_id in 'detailed':
            item = self._pre_proccess(item)
        if item is not None:
            self.exporters[item_id].export_item(item)
        return item