from community.community import Community
from database.database_utilities import (
    update_community,
    add_post_to_user_postlist,
    save_a_new_post,
    get_post_from_post_id)
from .post_type import PostType


class Post:
    def __init__(self,
                 post_id: int,
                 post_type_id: int,
                 post_owner_user_name: str,
                 like_count: int,
                 post_entries_dictionary: dict,
                 post_discussion_dictionary: dict):

        self.post_id = post_id
        self.post_type_id = post_type_id
        self.post_owner_user_name = post_owner_user_name
        self.post_like_count = like_count
        self.post_entries_list = Post.post_entries_dictionary2list(post_type_id, post_entries_dictionary)
        # TODO: This is not going to be a list probably.
        self.post_discussion_list = Post.post_discussion_dictionary2list(post_discussion_dictionary)

    def update_post_entries(self, post_entries_dictionary: dict):
        self.post_entries_list = Post.post_entries_dictionary2list(post_entries_dictionary)

    def like(self):
        self.post_like_count = self.post_like_count + 1

    def unlike(self):
        self.post_like_count = self.post_like_count - 1

    def update_after_creation(self):
        community = Community.get_community_from_id(self.base_post_type.parent_community_id)
        community.post_history_id_list.append(self.post_id)
        update_community(community.to_dict())
        add_post_to_user_postlist(self.post_owner_user_name, self.post_id)

    def to_dict(self):
        return {"post_id": self.post_id,
                "post_type_id": self.post_type_id,
                "post_owner_user_name": self.post_owner_user_name,
                "post_like_count": self.post_like_count,
                "post_entries": Post.post_entries2dict(self.post_entries),
                "post_discussion": Post.post_discussion2dict(self.post_discussion)}

    def save2database(self):
        post_dictionary = self.to_dict()
        # TODO: change the name of this function
        save_a_new_post(post_dictionary)

    @staticmethod
    def get_post_from_id(post_id):
        """ post_dictionary = {"base_post_type": PostType,
                         "fields_dictionary": dict,
                         "post_id": int,
                         "post_owner_user_name": str}
                         """

        # this is a db method
        post_dictionary = get_post_from_post_id(post_id)
        post_type_dictionary = post_dictionary["base_post_type"]
        base_post_type = PostType(post_type_dictionary["fields_dictionary"],
                                  post_type_dictionary["post_type_name"],
                                  post_type_dictionary["parent_community_id"],
                                  post_type_dictionary["post_type_id"])

        return Post(base_post_type,
                    post_type_dictionary["fields_dictionary"],
                    post_dictionary["post_id"],
                    post_dictionary["post_owner_user_name"])

    @staticmethod
    def post_entries2dict():
        post_entries_dict = {}
        return post_entries_dict

    # TODO: remove this method, use the expected function from discussion class.
    @staticmethod
    def post_discussion2dict():
        post_discussion_dict = {}
        return post_discussion_dict

    @staticmethod
    def post_entries_dictionary2list(post_type_id: int,
                                     post_entries_dictionary: dict):
        post_entries_list = []
        return post_entries_list

    @staticmethod
    def post_discussion_dictionary2list():
        # TODO: This is not going to be a list probably.
        post_discussion_list = []
        return post_discussion_list

    @staticmethod
    def create_new_post(post_type_id: int,
                        post_owner_user_name: str,
                        ):
        post_id = None
        like_count = 0
        post_entries_dictionary = {}
        post_discussion_dictionary = {}
        new_post = Post(post_id,
                        post_type_id,
                        post_owner_user_name,
                        like_count,
                        post_entries_dictionary,
                        post_discussion_dictionary)

        return new_post
