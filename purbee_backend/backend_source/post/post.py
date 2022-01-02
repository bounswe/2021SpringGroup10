import datetime
import uuid

from community.community import Community
from database import database_utilities
from discussion.discussion import Discussion
from . import fields
from .post_type import PostType


class Post:
    def __init__(self,
                 _id: int,
                 post_type_id: str,
                 post_owner_user_name: str,
                 post_liked_user_list: int,
                 post_entries_dictionary_list: dict,
                 post_discussion_id: str,
                 post_creation_time: str,
                 post_title: str
                 ):
        self._id = _id
        self.post_owner_user_name = post_owner_user_name
        self.post_liked_user_list = post_liked_user_list
        self.post_type_id = post_type_id
        self.post_fields_list = Post.post_entries_dictionary_list_to_post_fields_list(post_type_id,
                                                                                      post_entries_dictionary_list)
        self.post_discussion_id = post_discussion_id
        self.post_creation_time = post_creation_time
        self.post_title = post_title

    def get_id(self):
        return self._id

    def update_post_entries(self, post_entries_dictionary: dict):
        self.post_fields_list = Post.post_entries_dictionary_to_list(post_entries_dictionary)

    def like(self, user_name):
        lst = self.post_liked_user_list
        if user_name not in lst:
            lst.append(user_name)
        else:
            raise Exception("User already liked the post.")

        return lst

    def unlike(self, user_name):
        lst = self.post_liked_user_list
        try:
            lst.remove(user_name)
        except ValueError:
            raise Exception("User has already not liked the post.")
        return lst

    def participate_to_a_participation_field(self, header_of_participation_field, user_name):
        for field in self.post_fields_list:
            if field.header == header_of_participation_field:
                if not isinstance(field, fields.Participation):
                    raise Exception(f"Given header name is not a header of a field\
                    type Participation, it is of type {type(field).__name__()}")
                else:
                    field.participate(user_name)

                    return field.list_of_participants
            else:
                continue

        raise Exception(f"Post with _id: {self.get_id()} has no field of type Participation\
        with header {header_of_participation_field}")

    def cancel_participation_to_a_participation_field(self, header_of_participation_field, user_name):
        for field in self.post_fields_list:
            if field.header == header_of_participation_field:
                if not isinstance(field, fields.Participation):
                    raise Exception(f"Given header name is not a header of a field" \
                                    f"type Participation, it is of type {type(field).__name__()}")
                else:
                    field.cancel_participation(user_name)
                    return field.list_of_participants
            else:
                continue

        raise Exception(f"Post with _id: {self.get_id()} has no field of type Participation" \
                        f"with header {header_of_participation_field}")

    def vote_in_a_poll_field(self, header_of_poll_field, option, user_name):
        for field in self.post_fields_list:
            if field.header == header_of_poll_field:
                if not isinstance(field, fields.Poll):
                    raise Exception(f"Given header name is not a header of a field" \
                                    f"type Poll, it is of type {type(field).__name__()}")
                else:
                    field.vote_for(option, user_name)
                    return field.options
            else:
                continue

        raise Exception(f"Post with _id: {self.get_id()} has no field of type Participation" \
                        f"with header {header_of_poll_field}")

    def cancel_vote_in_a_poll_field(self, header_of_poll_field, option, user_name):
        for field in self.post_fields_list:
            if field.header == header_of_poll_field:
                if not isinstance(field, fields.Poll):
                    raise Exception(f"Given header name is not a header of a field" \
                                    f"type Poll, it is of type {type(field).__name__()}")
                else:
                    field.cancel_vote_for(option, user_name)
                    return field.options
            else:
                continue

        raise Exception(f"Post with _id: {self.get_id()} has no field of type Participation" \
                        f"with header {header_of_poll_field}")

    def to_dict(self):
        dict = {
            "_id": self.get_id(),
            "post_type_id": self.post_type_id,
            "post_owner_user_name": self.post_owner_user_name,
            "post_liked_user_list": self.post_liked_user_list,
            "post_entries_dictionary_list": Post.post_fields_list_to_post_entries_dictionary_list(
                self.post_fields_list),
            "post_discussion_id": self.post_discussion_id,
            "post_creation_time": self.post_creation_time,
            "post_title": self.post_creation_time
        }
        return dict

    def save_to_database(self):
        post_dictionary = self.to_dict()
        post_id = database_utilities.save_post(post_dictionary)
        return post_id

    def update_in_database(self):
        post_dictionary = self.to_dict()
        number_of_updated = database_utilities.update_post(post_dictionary)
        if number_of_updated < 1:
            raise Exception("Nothing could updated.")

        return number_of_updated

    @staticmethod
    def create_post(post_type_id: str,
                    post_owner_user_name: str,
                    post_entries_dictionary_list: list,
                    post_title: str
                    ):

        # TODO: Check if user is eligible to post in the community.

        _id = str(uuid.uuid4())
        post_liked_user_list = []
        post_discussion_id = Discussion.create_new_empty_discussion()["id"]
        post_creation_time = str(datetime.datetime.now())

        new_post = Post(_id,
                        post_type_id,
                        post_owner_user_name,
                        post_liked_user_list,
                        post_entries_dictionary_list,
                        post_discussion_id,
                        post_creation_time,
                        post_title
                        )
        new_post.save_to_database()
        Post.has_created(new_post)
        return new_post

    @staticmethod
    def update_post(post_id: int,
                    post_entries_dictionary_list):
        post = Post.get_post(post_id)
        post.update_post_entries(post_entries_dictionary_list)
        post.update_in_database()
        return post

    @staticmethod
    def delete_existing_post(post_id: int):
        post = Post.get_post(post_id)
        post_type = PostType.get_post_type(post.post_type_id)
        parent_community_id = post_type.parent_community_id

        num_deleted = database_utilities.delete_post(post_id)
        if num_deleted:
            PostType.has_deleted(post.post_type_id, parent_community_id)
            return post_id
        else:
            raise Exception(f"No such post_type with id {post_id} exists.")
        return post_id

    @staticmethod
    def get_post(post_id):
        post_dictionary = database_utilities.get_post(post_id)
        return Post(**post_dictionary)

    @staticmethod
    def post_entries_dictionary_list_to_post_fields_list(post_type_id: str,
                                                         post_entries_dictionary_list: list):
        post_fields_list = []

        # Load the post_type object
        post_type_instance = PostType.get_post_type(post_type_id)
        post_field_info_dictionaries_list = post_type_instance.post_field_info_dictionaries_list

        # All headers of a field is unique. This is ensured by PostType.create_new_post_type func.
        for post_type_dictionary in post_field_info_dictionaries_list:
            field_header = post_type_dictionary["header"]

            post_field_dictionary = next(
                (post_field_dictionary for post_field_dictionary in post_entries_dictionary_list
                 if post_field_dictionary["header"] == field_header), None)

            field_type_name = post_type_dictionary["field_type"]
            # TODO: to make the fields safe differentiate this behaviour for database
            #  loaded Post objects and user created Post objects.
            field_instance = getattr(fields, field_type_name)(**post_field_dictionary)
            post_fields_list.append(field_instance)

        return post_fields_list

    @staticmethod
    def post_fields_list_to_post_entries_dictionary_list(post_fields_list: list):
        post_entries_dictionary_list = []

        for post_field in post_fields_list:
            post_entry_dictionary = fields.to_dict(post_field)
            post_entries_dictionary_list.append(post_entry_dictionary)

        return post_entries_dictionary_list

    @staticmethod
    def has_created(post):
        post_type = PostType.get_post_type(post.post_type_id)

        # Update Community's post list
        community_dictionary = database_utilities.get_community_by_community_id(post_type.parent_community_id)
        community_dictionary["post_history_id_list"].append(post.get_id())
        Community.update_on_database(community_dictionary)

        # Update user's post list
        database_utilities.add_post_to_user_postlist(post.post_owner_user_name, post.get_id())

    @staticmethod
    def has_deleted(post_id, parent_community_id, post_owner_user_name):
        # Carry out the community related updates.
        community_dictionary = database_utilities.get_community_by_community_id(parent_community_id)
        try:
            community_dictionary["post_type_id_list"].remove(post_id)
            database_utilities.remove_post_from_user_postlist(post_owner_user_name, post_id)
        except ValueError:
            raise Exception("No post with given id exists.")
        Community.update_on_database(community_dictionary)

    @staticmethod
    def action_like_post(post_id, user_name):
        post = Post.get_post(post_id)
        post_liked_user_list = post.like(user_name)
        post.update_in_database()
        return post_liked_user_list

    @staticmethod
    def action_unlike_post(post_id, user_name):
        post = Post.get_post(post_id)
        post_liked_user_list = post.unlike(user_name)
        post.update_in_database()
        return post_liked_user_list

    @staticmethod
    def action_vote(post_id, header_of_poll_field, option, voter_user_name):
        post = Post.get_post(post_id)
        options = post.vote_in_a_poll_field(header_of_poll_field,
                                            option,
                                            voter_user_name)
        post.update_in_database()

        return options

    @staticmethod
    def action_cancel_vote(post_id, header_of_poll_field, option, voter_user_name):
        post = Post.get_post(post_id)
        options = post.cancel_vote_in_a_poll_field(header_of_poll_field,
                                                   option,
                                                   voter_user_name)
        post.update_in_database()
        return options

    @staticmethod
    def action_participate(post_id, header_of_participation_field, user_name):
        post = Post.get_post(post_id)
        list_of_participants = post.participate_to_a_participation_field(header_of_participation_field,
                                                                         user_name)
        post.update_in_database()
        return list_of_participants

    @staticmethod
    def action_cancel_participation(post_id, header_of_participation_field, user_name):
        post = Post.get_post(post_id)
        list_of_participants = post.cancel_participation_to_a_participation_field(header_of_participation_field,
                                                                                  user_name)
        post.update_in_database()
        return list_of_participants
