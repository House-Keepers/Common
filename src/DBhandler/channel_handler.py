from mongo_handler import MongoHandler
from utils import CHANNELS_COLLECTION_NAME, CONNECTION_STRING, DB_NAME, UNKNOWN_ERROR


class ChannelHandler(MongoHandler):
    def __init__(self, connection_string: CONNECTION_STRING, db_name: DB_NAME,
                 collection_name: CHANNELS_COLLECTION_NAME):
        super().__init__(connection_string, db_name, collection_name)
        self._key_mapping_in_db = {'channel_id': 'channel_id', 'platform': 'platform'}

    def _get_key_mapping_in_db(self, key: str):
        return self._key_mapping_in_db[key]

    def _get_channel_id_key_in_db(self):
        return self._key_mapping_in_db['channel_id']

    def get_all_channels(self) -> list:
        return self.query(**{})

    def get_channel_details(self, channel_id: str) -> dict:
        results = self.query(**{self._get_channel_id_key_in_db: channel_id})
        return results[0] if results else None

    def get_channel_platform(self, channel_id: str) -> str:
        results = self.query(**{self._get_channel_id_key_in_db: channel_id})
        return results[0][self._get_key_mapping_in_db('platform')] if results else None

    def insert_new_channel(self, channel_details: dict):
        try:
            self.insert(**channel_details)
        except Exception as e:
            print(f"{UNKNOWN_ERROR}: {str(e)}")
