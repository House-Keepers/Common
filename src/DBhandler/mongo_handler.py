from base_db_handler import BaseDBHandler
from utils import UNKNOWN_ERROR


class MongoHandler(BaseDBHandler):
    def __init__(self, connection_string: str, db_name: str, collection_name: str, doc_type: str, max_pool_size=20):
        super().__init__(connection_string, max_pool_size)
        self.db_name = db_name
        self.collection_name = collection_name
        self._doc_type_key = 'doc_type'
        self.doc_type = doc_type

    def query(self, **search_filter):
        with self.connect() as client:
            db = client[self.db_name]
            collection = db[self.collection_name]
            search_filter = self._adding_doc_type(search_filter)
            results = collection.find(search_filter)
            return list(results)

    def insert(self, documents: list):
        with self.connect() as client:
            db = client[self.db_name]
            collection = db[self.collection_name]
            insert_data = [self._adding_doc_type(document) for document in documents]
            try:
                collection.insert_many(insert_data)
                return True
            except Exception as e:
                print(f"{UNKNOWN_ERROR}: {str(e)}")
                return False

    def _adding_doc_type(self, document: dict):
        document[self._doc_type_key] = self.doc_type
        return document
