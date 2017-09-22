import getopt
import sys

class MCQToken:
    TYPE_MCQ_TITLE = 0
    TYPE_QNAME = 1
    TYPE_QANSWER = 2
    TYPE_EOF = -1

    def __init__(self, type_token, representation):
        self.type = type_token
        self.representation = representation

    def print(self):
        print('[' + str(self.type) + ': ' + self.representation + ']')


class MCQLexer:
    def __init__(self, filename):
        self.inputfile = open(filename, encoding="utf8")
        self.line = self.inputfile.readline(1000000)
        self.position = 0

    def step(self) -> bool:
        if self.line == '':
            return False
        if self.position == len(self.line):
            self.line = self.inputfile.readline(1000000)
            if self.line == '':
                return False
            self.position = 0
            self.step()
        c = self.line[self.position]
        # passer les espaces
        if not (c == ' ' or c == '\t' or c == '\r' or c == '\n'):
            return True
        self.position += 1
        return self.step()

    def next(self) -> MCQToken:
        if not (self.step()):
            return MCQToken(MCQToken.TYPE_EOF, "")
        c = self.line[self.position]


    def estBaliseOuvrante(self, jeton) -> bool:
        return jeton.type == Jeton.TYPE_BALISE_OUVRANTE



class MCQMaster:
    def __init__(self, file):
        f = open(file)
        print(f.readlines())


def main(argv):
    usage = 'usage: MCQMaster.py -f <MCQ file>'
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-f", "--file"):
            m = MCQMaster(arg)


if __name__ == "__main__":
    main(sys.argv[1:])