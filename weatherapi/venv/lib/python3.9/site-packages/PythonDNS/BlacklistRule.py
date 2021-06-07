import re

class BlacklistRule():

    def __init__(self, regex):
        self.regex = regex

    def search(self, test):
        return bool(self.regex.search(test))

    @classmethod
    def importRules(self, file):

        rules = []

        with open(file, 'r') as rdr:
            for line in rdr:

                line = line.strip()

                if len(line) == 0 or line[0] == "#":
                    continue

                try:
                    rule = self(re.compile(line))
                except re.error:
                    continue

                rules.append(rule)

        return rules