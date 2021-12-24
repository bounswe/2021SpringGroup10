from database.database_utilities import (
    save_new_community,
    get_community_by_community_id,
    update_community,
    get_user_by_name
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
        self.requesters = []
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
            'is_private': self.is_private,
            'requesters': self.requesters
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

    def handle_ban_user(self, user_id):
        community_dictionary = self.to_dict()
        if user_id in self.requesters:
            neu_requesters = community_dictionary['requesters']
            neu_requesters.remove(user_id)
            community_dictionary['requesters'] = neu_requesters
        if user_id in self.subscriber_list:
            neu_subscriber_list = community_dictionary['subscriber_list']
            neu_subscriber_list.remove(user_id)
            community_dictionary['subscriber_list'] = neu_subscriber_list
        neu_banned_user_list = community_dictionary['banned_user_list']
        neu_banned_user_list.append(user_id)
        community_dictionary['banned_user_list'] = neu_banned_user_list
        result = update_community(community_dictionary)
        if result == 0:
            self.update(community_dictionary)
        return result

    def handle_unban_user(self, user_id):
        community_dictionary = self.to_dict()
        neu_banned_user_list = community_dictionary['banned_user_list']
        neu_banned_user_list.remove(user_id)
        community_dictionary['banned_user_list'] = neu_banned_user_list
        result = update_community(community_dictionary)
        if result == 0:
            self.update(community_dictionary)
        return result

    @staticmethod
    def ban_user(admin_id, community_id, user_id):
        current_community_dict = get_community_by_community_id(community_id)
        if current_community_dict is None:
            # there is no community with the given community id
            return 11, None
        current_user = get_user_by_name(user_id)
        if current_user is None:
            # there is no user to ban
            return 12, None
        admin = get_user_by_name(admin_id)
        if admin is None:
            # there is no admin
            return 13, None
        if admin_id not in current_community_dict['admin_list']:
            # given user as an admin is not an admin
            return 14, None
        if user_id in current_community_dict['admin_list']:
            # given user is admin
            return 15, None
        if user_id == current_community_dict['community_creator_id']:
            # given user is community creator
            return 16, None

        current_community = Community(current_community_dict)
        result = current_community.handle_ban_user(user_id)
        if result == 0:
            # return success
            return 0, current_community.to_dict()
        else:
            # internal error
            return 1, None

    @staticmethod
    def unban_user(admin_id, community_id, user_id):
        current_community_dict = get_community_by_community_id(community_id)
        if current_community_dict is None:
            # there is no community
            return 11, None
        current_user = get_user_by_name(user_id)
        if current_user is None:
            # there is no user
            return 12, None
        admin = get_user_by_name(admin_id)
        if admin is None:
            # there is no admin
            return 13, None
        if admin_id not in current_community_dict['admin_list']:
            # given admin is not an admin
            return 14, None
        if user_id not in current_community_dict['banned_user_list']:
            # given user is not banned user
            return 15, None

        current_community = Community(current_community_dict)
        result = current_community.handle_unban_user(user_id)
        if result == 0:
            # success
            return 0, current_community.to_dict()
        else:
            # internal error
            return 1, None


