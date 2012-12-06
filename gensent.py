#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import markov


def main(args):

    if not args or len(args) > 1:
        print "usage: gensent.py <letters>"
        exit(1)

    letters = args.pop()

    p = markov.Markov(length=10, letters=letters)
    print p._run()

if __name__ == '__main__':
    main(sys.argv[1:])
