from mongo_handler import MongoHandler
from utils import COLLECTION_NAME, CONNECTION_STRING, DB_NAME
from bson.objectid import ObjectId


class BotHandler(MongoHandler):
    def __init__(self, connection_string=CONNECTION_STRING, db_name=DB_NAME,
                 collection_name=COLLECTION_NAME, doc_type='bot'):
        super().__init__(connection_string, db_name, collection_name, doc_type)
        self.bot_id_key = '_id'

    def get_all_bots(self):
        return self.query(**{})

    def get_bot_details(self, bot_id: str) -> dict:
        bot_id = self.convert_to_object_id(bot_id)
        results = self.query(**{self.bot_id_key: bot_id})
        return results[0] if results else None

    def get_bots_name_and_id(self):
        results = self.get_all_bots()
        results_to_return = [{"name": data["name"], "id": str(data['_id'])} for data in results]
        return results_to_return

    def insert_bot(self, bot_details: dict):
        self.insert([bot_details])

    def delete_bot(self, bot_id: str):
        bot_id = self.convert_to_object_id(bot_id)
        return self.delete(**{self.bot_id_key: bot_id})

    def delete_all_bots(self):
        return self.delete(**{})

    def update_bot_details(self, bot_id: str, **details_to_update):
        bot_id = self.convert_to_object_id(bot_id)
        return self.update({self.bot_id_key: bot_id}, **details_to_update)

    def update_all_bots_details(self, **details_to_update):
        return self.update({}, **details_to_update)
