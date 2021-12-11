from .post_type import PostType


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

        self.PostType = updated_post_type

    def has_created(self):
        # TODO: Get community and user objects and update the corresponding lists of them and then save to database.
        # community = Community.get_community_from_id(parent_community_id)
        # self.owner_user_name
        pass

    def to_dict(self):
        pass

    def save2database(self):
        post_dictionary = self.to_dict()
        # TODO: save the community_dictionary
        pass

    @staticmethod
    def get_post_from_id(post_id):
        #TODO: implement this method

        # do database stuff
        post_dictionary = {"fields_dictionary": "",
                                "post_type_name": "",
                                "parent_community_id": "",
                                "post_type_id": ""}
        return Post(**post_dictionary)
