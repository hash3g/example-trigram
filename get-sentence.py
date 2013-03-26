import sys
import StringIO

from grammar.contextfree import ContextFreeReader, NotFoundSentence
from grammar.wordnet import getlemmas


if __name__ == '__main__':
    args = sys.argv[1:]

    if not args or len(args) > 1:
        print "usage: gen-sentence.py <letters>"
        exit(1)

    letters = args.pop()

    cfree = ContextFreeReader(letters)
    cfree.clause_from_file(open("data/test.clauses"))
    cfree.parse_from_file(StringIO.StringIO(getlemmas(letters)))
    try:
        expansion = cfree.get_expansion('S')
        print ' '.join(expansion)
    except NotFoundSentence:
        print 'Unable to find sentences with %s letters' % letters
