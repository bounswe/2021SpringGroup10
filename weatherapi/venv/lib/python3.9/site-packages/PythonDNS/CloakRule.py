import re

class CloakRule():

    # https://stackoverflow.com/a/25969006/570787
    IPV4_REGEX = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

    def __init__(self, regex, target):
        self.regex = regex
        self.target = target

    def search(self, test):
        return bool(self.regex.search(test))

    def targetIsIp4(self):
        return bool(self.IPV4_REGEX.search(self.target))

    @classmethod
    def importRules(self, file):

        rules = []

        with open(file, 'r') as rdr:
            for line in rdr:

                line = line.strip()

                if len(line) == 0 or line[0] == "#":
                    continue

                parts = line.split(None, 2)

                if len(parts) != 2:
                    continue

                try:
                    rule = self(re.compile(parts[0]), parts[1])
                except re.error:
                    continue

                rules.append(rule)

        return rules