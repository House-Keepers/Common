from base_db_handler import BaseDBHandler
from utils import UNKNOWN_ERROR
from bson.objectid import ObjectId


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

    def delete(self, **delete_filter):
        with self.connect() as client:
            db = client[self.db_name]
            collection = db[self.collection_name]
            delete_filter = self._adding_doc_type(delete_filter)
            collection.delete_one(delete_filter)
            return True

    def update(self, search_filter: dict, **new_values_to_update):
        with self.connect() as client:
            db = client[self.db_name]
            collection = db[self.collection_name]
            search_filter = self._adding_doc_type(search_filter)
            new_values_to_update = {'$set': new_values_to_update}
            collection.update_many(search_filter, new_values_to_update)
            return True

    def replace_document(self, search_filter: dict, **new_document_to_replace):
        with self.connect() as client:
            db = client[self.db_name]
            collection = db[self.collection_name]
            search_filter = self._adding_doc_type(search_filter)
            new_document_to_replace = self._adding_doc_type(new_document_to_replace)
            collection.replace_one(search_filter, new_document_to_replace)
            return True

    @staticmethod
    def convert_to_object_id(id: str):
        return ObjectId(id)

    def _adding_doc_type(self, document: dict):
        document[self._doc_type_key] = self.doc_type
        return document
