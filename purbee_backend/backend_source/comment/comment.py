import uuid
from database.database_utilities import (
    get_discussion_dict_by_discussion_id,
    create_new_comment,
    update_comment,
    get_user_by_name
)
from discussion.discussion import Discussion


class Comment:
    def __init__(self, comment_dictionary):
        self.id = None
        self.discussion_id = None
        self.text = None
        self.creator_id = None
        self.update(comment_dictionary)

    def update(self, comment_dictionary):
        for comment_field_name, comment_field_value in comment_dictionary:
            setattr(self, comment_field_name, comment_field_value)

    def to_dict(self):
        dict_object = {
            "id": self.id,
            "discussion_id": self.discussion_id,
            "text": self.text,
            "creator_id": self.creator_id
        }
        return dict_object

    @staticmethod
    def update_on_database(comment_dictionary):
        return update_comment(comment_dictionary)

    @staticmethod
    def create_comment(parent_discussion_id, text, user_id):
        discussion = get_discussion_dict_by_discussion_id(parent_discussion_id)
        if discussion is None:
            # there is no parent discussion with the defined parent_discussion_id
            return 11, None
        if len(text) <= 0:
            # the text is empty
            return 12, None
        current_creator = get_user_by_name(user_id)
        if current_creator is None:
            # there is no registered user with the given user_id
            return 13, None
        created_discussion = Discussion.create_new_empty_discussion()
        if created_discussion is None:
            # new discussion could not created
            return 14, None
        neu_discussion_id = created_discussion['id']
        neu_comment_id = uuid.uuid4()
        current_comment_dict = {
            "id": neu_comment_id,
            "discussion_id": neu_discussion_id,
            "text": text,
            "creator_id": user_id
        }
        result = create_new_comment(current_comment_dict)
        if result == 0:
            after_result = Discussion.add_comment(neu_comment_id, parent_discussion_id)
            if after_result == 0:
                return 0
            else:
                return after_result + 20
        return result
