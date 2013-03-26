import sys

from grammar.wordnet import getlemmas


if __name__ == '__main__':
    args = sys.argv[1:]

    if not args or len(args) > 1:
        print "usage: gen-sentence.py <letters>"
        exit(1)

    letters = args.pop()

    print getlemmas(letters)
