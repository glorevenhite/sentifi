__author__ = 'duy.do@sentifi.com, vinh.vo@sentifi.com'

import shlex
import re

NOT = '^'
OR = '|'


def match(query, text):
    pieces = shlex.split(unicode(query).encode('utf-8').lower())
    include, or_include, not_include = [], [], []
    for piece in pieces:
        if piece.startswith(NOT):
            not_include.append(re.compile(piece[1:]))
        elif piece.startswith(OR):
            or_include.append(re.compile(piece[1:]))
        else:
            include.append(re.compile(piece))

    s = text.lower()
    print s.split()
    for r in include:
        print r.pattern.lower()
    print all(r.search(s) for r in include)
    #for r in not_include:
        #print r.pattern.lower()


    return (
        (
            all(r.search(s)for r in include)
            and not any(r.search(s) in s.split() for r in not_include)
        ) or any(r.search(s) in s.split() for r in or_include)
    )


if __name__ == "__main__":
    rule = 'ABB falling'
    s = 'ABB is falling down'
    print match(rule, s)    # true

    rule = 'ABB |$ABB |#ABB ^falling'
    s = 'ABB is falling down'
    print match(rule, s)    # false

    rule = 'equity analyst'
    s = 'i am an equity analyst sell side'
    print match(rule, s)    # true

    rule = '^our ^we ^provider'
    s = 'i am journalist '
    print match(rule, s)    # true

    rule = 'journalist'
    s = ' i am a journalist'
    print match(rule, s)    # true

