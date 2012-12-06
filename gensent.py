#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys

import markov


def main(args):

    if not args or len(args) > 1:
        print "usage: gensent.py <letters>"
        exit(1)

    letters = args.pop()

    fp = open('/usr/share/dict/words', 'r')
    words = fp.read()
    fp.close()

    sourcewords = []
    map(sourcewords.append, re.findall(ur'^[{0}]*$'.format(re.escape(letters)), words, re.I | re.M))

    p = markov.Markov(length=10)
    print p._run()

if __name__ == '__main__':
    main(sys.argv[1:])
