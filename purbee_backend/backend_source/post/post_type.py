import uuid

from community.community import Community
from database import database_utilities


class PostType:
    def __init__(self,
                 _id: int,
                 post_type_name: str,
                 parent_community_id: int,
                 post_field_info_dictionaries_list: list):
        self._id = _id
        self.post_type_name = post_type_name
        self.parent_community_id = parent_community_id
        self.post_field_info_dictionaries_list = post_field_info_dictionaries_list

    def get_id(self):
        return self._id

    def to_dict(self):
        dict = {
            "_id": self.get_id(),
            "post_type_name": self.post_type_name,
            "parent_community_id": self.parent_community_id,
            "post_field_info_dictionaries_list": self.post_field_info_dictionaries_list}

        return dict

    def save_to_database(self):
        post_type_dictionary = self.to_dict()
        return database_utilities.save_post_type(post_type_dictionary)

    @staticmethod
    def create_post_type(post_type_name: str,
                         parent_community_id: int,
                         post_field_info_dictionaries_list: list):

        # Check if headers of the fields are unique.
        headers = [dic["header"] for dic in post_field_info_dictionaries_list]
        if len(headers) != len(set(headers)):
            raise Exception("Headers must be unique inside a post type.")

        # Check if community with given id exists.
        if database_utilities.get_community_by_community_id(parent_community_id) is None:
            raise Exception("No such community with given parent community id exists.")

        # TODO: Check if eligible.

        _id = str(uuid.uuid4())
        new_post_type = PostType(_id,
                                 post_type_name,
                                 parent_community_id,
                                 post_field_info_dictionaries_list)
        new_post_type.save_to_database()
        PostType.has_created(new_post_type)
        return new_post_type

    @staticmethod
    def delete_post_type(post_type_id: int):
        # TODO: This doesn't work rn. First get the post_type, save necessaries.
        #  Then delete. Then update if succesfully deleted.
        post_type = PostType.get_post_type(post_type_id)

        parent_community_id = post_type.parent_community_id
        num_deleted = database_utilities.delete_post_type(post_type_id)
        if num_deleted:
            PostType.has_deleted(post_type_id, parent_community_id)
            return post_type_id
        else:
            raise Exception(f"No such post_type with id {post_type_id} exists.")

    @staticmethod
    def get_post_type(post_type_id: int):
        post_type_dictionary = database_utilities.get_post_type(post_type_id)
        return PostType(**post_type_dictionary)

    @staticmethod
    def has_created(post_type):
        # Update new post_type_id to community_post_type_id list
        community_dictionary = database_utilities.get_community_by_community_id(post_type.parent_community_id)
        community_dictionary["post_type_id_list"].append(post_type.get_id())
        Community.update_on_database(community_dictionary)

    @staticmethod
    def has_deleted(post_type_id, parent_community_id):
        # Carry out the community related updates.
        community_dictionary = database_utilities.get_community_by_community_id(parent_community_id)
        try:
            community_dictionary["post_type_id_list"].remove(post_type_id)
        except ValueError:
            raise Exception("No post_type with given id exists.")
        Community.update_on_database(community_dictionary)

