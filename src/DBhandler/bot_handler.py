from mongo_handler import MongoHandler
from utils import BOTS_COLLECTION_NAME, CONNECTION_STRING, DB_NAME, UNKNOWN_ERROR


class BotHandler(MongoHandler):
    def __init__(self, connection_string: CONNECTION_STRING, db_name: DB_NAME, collection_name: BOTS_COLLECTION_NAME):
        super().__init__(connection_string, db_name, collection_name)
        self._key_mapping_in_db = {'bot_id': 'bot_id', 'text': 'text', 'tags': 'tags', 'channels': 'channels'}

    def _get_key_mapping_in_db(self, key: str):
        return self._key_mapping_in_db[key]

    def _get_bot_id_key_in_db(self):
        return self._key_mapping_in_db['bot_id']

    def get_all_bots(self):
        return self.query(**{})

    def get_bot_details(self, bot_id: str) -> dict:
        results = self.query(**{self._get_bot_id_key_in_db: bot_id})
        return results[0] if results else None

    def get_bot_text(self, bot_id: str) -> str:
        results = self.query(**{self._get_bot_id_key_in_db: bot_id})
        return results[0][self._get_key_mapping_in_db('text')] if results else None

    def get_bot_tags(self, bot_id: str) -> list:
        results = self.query(**{self._get_bot_id_key_in_db: bot_id})
        return results[0][self._get_key_mapping_in_db('tags')] if results else None

    def get_bot_channels(self, bot_id: str) -> list:
        results = self.query(**{self._get_bot_id_key_in_db: bot_id})
        return results[0][self._get_key_mapping_in_db('channels')] if results else None

    def insert_new_bot(self, bot_details: dict):
        try:
            self.insert(**bot_details)
        except Exception as e:
            print(f"{UNKNOWN_ERROR}: {str(e)}")
