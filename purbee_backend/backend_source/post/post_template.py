from community.community import Community
from database.database_utilities import (
    get_post_type_from_post_type_id,
    update_community,
    save_post_template
)
from . import fields

class PostTemplate:
    def __init__(self,
                 post_type_id,
                 post_type_name,
                 post_type_parent_community_id,
                 post_type_fields_dict
                 ):

        self.post_type_id = None
        self.post_type_name = None
        self.post_type_parent_community_id = None
        self.post_type_fields = None

        self.update(post_type_id,
                    post_type_name,
                    post_type_parent_community_id,
                    post_type_fields_dict)

    def update(self,
               post_type_id,
               post_type_name,
               post_type_parent_community_id,
               post_type_fields_dict):

        self.post_type_id = post_type_id
        self.post_type_name = post_type_name
        self.post_type_parent_community_id = post_type_parent_community_id

        post_type_fields = {}
        for field_type_name in post_type_fields_dict.keys():
            field_type_list = []
            for field_type_dict in post_type_fields_dict[field_type_name]:
                header = field_type_dict["header"]
                field_type_list.append({"header": header, "field_type": getattr(fields, field_type_name)})
            post_type_fields[field_type_name] = field_type_list
        self.post_type_fields = post_type_fields

    def to_dict(self):
        post_type_fields_dict = {}
        for field_type_name in post_type_fields_dict.keys():
            field_type_list = []
            for field_type_dict in post_type_fields_dict[field_type_name]:
                header = field_type_dict["header"]
                field_type = field_type_dict["field_type"]
                field_type_list.append({"header": header, "field_type_name": type(field_type).__name__()})
            post_type_fields_dict[field_type_name] = field_type_list

        return {"post_type_id": self.post_type_id,
                "post_type_name": self.post_type_name,
                "post_type_parent_community_id": self.post_type_parent_community_id,
                "post_type_fields_dict": post_type_fields_dict
                }

    def save2database(self):
        post_template_dictionary = self.to_dict()
        save_post_template(post_template_dictionary)

    def has_created(self):
        community = Community.get_community_from_id(self.parent_community_id)
        community.post_type_id_list.append(self.id)
        update_community(community.to_dict())

    @staticmethod
    def get_post_type_from_id(post_type_id):
        # this is a db method in database_utilities.py
        post_type_dictionary = get_post_type_from_post_type_id(post_type_id)
        """
        post_type_dictionary = {"header": "",
                                "post_type_name": "",
                                "parent_community_id": "",
                                "post_type_id": ""}
        """
        return PostTemplate(**post_type_dictionary)
