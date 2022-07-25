from facebook import GraphAPI
import json
from src.Bots.base_bot import BaseBot

# the access token for using fb graph api
access_token_pg = 'Access Token'


class FacebookBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.graph = None
        self.access_token_pg = access_token_pg
        self.methods = {'my_feed': self.multiple_text_posts_in_feed, 'group': self.multiple_text_posts_in_group}
        self.login()

    def login(self):
        # Get Graph
        self.graph = GraphAPI(access_token=self.access_token_pg)

    def parse_format(self):
        pass

    def run(self, where: str, **kwargs):
        self.methods[where](**kwargs)

    def text_post(self, parent_object: str, connection_name: str, message: str, link: str = None):
        self.graph.put_object(
            parent_object=parent_object,
            connection_name=connection_name,
            message=message,
            link=link)
        print("Posted " + message + " On facebook")

    # Create Multiple New Text Posts On Page
    def multiple_text_posts_in_feed(self, messages: list, link: str = None, parent_object="me", connection_name="feed"):
        for message in messages:
            self.text_post(parent_object, connection_name, message, link)

    # Create Multiple New Text Posts On Group by group ID
    def multiple_text_posts_in_group(self, messages: list, groups_id: list, link: str = None,
                                     connection_name="feed"):
        for message in messages:
            for group_id in groups_id:
                self.text_post(group_id, connection_name, message, link)

    # Delete Post By Id
    def delete_post(self, post_id):
        self.graph.delete_object(id=post_id)
        print("Post with ID " + post_id + " Deleted")

    # Comment On Post By Id
    def comment_on_post(self, post_id, message):
        self.graph.put_comment(object_id=post_id, message=message)
        print("Commented On the Post")

    # Retrieve last post id
    def retrieve_last_post_id(self):
        pass

    # Store Last Post Id
    def store_last_post_id(self, last_post_id):
        pass


# fb = FacebookBot()
# fb.post(where="group", messages=['test'], groups_id=['744128789503859'])
