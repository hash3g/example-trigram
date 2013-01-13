#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from markov_chain import MarkovChain


def main(args):

    if not args or len(args) > 1:
        print "usage: gensent.py <letters>"
        exit(1)

    letters = args.pop()

    m = MarkovChain(2, letters=letters)
    m.observe_file('texts/en.txt', True)

    for i in xrange(4):
        start = m.get_random_prestate()
        print m.random_walk_string(10, start)

if __name__ == '__main__':
    main(sys.argv[1:])
