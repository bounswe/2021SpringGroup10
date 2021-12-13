from .post_type import PostType
from community.community import Community
from database.database_utilities import (
    update_community,
    add_post_to_user_postlist,
    save_a_new_post,
    get_post_from_post_id)


class Post:
    def __init__(self, base_post_type: PostType,
                 fields_dictionary: dict,
                 post_id: int,
                 post_owner_user_name: str):
        self.id = None
        self.base_post_type = None
        self.owner_user_name = None

        self.update(base_post_type, fields_dictionary, post_id, post_owner_user_name)

    def update(self,
               base_post_type: PostType,
               fields_dictionary: dict,
               post_id: int,
               post_owner_user_name: str):
        self.id = post_id
        self.owner_user_name = post_owner_user_name

        updated_post_type = base_post_type.update(fields_dictionary, enforce_all_fields_full=True)

        self.base_post_type = updated_post_type

    def has_created(self):
        community = Community.get_community_from_id(self.parent_community_id)
        community.post_id_list.append(self.id)
        update_community(community.to_dict())
        add_post_to_user_postlist(self.owner_user_name, self.post_id)

    def to_dict(self):
        return {'id': self.id, 'base_post_type': self.base_post_type.to_dict(),
                'owner_user_name': self.owner_user_name}

    def save2database(self):
        post_dictionary = self.to_dict()
        save_a_new_post(post_dictionary)

    @staticmethod
    def get_post_from_id(post_id):
        """ post_dictionary = {"base_post_type": PostType,
                         "fields_dictionary": dict,
                         "post_id": int,
                         "post_owner_user_name": str}
                         """

        # this is a db method
        post_dictionary = get_post_from_post_id(post_id)
        post_type_dictionary = post_dictionary["base_post_type"]
        base_post_type = PostType(post_type_dictionary["post_fields"],
                                  post_type_dictionary["name"],
                                  post_type_dictionary["parent_community_id"],
                                  post_type_dictionary["id"])

        return Post(base_post_type,
                    post_type_dictionary["post_fields"],
                    post_dictionary["post_id"],
                    post_dictionary["post_owner_user_name"])
