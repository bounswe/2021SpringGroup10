from database.database_utilities import (
    save_new_community,
    get_community_by_community_id,
    update_community
)


class Community:
    def __init__(self, community_dict):
        self.id = None
        # MongoDB automatically creates a unique id and returns it when POST functionality used
        # self.next_post_type_id = None
        self.admin_list = []
        self.subscriber_list = []
        self.post_type_id_list = []
        self.post_history_id_list = []
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
        print("community_dict", community_dict)
        if community_dict:
            return Community(community_dict)
        return None

