from community.community import Community
from database import database_utilities
from . import fields
from .post_type import PostType
import uuid


class Post:
    def   __init__(self,
                 _id: int,
                 post_type_id: str,
                 post_owner_user_name: str,
                 post_liked_user_list: int,
                 post_entries_dictionary_list: dict,
                 # TODO: post_discussion_dictionary: dict,
                 ):
        self._id = _id
        self.post_owner_user_name = post_owner_user_name
        self.post_liked_user_list = post_liked_user_list
        self.post_type_id = post_type_id
        self.post_fields_list = Post.post_entries_dictionary_list_to_post_fields_list(post_type_id,
                                                                                      post_entries_dictionary_list)
        # TODO:
        #  self.post_discussion_list = Post.post_discussion_dictionary_to_list(post_discussion_dictionary)

    def get_id(self):
        return self._id

    def update_post_entries(self, post_entries_dictionary: dict):
        self.post_fields_list = Post.post_entries_dictionary_to_list(post_entries_dictionary)

    def like(self, user_name):
        lst = self.post_liked_user_list
        if user_name not in lst:
            lst.append(user_name)
            self.update_in_database()
        else:
            raise Exception("User already liked the post.")

        return lst

    def unlike(self, user_name):
        lst = self.post_liked_user_list
        try:
            lst.remove(user_name)
        except ValueError:
            raise Exception("User has already not liked the post.")
        self.update_in_database()
        return lst

    def to_dict(self):
        dict = {
            "_id": self.get_id(),
            "post_type_id": self.post_type_id,
            "post_owner_user_name": self.post_owner_user_name,
            "post_liked_user_list": self.post_liked_user_list,
            "post_entries_dictionary_list": Post.post_fields_list_to_post_entries_dictionary_list(self.post_fields_list),
            # TODO: "post_discussion": Post.post_discussion_to_dict(self.post_discussion)
        }
        return dict

    def save_to_database(self):
        post_dictionary = self.to_dict()
        # TODO: change the name of this function
        post_id = database_utilities.save_post(post_dictionary)
        return post_id

    def update_in_database(self):
        post_dictionary = self.to_dict()
        # TODO: change the name of this function
        number_of_updated = database_utilities.update_post(post_dictionary)
        if number_of_updated < 1:
            raise Exception("Nothing could updated.")

        return number_of_updated
    
    @staticmethod
    def create_post(post_type_id: str,
                        post_owner_user_name: str,
                        post_entries_dictionary_list: list
                        ):
        _id = str(uuid.uuid4())
        post_liked_user_list = []
        new_post = Post(_id,
                        post_type_id,
                        post_owner_user_name,
                        post_liked_user_list,
                        post_entries_dictionary_list,
                        # TODO: post_discussion_dictionary
                        )
        new_post.save_to_database()
        Post.has_created(new_post)
        return new_post
    
    @staticmethod
    def update_post(post_id: int,
                             post_entries_dictionary_list):
        post = Post.get_post(post_id)
        post.update_post_entries(post_entries_dictionary_list)
        post.update_in_database()
        return post

    @staticmethod
    def delete_existing_post(post_id: int):
        post = Post.get_post(post_id)
        post_type = PostType.get_post_type(post.post_type_id)
        parent_community_id = post_type.parent_community_id

        num_deleted = database_utilities.delete_post(post_id)
        if num_deleted:
            PostType.has_deleted(post.post_type_id, parent_community_id)
            return post_id
        else:
            raise Exception(f"No such post_type with id \"{post_id}\" exists.")
        return post_id

    @staticmethod
    def get_post(post_id):
        post_dictionary = database_utilities.get_post(post_id)
        return Post(**post_dictionary)


    @staticmethod
    def post_entries_dictionary_list_to_post_fields_list(post_type_id: str,
                                                         post_entries_dictionary_list: list):
        post_fields_list = []

        # Load the post_type object
        post_type_instance = PostType.get_post_type(post_type_id)
        post_field_info_dictionaries_list = post_type_instance.post_field_info_dictionaries_list

        # All headers of a field is unique. This is ensured by PostType.create_new_post_type func.
        for post_type_dictionary in post_field_info_dictionaries_list:
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
    def has_created(post):
        post_type = PostType.get_post_type(post.post_type_id)

        community = Community.get_community_from_id(post_type.parent_community_id)
        community.post_history_id_list.append(post.get_id())

        database_utilities.update_community(community.to_dict())
        database_utilities.add_post_to_user_postlist(post.post_owner_user_name, post.get_id())

    @staticmethod
    def has_deleted(post_id, parent_community_id, post_owner_user_name):

        community = Community.get_community_from_id(parent_community_id)
        community.post_history_id_list.pop(post_id)
        database_utilities.update_community(community.to_dict())

        database_utilities.remove_post_from_user_postlist(post_owner_user_name, post_id)
