from base_db_handler import BaseDBHandler


class MongoHandler(BaseDBHandler):
    def __init__(self, connection_string: str, db_name: str, collection_name: str, max_pool_size=50):
        super().__init__(connection_string, max_pool_size)
        self.db_name = db_name
        self.collection_name = collection_name

    def query(self, **search_filter):
        with self.connect() as client:
            db = client[self.db_name]
            collection = db[self.collection_name]
            results = collection.find(search_filter)
            return list(results)

    def insert(self, **data):
        with self.connect() as client:
            db = client[self.db_name]
            collection = db[self.collection_name]
            collection.insert_one(data)
            return True

