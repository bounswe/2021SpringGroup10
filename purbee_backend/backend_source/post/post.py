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
        self.post_id = None
        self.base_post_type = None
        self.post_owner_user_name = None

        self.update(base_post_type, fields_dictionary, post_id, post_owner_user_name)

    def update(self,
               base_post_type: PostType,
               fields_dictionary: dict,
               post_id: int,
               post_owner_user_name: str):
        self.post_id = post_id
        self.post_owner_user_name = post_owner_user_name

        updated_post_type = base_post_type.update(fields_dictionary, enforce_all_fields_full=True)

        self.base_post_type = updated_post_type

    def has_created(self):
        community = Community.get_community_from_id(self.base_post_type.parent_community_id)
        community.post_history_id_list.append(self.post_id)
        update_community(community.to_dict())
        add_post_to_user_postlist(self.post_owner_user_name, self.post_id)

    def to_dict(self):
        return {'post_id': self.post_id, 'base_post_type': self.base_post_type.to_dict(),
                'post_owner_user_name': self.post_owner_user_name}

    def save2database(self):
        post_dictionary = self.to_dict()
        print("post_dict", post_dictionary)
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
        base_post_type = PostType(post_type_dictionary["fields_dictionary"],
                                  post_type_dictionary["post_type_name"],
                                  post_type_dictionary["parent_community_id"],
                                  post_type_dictionary["post_type_id"])

        return Post(base_post_type,
                    post_type_dictionary["fields_dictionary"],
                    post_dictionary["post_id"],
                    post_dictionary["post_owner_user_name"])
