class Community:
    def __init__(self, community_dict):
        self.id = None
        self.next_post_type_id = None
        self.update(community_dict)
        self.admin_list = None
        self.subscriber_list = None

    def update(self, community_dict):
        for community_field_name, community_field_value in community_dict.items():
            setattr(self, community_field_name, community_field_value)

    @staticmethod
    def get_community_dict(community_id):
        #do database stuff
        community_dict = {}
        return community_dict
