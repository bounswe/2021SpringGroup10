
# send false for the parameters that you don't want to send
class date_time:

    def __init__(self, header, date, time):
        if header:
            self.header = header
        if date:
            self.date = date
        if time:
            self.time = time
        return 0

    def update_field(self, header, date, time):
        if header:
            self.header = header
        if date:
            self.date = date
        if time:
            self.time = time
        return 0

class Location:
    def __init__(self, header, location, description):
        if header:
            self.header = header
        if location:
            self.location = location
        if description:
            self.description = description
        return 0

    def update_field(self, header, location, description):
        if header:
            self.header = header
        if location:
            self.location = location
        if description:
            self.description = description
        return 0

class PlainText:
    def __init__(self, header, text):
        if header:
            self.header = header
        if text:
            self.text = text
        return 0

    def update_field(self, header, text):
        if header:
            self.header = header
        if text:
            self.text = text
        return 0

class Price:
    def __init__(self, header, description):
        if header:
            self.header = header
        if description:
            self.description = description
        return 0

    def update_field(self, header, description):
        if header:
            self.header = header
        if description:
            self.description = description
        return 0

class Participation:
    def __init__(self, header, listOfParticipants , numOfParticipants):
        if header:
            self.header = header
            self.listOfParticipants = []
        if numOfParticipants:
            self.numOfParticipants = numOfParticipants

        return 0


    def set_header(self,header):
        self.header = header
        return 0

    def participate(self, user):
        self.listOfParticipants = self.listOfParticipants.append(user)
        self.numOfParticipants += 1

        return 0

    def cancel_participation(self, user):
        self.listOfParticipants = self.listOfParticipants.remove(user)
        self.numOfParticipants -= 1

        return 0

class Document:
    def __init__(self, header, url, name):
        if header:
            self.header = header
        if url:
            self.text = url
        if name:
            self.name = name
        return 0

    def update_field(self, header, url, name):
        if header:
            self.header = header
        if url:
            self.text = url
        if name:
            self.name = name
        return 0

class Photo:
    def __init__(self, header, image, description):
        if header:
            self.header = header
        if image:
            self.image = image
        if description:
            self.description = description
        return 0

    def update_field(self, header, image, description):
        if header:
            self.header = header
        if image:
            self.image = image
        if description:
            self.description = description
        return 0

## Poll class will be implemented



































