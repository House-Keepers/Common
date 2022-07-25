from mongo_handler import MongoHandler
from utils import COLLECTION_NAME, CONNECTION_STRING, DB_NAME
from bson.objectid import ObjectId


class BotHandler(MongoHandler):
    def __init__(self, connection_string=CONNECTION_STRING, db_name=DB_NAME,
                 collection_name=COLLECTION_NAME, doc_type='bot'):
        super().__init__(connection_string, db_name, collection_name, doc_type)
        self.bot_id_key = '_id'
        self.text_key = 'text'
        self.tags_key = 'tags'
        self.channels_key = 'channels'

    @staticmethod
    def convert_to_object_id(bot_id: str):
        return ObjectId(bot_id)

    def get_all_bots(self):
        return self.query(**{})

    def get_bot_details(self, bot_id: str) -> dict:
        bot_id = self.convert_to_object_id(bot_id)
        results = self.query(**{self.bot_id_key: bot_id})
        return results[0] if results else None

    def get_bots_name_and_id(self):
        results = self.query(**{})


    def add_bot_channel(self, bot_id: str, chanel_id: str):
        results = self.query(**{self.bot_id_key: bot_id})
        channels = results[0][self.channels_key]
        channels.append(chanel_id)
        return self.update({self.bot_id_key: bot_id}, channels=channels)

    def get_bot_text(self, bot_id: str) -> str:
        results = self.query(**{self.bot_id_key: bot_id})
        return results[0][self.text_key] if results else None

    def get_bot_tags(self, bot_id: str) -> list:
        results = self.query(**{self.bot_id_key: bot_id})
        return results[0][self.tags_key] if results else None

    def get_bot_channels(self, bot_id: str) -> list:
        results = self.query(**{self.bot_id_key: bot_id})
        return results[0][self.channels_key] if results else None

    def delete_bot(self, bot_id: str):
        return self.delete(**{self.bot_id_key: bot_id})

    def delete_all_bots(self):
        return self.delete(**{})

    def update_bot_details(self, bot_id: str, **details_to_update):
        return self.update({self.bot_id_key: bot_id}, **details_to_update)

    def update_all_bots_details(self, **details_to_update):
        return self.update({}, **details_to_update)
