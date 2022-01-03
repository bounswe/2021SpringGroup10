from database.database_utilities import (
    create_new_discussion,
    update_discussion,
    get_discussion_dict_by_discussion_id
)
import uuid


class Discussion:
    def __init__(self, discussion_dict):
        self.id = None
        self.comment_list = []
        self.update(discussion_dict)

    def update(self, discussion_dict):
        for discussion_field_name, discussion_field_value in discussion_dict:
            setattr(self, discussion_field_name, discussion_field_value)

    def to_dict(self):
        dict_object = {
            "id": self.id,
            "comment_list": self.comment_list
        }
        return dict_object

    @staticmethod
    def create_new_empty_discussion(env=None):
        discussion_id = uuid.uuid4()
        discussion_dict = {
            'id': discussion_id,
            'comment_list': []
        }
        result = create_new_discussion(discussion_dict, env)
        if result == 0:
            return discussion_dict
        else:
            return None

    @staticmethod
    def update_on_database(discussion_dictionary, env=None):
        result = update_discussion(discussion_dictionary, env)
        return result

    @staticmethod
    def add_comment(comment_id, discussion_id, env=None):
        current_discussion = get_discussion_dict_by_discussion_id(discussion_id, env)
        current_discussion['comment_list'].append(comment_id)
        return Discussion.update_on_database(current_discussion, env)
