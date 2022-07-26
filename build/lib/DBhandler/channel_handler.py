from mongo_handler import MongoHandler
from utils import COLLECTION_NAME, CONNECTION_STRING, DB_NAME


class ChannelHandler(MongoHandler):
    def __init__(self, connection_string=CONNECTION_STRING, db_name=DB_NAME,
                 collection_name=COLLECTION_NAME, doc_type="channel"):
        super().__init__(connection_string, db_name, collection_name, doc_type)
        self.channel_id_key = "_id"

    def get_all_channels(self) -> list:
        return self.query(**{})

    def get_channels(self, channel_ids: list[str]):
        channel_ids = [self.convert_to_object_id(channel_id) for channel_id in channel_ids]
        query_to_mongo = {self.channel_id_key: {"$in": channel_ids}}
        return self.query(**query_to_mongo)

    def get_channels_platform_and_id(self):
        results = self.get_all_channels()
        results_to_return = [{"platform": data["platform"], "id": str(data['_id'])} for data in results]
        return results_to_return

    def get_channel_details(self, channel_id: str) -> dict:
        channel_id = self.convert_to_object_id(channel_id)
        results = self.query(**{self.channel_id_key: channel_id})
        return results[0] if results else None

    def delete_channel(self, channel_id: str):
        channel_id = self.convert_to_object_id(channel_id)
        return self.delete(**{self.channel_id_key: channel_id})

    def delete_all_channels(self):
        return self.delete(**{})

    def update_channel_details(self, channel_id: str, **details_to_update):
        channel_id = self.convert_to_object_id(channel_id)
        return self.update({self.channel_id_key: channel_id}, **details_to_update)

    def update_all_channels_details(self, **details_to_update):
        return self.update({}, **details_to_update)
