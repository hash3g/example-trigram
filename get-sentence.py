import re
import sys

from random import choice


class ContextFree(object):

    def __init__(self):
        self.rules = dict()
        self.expansion = list()

    # rules are stored in self.rules, a dictionary; the rules themselves are
    # lists of expansions (which themselves are lists)
    def add_rule(self, rule, expansion):
        if rule in self.rules:
            self.rules[rule].append(expansion)
        else:
            self.rules[rule] = [expansion]

    def expand(self, start):
        # if the starting rule was in our set of rules, then we can expand it
        if start in self.rules:
            possible_expansions = self.rules[start]
            # grab one possible expansion
            random_expansion = choice(possible_expansions)
            # call this method again with the current element of the expansion
            for elem in random_expansion:
                self.expand(elem)
        else:
            # if the rule wasn't found, then it's a terminal: simply append the
            # string to the expansion
            self.expansion.append(start)

    # utility method to run the expand method and return the results
    def get_expansion(self, axiom):
        self.filter_with_available_letters(axiom)
        self.expand(axiom)
        return self.expansion


class ContextFreeReader(ContextFree):

    def __init__(self, letters):
        self.letters = letters
        super(ContextFreeReader, self).__init__()

    def filter_with_available_letters(self, axiom):
        result = []
        for s in self.rules[axiom]:
            if set(s).difference(set(self.list_rules)):
                continue
            result.append(s)
        self.rules[axiom] = result

    def clause_from_file(self, file_obj):
        for line in file_obj:
            line = re.sub(r"#.*$", "", line)  # get rid of comments
            line = line.strip()  # strip any remaining white space
            match_obj = re.search(r"(\w+) *-> *(.*)", line)
            if match_obj:
                rule = match_obj.group(1)
                expansions = re.split(r"\s*\|\s*", match_obj.group(2))
                for expansion in expansions:
                    expansion_list = expansion.split(" ")
                    self.add_rule(rule, expansion_list)

    def parse_from_file(self, file_obj):
        # rules are stored in the given file in the following format:
        # Rule -> a | a b c | b c d
        # ... which will be translated to:
        # self.add_rule('Rule', ['a'])
        # self.add_rule('Rule', ['a', 'b', 'c'])
        # self.add_rule('Rule', ['b', 'c', 'd'])

        self.list_rules = []
        for line in file_obj:
            line = re.sub(r"#.*$", "", line)  # get rid of comments
            line = line.strip()  # strip any remaining white space
            match_obj = re.search(r"(\w+) *-> *(.*)", line)
            if match_obj:
                rule = match_obj.group(1)
                expansions = re.split(r"\s*\|\s*", match_obj.group(2))
                for expansion in expansions:
                    if set(expansion).difference(self.letters):
                        continue
                    if rule not in self.list_rules:
                        self.list_rules.append(rule)
                    expansion_list = expansion.split(" ")
                    self.add_rule(rule, expansion_list)

if __name__ == '__main__':
    args = sys.argv[1:]

    if not args or len(args) > 1:
        print "usage: gensent.py <letters>"
        exit(1)

    letters = args.pop()

    cfree = ContextFreeReader(letters)
    cfree.clause_from_file(open("test.clauses"))
    cfree.parse_from_file(open("test.grammar"))
    expansion = cfree.get_expansion('S')
    print ' '.join(expansion)
