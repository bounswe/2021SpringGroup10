import .fields

POST_FIELD_NAMES = ["PlainText", "Photo", "DateTime", "Document", "Price", "Location", "Poll", "Participation"]


class PostFields:
    def __init__(self, fields_dictionary, enforce_all_fields_full):
        self.plain_text_fields = []
        self.photo_fields = []
        self.poll_fields = []
        self.document_fields = []
        self.participation_fields = []
        self.location_fields = []
        self.date_time_fields = []
        self.price_fields = []

        self.setPostFields(fields_dictionary, enforce_all_fields_full)

    def setPostFields(self, fields_dictionary, enforce_all_fields_full):
        for field_name in fields_dictionary.keys():
            if field_name not in POST_FIELD_NAMES:
                return 1  # Invalid field name, no such field exists.
            for field in fields_dictionary[field_name]:
                try:
                    field_instance = getattr(fields, field_name)(**field)
                except Exception as E:
                    return 2  # Invalid argument name for the field.
            if enforce_all_fields_full:
                if [val for val in [getattr(field_instance, field_name) for
                                    field_name in dir(field_instance)
                                    if not field_name.startswith('_')] if not val]:
                    raise Exception("All fields should be specified")

            getattr(self, (field_name.lower() + "_fields")).append(field_instance)

        return 0
