# send false for the parameters that you don't want to send

def to_dict(self):
    # TODO: remove callable filter, since we have removed update methods.
    return {field_name: getattr(self, field_name) for field_name in dir(self)
            if not field_name.startswith('_') if not callable(getattr(self, field_name))}


class DateTime:
    def __init__(self, header, date="", time=""):
        self.header = header
        self.date = date
        self.time = time


class Location:
    def __init__(self, header, location="", text=""):
        self.header = header
        self.location = location
        self.text = text


class PlainText:
    def __init__(self, header="", text=""):
        self.header = header
        self.text = text


class Price:
    # TODO: Update the fields of this class in the class diagram
    def __init__(self, header, amount="", currency=""):
        self.header = header
        self.amount = amount
        self.currency = currency


class Participation:
    def __init__(self, header, listOfParticipants=[], numOfParticipants=0):
        self.header = header
        self.listOfParticipants = listOfParticipants
        self.numOfParticipants = numOfParticipants

    def participate(self, user_name):
        self.listOfParticipants = self.listOfParticipants.append(user_name)
        self.numOfParticipants += 1

    def cancel_participation(self, user_name):
        self.listOfParticipants = self.listOfParticipants.remove(user_name)
        self.numOfParticipants -= 1


class Document:
    def __init__(self, header, url=""):
        self.header = header
        self.url = url


class Photo:
    def __init__(self, header, image=""):
        self.header = header
        self.image = image


class Poll:
    # TODO: update the class diagram fields accordingly
    def __init__(self, header, options=""):
        self.header = header
        self.options = {option: [] for option in options}

    def vote_for(self, option, user_name):
        self.options[option].append(user_name)

    def cancel_vote_for(self, option, user_name):
        self.options[option].remove(user_name)
