from .post_fields import PostFields


class PostType:
    def __init__(self, fields_dictionary: dict, post_type_name: str, parent_community_id: int, post_type_id: int):
        self.post_fields = PostFields(fields_dictionary)
        self.id = post_type_id
        self.name = post_type_name
        self.parent_community_id = parent_community_id

"""
        dic = {"Poll": [{"header": "header"},], "PlainText": [{"header": "header"}]}
"""
