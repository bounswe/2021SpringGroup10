from ..post.fields import PlainText
from ..post import fields
import re


POST_FIELD_NAMES = ["PlainText", "Photo", "DateTime", "Document", "Price", "Location", "Poll", "Participation"]


class PostFields:
    def __init__(self, post_fields_dictionary, enforce_all_fields_full):
        self.plain_text_fields = []
        self.photo_fields = []
        self.poll_fields = []
        self.document_fields = []
        self.participation_fields = []
        self.location_fields = []
        self.date_time_fields = []
        self.price_fields = []

        self.set_post_fields(post_fields_dictionary, enforce_all_fields_full)

    def set_post_fields(self, post_fields_dictionary, enforce_all_fields_full):
        print(post_fields_dictionary)
        for field_name in post_fields_dictionary.keys():
            if field_name not in POST_FIELD_NAMES:
                return 1  # Invalid field name, no such field exists.
            for field in post_fields_dictionary[field_name]:
                try:
                    field_instance = getattr(fields, field_name)(**field)
                   #"PlainText", "Photo", "DateTime", "Document", "Price", "Location", "Poll", "Participation"
                except Exception as E:
                    print(field_name)
                    if field_name=="PlainText":
                        field_instance = PlainText(**field)
                    return 2  # Invalid argument name for the field.
            if enforce_all_fields_full:
                if [val for val in [getattr(field_instance, field_name) for
                                    field_name in dir(field_instance)
                                    if not field_name.startswith('_')] if not val]:
                    raise Exception("All fields should be specified")
            actual_name = "_".join([i.lower() for i in re.findall('[A-Z][^A-Z]*', field_name)]) + "_fields"
            getattr(self, actual_name).append(field_instance)

        return 0

    def to_dict(self):
        result_dict = {}
        for field_name in dir(self):
            #print(field_name)
            if not (field_name.startswith('_') or field_name == "set_post_fields" or field_name == "to_dict" ):
                field_list = getattr(self, field_name)
                actual_field_name = "".join([i.capitalize() for i in field_name.replace("_fields","").split("_")])
                field_type_list = []
                for field_instance in field_list:
                    field_type_list.append(fields.to_dict(field_instance))
                result_dict[actual_field_name]= field_type_list
        return result_dict
