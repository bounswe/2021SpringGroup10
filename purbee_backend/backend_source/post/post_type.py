from .post_fields import PostFields
from ..database.database_utilities import save_post_type,get_post_type_from_post_type_id, update_community
from ..community.community import Community


class PostType:
    def __init__(self, fields_dictionary: dict,
                 post_type_name: str,
                 parent_community_id: int,
                 post_type_id: int,
                 enforce_all_fields_full=False):
        self.post_fields = None
        self.id = None
        self.name = None
        self.parent_community_id = None

        self.update(fields_dictionary,
                    post_type_name,
                    parent_community_id,
                    post_type_id,
                    enforce_all_fields_full)

    def update(self, fields_dictionary: dict,
               post_type_name: str,
               parent_community_id: int,
               post_type_id: int,
               enforce_all_fields_full=False):
        self.id = post_type_id
        self.name = post_type_name
        self.parent_community_id = parent_community_id
        self.post_fields = PostFields(fields_dictionary, enforce_all_fields_full)
        return self

    def to_dict(self):
        return {'id': self.id, "post_fields": self.post_fields.to_dict(),
                'name': self.name, 'parent_community_id': self.parent_community_id}

    def save2database(self):
        post_type_dictionary = self.to_dict()
        save_post_type(post_type_dictionary)

    def has_created(self):
        community = Community.get_community_from_id(self.parent_community_id)
        community.post_type_id_list.append(self.id)
        update_community(community.to_dict())

    @staticmethod
    def get_post_type_from_id(post_type_id):
        #this is a db method in database_utilities.py
        post_type_dictionary = get_post_type_from_post_type_id(post_type_id)
        # do database stuff
        """
        post_type_dictionary = {"fields_dictionary": "",
                                "post_type_name": "",
                                "parent_community_id": "",
                                "post_type_id": ""}
        """
        return PostType(**post_type_dictionary)

    @staticmethod
    def get_post_type_from_dict(post_type_dictionary):
        return PostType(**post_type_dictionary)
