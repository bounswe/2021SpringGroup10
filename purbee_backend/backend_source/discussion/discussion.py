from database.database_utilities import (
    create_new_discussion,
    update_discussion,
    get_discussion_dict_by_discussion_id,
    get_comment_dict_by_comment_id
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
        discussion_id = str(uuid.uuid4())
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

    @staticmethod
    def get_discussion(discussion_id, env=None):
        current_discussion = get_discussion_dict_by_discussion_id(discussion_id, env)
        if current_discussion is None:
            # there is no discussion with the given discussion id
            return 11, None
        comment_list = current_discussion['comment_list']
        resulting_comments = []
        for comment_id in comment_list:
            current_comment = get_comment_dict_by_comment_id(comment_id, env)
            resulting_comments.append(current_comment)
        current_discussion['comment_object_list'] = resulting_comments
        return 0, current_discussion

