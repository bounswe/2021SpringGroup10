from database.database_utilities import (
    save_new_community,
    get_community_by_community_id,
    update_community,
    get_user_by_name
)
import datetime


class Community:
    def __init__(self, community_dict):
        self.id = None
        # MongoDB automatically creates a unique id and returns it when POST functionality used
        # self.next_post_type_id = None
        self.admin_list = []
        self.subscriber_list = []
        self.requesters = []
        self.post_type_id_list = []
        self.post_type_name_list = []
        self.post_history_id_list = []
        self.requesters = []
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
            'post_type_name_list': self.PostType.post_type_id_list_to_post_type_name_list(self.post_type_id_list),
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

    def save2database(self, env=None):
        self.update({"created_at": str(datetime.datetime.now())})
        community_dictionary = self.to_dict()
        result = save_new_community(community_dictionary, env)
        return result

    @staticmethod
    def update_on_database(community_dictionary, env=None):
        result = update_community(community_dictionary, env)
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

    def add_subscriber(self, user_id, env):
        if user_id in self.subscriber_list:
            # already subscriber
            return 2
        neu_subscriber_list = self.subscriber_list
        neu_subscriber_list.append(user_id)
        community_dictionary = self.to_dict()
        community_dictionary['subscriber_list'] = neu_subscriber_list
        result = update_community(community_dictionary, env)
        if result == 0:
            self.subscriber_list = neu_subscriber_list
        return result

    def remove_subscriber(self, user_id, env=None):
        neu_subscriber_list = self.subscriber_list
        neu_subscriber_list.remove(user_id)
        community_dictionary = self.to_dict()
        community_dictionary['subscriber_list'] = neu_subscriber_list
        result = update_community(community_dictionary, env)
        if result == 0:
            self.subscriber_list = neu_subscriber_list
        return result

    def add_requester(self, user_id, env=None):
        if user_id in self.subscriber_list or user_id in self.requesters:
            # already subscriber
            return 2
        neu_requester_list = self.requesters
        neu_requester_list.append(user_id)
        community_dictionary = self.to_dict()
        community_dictionary['requesters'] = neu_requester_list
        result = update_community(community_dictionary, env=env)
        if result == 0:
            self.requesters = neu_requester_list
        return result

    def remove_requester(self, user_id, env=None):
        neu_requester_list = self.requesters
        neu_requester_list.remove(user_id)
        community_dictionary = self.to_dict()
        community_dictionary['requesters'] = neu_requester_list
        result = update_community(community_dictionary, env)
        if result == 0:
            self.requesters = neu_requester_list
        return result

    def ban_member(self, user_id, env=None):
        neu_subscriber_list = self.subscriber_list
        neu_banned_user_list = self.banned_user_list
        neu_subscriber_list.remove(user_id)
        neu_banned_user_list.append(user_id)
        community_dictionary = self.to_dict()
        community_dictionary['subscriber_list'] = neu_subscriber_list
        community_dictionary['banned_user_list'] = neu_banned_user_list
        result = update_community(community_dictionary, env)
        if result == 0:
            self.subscriber_list = neu_subscriber_list
            self.banned_user_list = neu_banned_user_list
        return result

    def get_post_types(self):
        return self.post_type_id_list

    def make_private(self, env=None):
        community_dictionary = self.to_dict()
        community_dictionary['is_private'] = True
        result = update_community(community_dictionary, env)
        if result == 0:
            self.is_private = True
        return result

    def make_public(self, env=None):
        community_dictionary = self.to_dict()
        community_dictionary['is_private'] = False
        before_requesters = community_dictionary['requesters']
        community_dictionary['requesters'] = []
        subscribers = community_dictionary['subscriber_list']
        subscribers.extend(before_requesters)
        community_dictionary['subscriber_list'] = subscribers
        result = update_community(community_dictionary, env)
        if result == 0:
            self.update(community_dictionary)
        return result

    @staticmethod
    def get_community_from_id(community_id, env=None):
        community_dict = get_community_by_community_id(community_id, env)
        if community_dict:
            return Community(community_dict)
        return None

    def handle_ban_user(self, user_id, env=None):
        community_dictionary = self.to_dict()
        if user_id in self.requesters:
            neu_requesters = community_dictionary['requesters']
            neu_requesters.remove(user_id)
            community_dictionary['requesters'] = neu_requesters
        if user_id in self.subscriber_list:
            neu_subscriber_list = community_dictionary['subscriber_list']
            neu_subscriber_list.remove(user_id)
            community_dictionary['subscriber_list'] = neu_subscriber_list
        if user_id not in self.banned_user_list:
            neu_banned_user_list = community_dictionary['banned_user_list']
            neu_banned_user_list.append(user_id)
            community_dictionary['banned_user_list'] = neu_banned_user_list
            result = update_community(community_dictionary, env)
            if result == 0:
                self.update(community_dictionary)
            return result
        else:
            return 2

    def handle_unban_user(self, user_id, env=None):
        community_dictionary = self.to_dict()
        neu_banned_user_list = community_dictionary['banned_user_list']
        neu_banned_user_list.remove(user_id)
        community_dictionary['banned_user_list'] = neu_banned_user_list
        result = update_community(community_dictionary, env)
        if result == 0:
            self.update(community_dictionary)
        return result

    @staticmethod
    def ban_user(admin_id, community_id, user_id, env=None):
        current_community_dict = get_community_by_community_id(community_id, env)
        if current_community_dict is None:
            # there is no community with the given community id
            return 11, None
        current_user = get_user_by_name(user_id, env)
        if current_user is None:
            # there is no user to ban
            return 12, None
        admin = get_user_by_name(admin_id, env)
        if admin is None:
            # there is no admin
            return 13, None
        if admin_id not in current_community_dict['admin_list'] and admin_id != current_community_dict['community_creator_id']:
            # given user as an admin is not an admin
            return 14, None
        if user_id in current_community_dict['admin_list']:
            # given user is admin
            return 15, None
        if user_id == current_community_dict['community_creator_id']:
            # given user is community creator
            return 16, None

        current_community = Community(current_community_dict)
        result = current_community.handle_ban_user(user_id, env)
        if result == 0:
            # return success
            return 0, current_community.to_dict()
        else:
            # internal error or already banned user
            return result, None

    @staticmethod
    def unban_user(admin_id, community_id, user_id, env=None):
        current_community_dict = get_community_by_community_id(community_id, env)
        if current_community_dict is None:
            # there is no community
            return 11, None
        current_user = get_user_by_name(user_id, env)
        if current_user is None:
            # there is no user
            return 12, None
        admin = get_user_by_name(admin_id, env)
        if admin is None:
            # there is no admin
            return 13, None
        if admin_id not in current_community_dict['admin_list'] and admin_id != current_community_dict['community_creator_id']:
            # given admin is not an admin
            return 14, None
        if user_id not in current_community_dict['banned_user_list']:
            # given user is not banned user
            return 15, None

        current_community = Community(current_community_dict)
        result = current_community.handle_unban_user(user_id, env)
        if result == 0:
            # success
            return 0, current_community.to_dict()
        else:
            # internal error
            return 1, None

    @staticmethod
    def change_privacy(admin_id, community_id, env=None):
        community_dict = get_community_by_community_id(community_id, env)
        if community_dict is None:
            # there is no community with the given community id
            return 11, None
        current_user = get_user_by_name(admin_id, env)
        if current_user is None:
            # there is no user with the given admin id
            return 12, None
        if not (admin_id in community_dict['admin_list'] or admin_id == community_dict['community_creator_id']):
            # given registered user is not the admin of the given community
            return 13, None
        current_community = Community(community_dict)
        if current_community.is_private:
            result = current_community.make_public(env)
            if result == 0:
                # return success to change to public
                return 10, current_community.to_dict()
            else:
                # return fail
                return 1, None
        else:
            result = current_community.make_private(env)
            if result == 0:
                # return success to change to private
                return 0, current_community.to_dict()
            else:
                # return fail
                return 1, None

    @staticmethod
    def subscribe(user_id, community_id, env=None):
        current_community_dict = get_community_by_community_id(community_id, env)
        if current_community_dict is None:
            # there is no community with the given community id
            return 11, None
        current_user = get_user_by_name(user_id, env)        # user names and ids are the same
        if current_user is None:
            # there is no user with the given user id
            return 12, None
        current_community = Community(current_community_dict)
        if current_community.is_private:
            # eger community privatesa
            result = current_community.add_requester(user_id, env)
            if result == 0:
                return 10, current_community.to_dict()
        else:
            result = current_community.add_subscriber(user_id, env)
            if result == 0:
                return 0, current_community.to_dict()
        return result, None

    @staticmethod
    def unsubscribe(user_id, community_id, env=None):
        current_community_dict = get_community_by_community_id(community_id, env)
        if current_community_dict is None:
            # there is no community with the given community id
            return 11, None
        current_user = get_user_by_name(user_id, env)
        if current_user is None:
            # there is no user with the given user id
            return 12, None
        current_community = Community(current_community_dict)
        if current_community.is_private:
            if user_id in current_community.requesters:
                result = current_community.remove_requester(user_id, env)
                if result == 0:
                    # return success
                    return 10, current_community.to_dict()
            elif user_id in current_community.subscriber_list:
                result = current_community.remove_subscriber(user_id, env)
                if result == 0:
                    # retrun success
                    return 0, current_community.to_dict()
                else:
                    # return fail
                    return 1, None
            else:
                # return fail
                return 2, None
        else:
            if user_id in current_community.subscriber_list:
                result = current_community.remove_subscriber(user_id, env)
                if result == 0:
                    # return success
                    return 0, current_community.to_dict()
                else:
                    # return fail
                    return 1, None
            else:
                # return fail
                return 2, None

    @staticmethod
    def make_or_remove_admin(admin_id, community_id, user_id, action, env=None):
        if action not in ['make', 'remove']:
            # bad request
            return 2, None
        current_community_dict = get_community_by_community_id(community_id, env)
        if current_community_dict is None:
            # there is no community
            return 11, None
        current_user = get_user_by_name(user_id, env)
        if current_user is None:
            # there is no user
            return 12, None
        current_admin = get_user_by_name(admin_id, env)
        if current_admin is None:
            # there is no user with the admin_id
            return 13, None
        if admin_id not in current_community_dict['admin_list'] and admin_id != current_community_dict['community_creator_id']:
            # user with the admin_id is not an admin or not and community creator
            return 14, None
        if user_id in current_community_dict['banned_user_list']:
            return 17, None

        current_community = Community(current_community_dict)
        if action == 'make':
            result = current_community.handle_make_admin(user_id, env)
        elif action == 'remove':
            result = current_community.handle_remove_admin(user_id, env)
        else:
            # bad request
            return 2, None

        if result == 0:
            # success
            return 0, current_community.to_dict()
        else:
            return result, None

    def handle_make_admin(self, user_id, env=None):
        community_dictionary = self.to_dict()
        if user_id in community_dictionary['admin_list']:
            # user is already an admin
            return 15
        neu_admin_list = community_dictionary['admin_list']
        neu_admin_list.append(user_id)
        result = update_community(community_dictionary, env)
        if result == 0:
            self.update(community_dictionary)
        return result

    def handle_remove_admin(self, user_id, env=None):
        community_dictionary = self.to_dict()
        if user_id not in community_dictionary['admin_list']:
            # user is not an admin
            return 16
        neu_admin_list = community_dictionary['admin_list']
        neu_admin_list.remove(user_id)
        result = update_community(community_dictionary, env)
        if result == 0:
            self.update(community_dictionary)
        return result

    @staticmethod
    def accept_or_reject_subscription_requester(admin_id, community_id, user_id, action, env=None):
        if action not in ['accept', 'reject']:
            # bad request
            return 2, None
        current_community_dict = get_community_by_community_id(community_id, env)
        if current_community_dict is None:
            # there is no community
            return 11, None
        current_user = get_user_by_name(user_id, env)
        if current_user is None:
            # there is no user
            return 12, None
        current_admin = get_user_by_name(admin_id, env)
        if current_admin is None:
            # there is no user with the admin_id
            return 13, None
        if admin_id not in current_community_dict['admin_list'] and admin_id != current_community_dict['community_creator_id']:
            # user with the admin_id is not an admin
            return 14, None
        if user_id not in current_community_dict['requesters']:
            # user is not a subscription requester
            return 15, None
        if user_id in current_community_dict['subscriber_list']:
            # user is already a subscriber
            return 16, None

        current_community = Community(current_community_dict)
        if action == 'accept':
            result = current_community.handle_accept_request(user_id, env)
        else:
            result = current_community.handle_reject_request(user_id, env)
        if result == 0:
            # success
            return 0, current_community.to_dict()
        else:
            # internal error
            return 1, None

    def handle_accept_request(self, user_id, env=None):
        community_dictionary = self.to_dict()
        neu_requester_list = community_dictionary['requesters']
        neu_requester_list.remove(user_id)
        community_dictionary['requesters'] = neu_requester_list
        neu_subscriber_list = community_dictionary['subscriber_list']
        neu_subscriber_list.append(user_id)
        community_dictionary['subscriber_list'] = neu_subscriber_list
        result = update_community(community_dictionary, env)
        if result == 0:
            self.update(community_dictionary)
        return result

    def handle_reject_request(self, user_id, env=None):
        community_dictionary = self.to_dict()
        neu_requester_list = community_dictionary['requesters']
        neu_requester_list.remove(user_id)
        community_dictionary['requesters'] = neu_requester_list
        result = update_community(community_dictionary, env)
        if result == 0:
            self.update(community_dictionary)
        return result
