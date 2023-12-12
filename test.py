from ply import lex, yacc
import sys
import lexer
import parser




if len(sys.argv) >= 3:
    file1 = open(sys.argv[1], "r")
    s = file1.read()
    print(s)
    file1.close()
    file2 = open(sys.argv[2], "w")
    file2.write("test")
    file2.close()
    lexer = lex.lex(lexer)
    parser = yacc.yacc(parser)
    # parser.parse(s, lexer)
else:
    print("Blad: brak parametrow")
