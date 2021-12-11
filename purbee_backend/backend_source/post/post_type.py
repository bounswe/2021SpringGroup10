from .post_fields import PostFields


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
        # TODO: given the PostType object return the corresponding dictionary representation.
        return dict()

    def save2database(self):
        post_type_dictionary = self.to_dict()
        # TODO: save the post_type_dictionary
        pass

    @staticmethod
    def get_post_type_from_id(post_type_id):
        #TODO: implement this method

        # do database stuff
        post_type_dictionary = {"fields_dictionary": "",
                                "post_type_name": "",
                                "parent_community_id": "",
                                "post_type_id": ""}
        return PostType(**post_type_dictionary)


"""
        dic = {"Poll": [{"header": "header"},], "PlainText": [{"header": "header"}]}
"""
