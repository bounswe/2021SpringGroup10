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
        return {"_id": self._id,
                "post_type_name": self.post_type_name,
                "parent_community_id": self.parent_community_id,
                "post_field_info_dictionaries_list": self.post_field_info_dictionaries_list}

    def save_to_database(self):
        post_type_dictionary = self.to_dict()
        return database_utilities.save_post_type(post_type_dictionary)

    def has_created(self):
        # Carry out the community related updates.
        community = Community.get_community_from_id(self.parent_community_id)

        #   Append new post_type_id to community_post_type_id list
        community.post_type_id_list.append(self._id)

        # Save the updated community.
        database_utilities.update_community(community.to_dict())

    def has_deleted(self):
        # Carry out the community related updates.
        community = Community.get_community_from_id(self.parent_community_id)

        #   Append new post_type_id to community_post_type_id list
        community.post_type_id_list.pop(self._id)

        # Save the updated community.
        database_utilities.update_community(community.to_dict())

    @staticmethod
    def get_post_type_from_id(post_type_id: int):
        post_type_dictionary = database_utilities.get_post_type_from_post_type_id(post_type_id)
        return PostType(**post_type_dictionary)

    @staticmethod
    def create_new_post_type(post_type_name: str,
                             parent_community_id: int,
                             post_field_info_dictionaries_list: list):
        # TODO: Make sure all headers are unique in a post type.
        _id = None
        new_post_type = PostType(_id,
                                 post_type_name,
                                 parent_community_id,
                                 post_field_info_dictionaries_list)

        _id = new_post_type.save_to_database()
        del new_post_type

        new_post_type = PostType.get_post_type_from_id(_id)
        new_post_type.has_created()
        return new_post_type
