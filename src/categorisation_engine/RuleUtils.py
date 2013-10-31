__author__ = 'duydo'

import shlex
import re

NOT = '-'
OR = '|'


def match(query, text):
    pieces = shlex.split(query.lower())
    include, or_include, not_include = [], [], []
    for piece in pieces:
        if piece.startswith(NOT):
            not_include.append(re.compile(piece[1:]))
        elif piece.startswith(OR):
            or_include.append(re.compile(piece[1:]))
        else:
            include.append(re.compile(piece))

    s = text.lower()
    return (
        (
            all(r.search(s) for r in include)
            and not any(r.search(s) for r in not_include)
        ) or any(r.search(s) for r in or_include)
    )

if __name__ == "__main__":
    rule = 'ABB ABBB'
    s = 'ABB is falling down'
    print match(rule, s)    # true

    rule = 'ABB |$ABB |#ABB -falling'
    s = 'ABB is falling down'
    print match(rule, s)    # false

    rule = 'financial analyst'
    s = 'i am financial analyst'
    print match(rule, s)
