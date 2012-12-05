#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys

import random
from collections import defaultdict

r_alphabet = re.compile(u'[a-zA-Zа-яА-Я0-9-]+|[.,:;?!]+')


def gen_lines(corpus):
    data = open(corpus)
    for line in data:
        yield line.decode('utf-8').lower()


def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$', '$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2


def train(corpus):
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.iteritems():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq / bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq / bi[t0, t1])]
    return model


def generate_sentence(model):
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, random.choice(model[t0, t1])
        if t1 == '$':
            break
        if t1 in ('.!?,;:', ) or t0 == '$':
            phrase += t1[0]
        else:
            phrase += ' ' + t1[0]
    return phrase.capitalize()


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

    model = train('dickens.txt')
    print generate_sentence(model)

if __name__ == '__main__':
    main(sys.argv[1:])
