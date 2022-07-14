from mongo_handler import MongoHandler
from utils import COLLECTION_NAME, CONNECTION_STRING, DB_NAME


class ChannelHandler(MongoHandler):
    def __init__(self, connection_string=CONNECTION_STRING, db_name=DB_NAME,
                 collection_name=COLLECTION_NAME, doc_type="channel"):
        super().__init__(connection_string, db_name, collection_name, doc_type)
        self.channel_id_key = "channel_id"
        self.platform_key = 'platform'

    def get_all_channels(self) -> list:
        return self.query(**{})

    def get_channel_details(self, channel_id: str) -> dict:
        results = self.query(**{self.channel_id_key: channel_id})
        return results[0] if results else None

    def get_channel_platform(self, channel_id: str) -> str:
        results = self.query(**{self.channel_id_key: channel_id})
        return results[0][self.platform_key] if results else None
