#!/usr/bin/python3

"""
Um mapeador para contar palavras que usa iteradores e geradores para eficiência de memória, bem como define várias funções auxiliares.
"""

import sys

class Mapper(object):

    def __init__(self, infile=sys.stdin, separator='\t'):
        self.infile = infile
        self.sep    = separator

    def emit(self, key, value):
        sys.stdout.write("%s%s%s\n" % (key, self.sep, value))

    def map(self):
        for line in self:
            for word in line.split():
                self.emit(word, 1)

    def __iter__(self):
        for line in self.infile:
            yield line

if __name__ == "__main__":
    mapper = Mapper()
    mapper.map()
