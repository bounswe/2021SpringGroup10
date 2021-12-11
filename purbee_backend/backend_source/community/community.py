import pymongo
from database.database_utilities import (
    save_new_community,
    get_community_by_community_id
)


class Community:
    def __init__(self, community_dict):
        self.id = None
        # MongoDB automotically creates a unique id and returns it when POST functionality used
        # self.next_post_type_id = None
        self.admin_list = None
        self.subscriber_list = None
        self.post_type_id_list = None
        self.post_history_id_list = None
        self.description = None
        self.photo = None
        self.community_creator_id = None
        self.created_at = None
        self.banned_user_list = None
        self.is_private = None
        self.update(community_dict)

    def update(self, community_dict):
        for community_field_name, community_field_value in community_dict.items():
            setattr(self, community_field_name, community_field_value)

    def to_dict(self):
        dict_object = {
            'id': self.id,
            'admin_list': self.admin_list,
            'subscriber_list': self.subscriber_list,
            'post_type_id_list': self.post_type_id_list,
            'post_history_id_list': self.post_history_id_list,
            'description': self.description,
            'photo': self.photo,
            'community_creator_id': self.community_creator_id,
            'created_at': self.created_at,
            'banned_user_list': self.banned_user_list,
            'is_private': self.is_private
        }
        return dict_object

    def save2database(self):
        community_dictionary = self.to_dict()
        result = save_new_community(community_dictionary)
        return result

    @staticmethod
    def get_community_from_id(community_id):
        # TODO: implement this method
        # do database stuff and get the community_dict
        result, community_dict = get_community_by_community_id(community_id)
        if result == 0:
            return result, Community(community_dict)
        return result, None

