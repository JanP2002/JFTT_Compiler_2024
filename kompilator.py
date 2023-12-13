from parser import parser, lexer
import sys


def read_file(filename):
    with open(filename, "r") as file:
        return file.read()


def write_to_file(filename, data):
    with open(filename, "w") as file:
        file.write(data)


inputFile = sys.argv[1]
outFile = sys.argv[2]
try:
    data = read_file(inputFile)
    print("Compiling file '%s'" % inputFile)
    program = parser.parse(data, lexer, tracking=True)
    output = program.translate()
    write_to_file(outFile, output)
    print("Output file: '%s'" % outFile)
except Exception as err:
    print(err)
    exit(1)