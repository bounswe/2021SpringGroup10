class Community:
    def __init__(self, community_dict):
        self.id = None
        self.next_post_type_id = None
        self.admin_list = None
        self.subscriber_list = None
        self.post_type_id_list = None
        
        self.update(community_dict)

    def update(self, community_dict):
        for community_field_name, community_field_value in community_dict.items():
            setattr(self, community_field_name, community_field_value)

    def to_dict(self):
        # TODO: given the Community object return the corresponding dictionary representation.
        return dict()

    def save2database(self):
        community_dictionary = self.to_dict()
        # TODO: save the community_dictionary
        pass

    @staticmethod
    def get_community_from_id(community_id):
        # do database stuff
        community_dict = {}
        return Community(community_dict)

