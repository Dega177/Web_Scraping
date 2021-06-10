import pymongo


class MongoPipeline:

    def __init__(self):
        self.db = pymongo.MongoClient('mongodb://localhost:27017')
        self.db_name = 'auto_youla'
        self.collection_name = 'youla_parse'

    def process_item(self, data, spider):
        self.db[self.db_name][self.collection_name].insert_one(data)
        return data
