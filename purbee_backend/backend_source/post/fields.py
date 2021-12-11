# send false for the parameters that you don't want to send
class DateTime:

    def __init__(self, header, date="", time=""):
        self.header = header
        self.date = date
        self.time = time
        return 0

    def update(self, header, date="", time=""):
        if header:
            self.header = header
        if date:
            self.date = date
        if time:
            self.time = time
        return 0


class Location:
    def __init__(self, header, location="", text=""):
        self.header = header
        self.location = location
        self.text = text
        return 0

    def set(self, header, location="", text=""):
        if header:
            self.header = header
        if location:
            self.location = location
        if text:
            self.text = text
        return 0


class PlainText:
    def __init__(self, header="", text=""):
        self.header = header
        self.text = text
        return 0

    def set(self, header, text):
        if header:
            self.header = header
        if text:
            self.text = text
        return 0


class Price:
    # TODO: Update the fields of this class in the class diagram
    def __init__(self, header, amount="", currency=""):
        self.header = header
        self.amount = amount
        self.currency = currency
        return 0

    def set(self, header, amount="", currency=""):
        if header:
            self.header = header
        if amount:
            self.amount = amount
        if currency:
            self.currency = currency
        return 0


class Participation:
    def __init__(self, header):
        self.header = header
        self.listOfParticipants = []
        self.numOfParticipants = 0
        return 0

    def set(self, header):
        self.header = header
        return 0

    def participate(self, user_name):
        self.listOfParticipants = self.listOfParticipants.append(user_name)
        self.numOfParticipants += 1
        return 0

    def cancel_participation(self, user_name):
        self.listOfParticipants = self.listOfParticipants.remove(user_name)
        self.numOfParticipants -= 1
        return 0


class Document:
    def __init__(self, header, url=""):
        self.header = header
        self.url = url
        return 0

    def set(self, header, url=""):
        if header:
            self.header = header
        if url:
            self.url = url
        return 0


class Photo:
    def __init__(self, header, image=""):
        self.header = header
        self.image = image
        return 0

    def set(self, header, image=""):
        if header:
            self.header = header
        if image:
            self.image = image

        return 0


class Poll:
    # TODO: update the class diagram fields accordingly
    def __init__(self, header, options=""):
        self.header = header
        self.options = {option: [] for option in options}

    def vote_for(self, option, user_name):
        self.options[option].append(user_name)

    def cancel_vote_for(self, option, user_name):
        self.options[option].remove(user_name)
