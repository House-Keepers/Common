from src.Bots.base_bot import BaseBot
import tweepy


class Twitter_bot(BaseBot):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        super().__init__()
        auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                        access_token=access_token, access_token_secret=access_token_secret)
        self.__api = tweepy.API(auth=auth)

    def run(self, body):
        self.__api.update_status(body)
