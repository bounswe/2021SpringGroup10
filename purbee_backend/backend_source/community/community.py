from database.database_utilities import (
    save_new_community,
    get_community_by_community_id,
    update_community,
    get_user_by_name
)
import sys


class Community:
    def __init__(self, community_dict):
        self.id = None
        # MongoDB automatically creates a unique id and returns it when POST functionality used
        # self.next_post_type_id = None
        self.admin_list = []
        self.subscriber_list = []
        self.post_type_id_list = []
        self.post_history_id_list = []
        self.requesters = []
        self.description = ""
        self.photo = None
        self.community_creator_id = None
        self.created_at = None
        self.banned_user_list = []
        self.is_private = None
        self.update(community_dict)

    def update(self, community_dict):
        for community_field_name, community_field_value in community_dict.items():
            setattr(self, community_field_name, community_field_value)

        """"for field_name in dir(self):
            if not field_name.startswith('_') and not callable(getattr(self, field_name)):
                if getattr(self, field_name) is None:
                    setattr(self, field_name, [])"""

    def to_dict(self):
        dict_object = {
            'id': self.id,
            'admin_list': self.admin_list,
            'subscriber_list': self.subscriber_list,
            'post_type_id_list': self.post_type_id_list,
            'post_history_id_list': self.post_history_id_list,
            'description': self.description,
            'photo': self.photo,
            'requesters': self.requesters,
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
    def update_on_database(community_dictionary):
        result = update_community(community_dictionary)
        return result

    def remove_member(self, user_id):
        neu_subscriber_list = self.subscriber_list
        neu_subscriber_list.remove(user_id)
        community_dictionary = self.to_dict()
        community_dictionary['subscriber_list'] = neu_subscriber_list
        result = update_community(community_dictionary)
        if result == 0:
            self.subscriber_list = neu_subscriber_list
        return result

    def add_subscriber(self, user_id):
        if user_id in self.subscriber_list:
            # already subscriber
            return 2
        neu_subscriber_list = self.subscriber_list
        neu_subscriber_list.append(user_id)
        community_dictionary = self.to_dict()
        community_dictionary['subscriber_list'] = neu_subscriber_list
        result = update_community(community_dictionary)
        if result == 0:
            self.subscriber_list = neu_subscriber_list
        return result

    def add_requester(self, user_id):
        if user_id in self.subscriber_list or user_id in self.requesters:
            # already subscriber
            return 2
        neu_requester_list = self.requesters
        neu_requester_list.append(user_id)
        community_dictionary = self.to_dict()
        community_dictionary['requesters'] = neu_requester_list
        result = update_community(community_dictionary)
        if result == 0:
            self.requesters = neu_requester_list
        return result

    def ban_member(self, user_id):
        neu_subscriber_list = self.subscriber_list
        neu_banned_user_list = self.banned_user_list
        neu_subscriber_list.remove(user_id)
        neu_banned_user_list.append(user_id)
        community_dictionary = self.to_dict()
        community_dictionary['subscriber_list'] = neu_subscriber_list
        community_dictionary['banned_user_list'] = neu_banned_user_list
        result = update_community(community_dictionary)
        if result == 0:
            self.subscriber_list = neu_subscriber_list
            self.banned_user_list = neu_banned_user_list
        return result

    def get_post_types(self):
        return self.post_type_id_list

    @staticmethod
    def get_community_from_id(community_id):
        community_dict = get_community_by_community_id(community_id)
        if community_dict:
            return Community(community_dict)
        return None

    @staticmethod
    def subscribe(user_id, community_id):
        current_community_dict = get_community_by_community_id(community_id)
        if current_community_dict is None:
            # there is no community with the given community id
            return 11, None
        current_user = get_user_by_name(user_id) # user names and ids are the same
        if current_user is None:
            # there is no user with the given user id
            return 12, None
        current_community = Community(current_community_dict)
        if current_community.is_private:
            # eger community privatesa
            result = current_community.add_requester(user_id)
            if result == 0:
                return 10, current_community.to_dict()
        else:
            result = current_community.add_subscriber(user_id)
            if result == 0:
                return 0, current_community.to_dict()
        return result, None

