from community.community import Community
from database import database_utilities
from . import fields
from .post_type import PostType


class Post:
    def __init__(self,
                 _id: int,
                 post_type_id: int,
                 post_owner_user_name: str,
                 like_count: int,
                 post_entries_dictionary_list: dict,
                 # TODO: post_discussion_dictionary: dict,
                 ):
        self._id = _id
        self.post_type_id = post_type_id
        self.post_owner_user_name = post_owner_user_name
        self.post_like_count = like_count
        self.post_fields_list = Post.post_entries_dictionary_list_to_post_fields_list(post_type_id,
                                                                                      post_entries_dictionary_list)
        # TODO:
        #  self.post_discussion_list = Post.post_discussion_dictionary_to_list(post_discussion_dictionary)

    def get_id(self):
        return self._id

    def update_post_entries(self, post_entries_dictionary: dict):
        self.post_fields_list = Post.post_entries_dictionary_to_list(post_entries_dictionary)

    def like(self):
        self.post_like_count = self.post_like_count + 1

    def unlike(self):
        self.post_like_count = self.post_like_count - 1

    def to_dict(self):
        return {"_id": self._id,
                "post_type_id": self.post_type_id,
                "post_owner_user_name": self.post_owner_user_name,
                "post_like_count": self.post_like_count,
                "post_entries": Post.post_entries_to_dict(self.post_entries),
                # TODO: "post_discussion": Post.post_discussion_to_dict(self.post_discussion)
                }

    def save_to_database(self):
        post_dictionary = self.to_dict()
        # TODO: change the name of this function
        _id = database_utilities.save_a_new_post(post_dictionary)
        return _id

    @staticmethod
    def get_post_from_id(post_id):
        post_dictionary = database_utilities.get_post_from_post_id(post_id)
        return Post(**post_dictionary)

    @staticmethod
    def create_new_post(post_type_id: int,
                        post_owner_user_name: str,
                        post_entries_dictionary_list: list
                        ):
        post_id = None
        like_count = 0
        new_post = Post(post_id,
                        post_type_id,
                        post_owner_user_name,
                        like_count,
                        post_entries_dictionary_list,
                        # TODO: post_discussion_dictionary
                        )

        del new_post._id
        _id = new_post.save_to_database()
        del new_post

        new_post = Post.get_post_from_id(_id)
        new_post.has_created()
        return new_post

    @staticmethod
    def update_existing_post(post_id: int,
                             post_entries_dictionary_list):
        post = Post.get_post_from_id(post_id)
        post.update_post_entries(post_entries_dictionary_list)
        _id = post.save_to_database()
        return post

    @staticmethod
    def delete_existing_post(post_id: int):
        database_utilities.delete_post(post_id)
        return post_id

    @staticmethod
    def post_entries_dictionary_list_to_post_fields_list(post_entries_dictionary_list: list,
                                                         post_type_id: int):
        post_fields_list = []

        # Load the post_type object
        post_type_instance = PostType.get_post_type_from_id(post_type_id)
        post_field_info_dictionary_list = post_type_instance.post_field_info_dictionary_list

        # All headers of a field is unique. This is ensured by PostType.create_new_post_type func.
        for post_type_dictionary in post_field_info_dictionary_list:
            field_header = post_type_dictionary["header"]

            post_field_dictionary = next(
                (post_field_dictionary for post_field_dictionary in post_entries_dictionary_list
                 if post_field_dictionary["header"] == field_header), None)

            field_type_name = post_type_dictionary["field_type"]

            field_instance = getattr(fields, field_type_name)(**post_field_dictionary)
            post_fields_list.append(field_instance)

        return post_fields_list

    @staticmethod
    def post_fields_list_to_post_entries_dictionary_list(post_fields_list: list):
        post_entries_dictionary_list = []

        for post_field in post_fields_list:
            post_entry_dictionary = fields.to_dict(post_field)
            post_entries_dictionary_list.append(post_entry_dictionary)

        return post_entries_dictionary_list

    @staticmethod
    def has_created(self):
        community = Community.get_community_from_id(self.base_post_type.parent_community_id)
        community.post_history_id_list.append(self.post_id)

        database_utilities.update_community(community.to_dict())
        database_utilities.add_post_to_user_postlist(self.post_owner_user_name, self.post_id)

    @staticmethod
    def has_deleted(self):
        community = Community.get_community_from_id(self.base_post_type.parent_community_id)
        community.post_history_id_list.pop(self.post_id)
        database_utilities.update_community(community.to_dict())
        database_utilities.remove_post_from_user_postlist(self.post_owner_user_name, self.post_id)
