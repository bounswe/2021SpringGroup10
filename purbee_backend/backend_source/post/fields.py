# send false for the parameters that you don't want to send

def to_dict(self):
    # TODO: remove callable filter, since we have removed update methods.
    return {field_name: getattr(self, field_name) for field_name in dir(self)
            if not field_name.startswith('_') if not callable(getattr(self, field_name))}


class DateTime:
    def __init__(self, header, date, time):
        self.header = header
        self.date = date
        self.time = time


class Location:
    def __init__(self, header, location, text):
        self.header = header
        self.location = location
        self.text = text


class PlainText:
    def __init__(self, header, text):
        self.header = header
        self.text = text


class Price:
    def __init__(self, header, amount, currency):
        self.header = header
        self.amount = amount
        self.currency = currency


class Participation:
    def __init__(self, header, list_of_participants=[]):
        self.header = header
        self.list_of_participants = list_of_participants

    def participate(self, user_name):
        if user_name in self.list_of_participants:
            raise Exception(f"User with {user_name} has already been marked as participating to the Participation"
                            f"field with header {self.header}")
        else:
            self.list_of_participants.append(user_name)

    def cancel_participation(self, user_name):
        try:
            self.list_of_participants.remove(user_name)
        except ValueError:
            raise Exception(f"User with user_name {user_name}, has already not been marked as participating, to the" \
                            f"Participation field with the header {self.header}.")


class Document:
    def __init__(self, header, url):
        self.header = header
        self.url = url


class Photo:
    def __init__(self, header, image):
        self.header = header
        self.image = image


class Poll:
    def __init__(self, header, options, can_vote_for_n_many_options):
        self.header = header

        if not isinstance(can_vote_for_n_many_options, int) or can_vote_for_n_many_options < 1:
            raise Exception(f"The argument can_vote_for_n_many_options can not be lower than 1.")
        else:
            self.can_vote_for_n_many_options = can_vote_for_n_many_options

        if isinstance(options, list):
            self.options = {option: [] for option in options}
        elif isinstance(options, dict):
            self.options = options

    def vote_for(self, option, user_name):
        if option not in self.options.keys():
            raise Exception(f"No such option as: {option} exists in the options " \
                            f"of the Poll field with header {self.header}")

        number_of_votes_of_user = 1
        for option_list in self.options.values():
            if user_name in option_list:
                number_of_votes_of_user = number_of_votes_of_user + 1
        if number_of_votes_of_user > self.can_vote_for_n_many_options:
            raise Exception(f"User with {user_name} has already voted for {number_of_votes_of_user - 1}" \
                            f" many options (which is the limit) " \
                            f"in the Poll field with header {self.header}")

        if user_name in self.options[option]:
            raise Exception(f"User with {user_name} has already voted for option: {option}, in the" \
                            f"Poll field with header {self.header}")
        else:
            self.options[option].append(user_name)

    def cancel_vote_for(self, option, user_name):
        if option not in self.options.keys():
            raise Exception(f"No such option as: {option} exists in the options " \
                            f"of the Poll field with header {self.header}")

        try:
            self.options[option].remove(user_name)
            return self.options
        except ValueError:
            raise Exception(f"User with user_name {user_name}, has already not voted for option: {option}, in the " \
                            f"Poll field with the header {self.header}.")

        self.options[option].remove(user_name)
