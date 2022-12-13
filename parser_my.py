from lexema import Lexema
from lexema import tableOfSymb


class Parser:
    def __init__(self, name):
        self.numRow = 1
        lex = Lexema(name)
        lex.lex()
        print('-' * 30)
        print('tableOfSymb:{0}'.format(tableOfSymb))
        print('-' * 30)
        # довжина таблиці символів програми
        # він же - номер останнього запису
        self.len_tableOfSymb = len(tableOfSymb)
        print(('len_tableOfSymb', self.len_tableOfSymb))

    def getSymb(self):
        if self.numRow > self.len_tableOfSymb:
            self.failParse('getSymb(): неочікуваний кінець програми', self.numRow)
        # таблиця розбору реалізована у формі словника (dictionary)
        # tableOfSymb[numRow]={numRow: (numLine, lexeme, token, indexOfVarOrConst)
        numLine, lexeme, token, _ = tableOfSymb[self.numRow]
        return numLine, lexeme, token

    def failParse(self, str, tuple):
        if str == 'неочікуваний кінець програми':
            if len(tuple) == 3:
                (lexeme, token, numRow) = tuple
                print(
                'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format(
                    (lexeme, token), numRow))
            else:
                (token, numRow) = tuple
                print(
                    'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(
                        numRow, token))

            exit(1001)
        if str == 'getSymb(): неочікуваний кінець програми':
            numRow = tuple
            print(
                'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(
                    numRow, tableOfSymb[numRow-1]))
            exit(1002)

        elif str == 'невідповідність токенів':
            (numLine, lexeme, token, lex, tok) = tuple
            print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - ({3},{4}).'.format(
                numLine, lexeme, token, lex, tok))
            exit(1)

        elif str == 'невідповідність інструкцій':
            (numLine, lex, tok, expected) = tuple
            print(
                'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,
                                                                                                               lex,
                                                                                                               tok,
                                                                                                               expected))
            exit(2)
        elif str == 'невідповідність у Expression.Factor':
            (numLine, lex, tok, expected) = tuple
            print(
                'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,
                                                                                                               lex,
                                                                                                               tok,
                                                                                                               expected))
            exit(3)

        elif str =='невідповідність в IdentList':
            (numLine, lex, tok, expected) = tuple
            print(
                'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,
                                                                                                               lex,
                                                                                                               tok,
                                                                                                               expected))
            exit(4)
        elif str == 'невідповідність у BoolExpr':
            (numLine, lex, tok, expected) = tuple
            print(
                'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,
                                                                                                               lex,
                                                                                                               tok,
                                                                                                               expected))
            exit(5)
        elif str == 'відсутній StatementList':
            print('Parser ERROR: \n\t В програмі очікувався хоча б один Statement')
            exit(6)

    def parseLexToken(self, lexeme, token, indent):
        if self.numRow > self.len_tableOfSymb:
            self.failParse('неочікуваний кінець програми', (lexeme, token, self.numRow))
        numLine, lex, tok = self.getSymb()

        self.numRow += 1

        if (lex, tok) == (lexeme, token):
            # вивести у консоль номер рядка програми та лексему і токен
            print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lexeme, token)))
            return True
        else:
            self.failParse('невідповідність токенів', (numLine, lex, tok, lexeme, token))
            return False

    def parseToken(self, token, indent):
        if self.numRow > self.len_tableOfSymb:
            self.failParse('неочікуваний кінець програми', (token,  self.numRow))

        numLine, lex, tok = self.getSymb()

        # тепер поточним буде наступний рядок таблиці розбору
        self.numRow += 1

        # чи збігаються лексема та токен таблиці розбору з заданими
        if tok == token:
            # вивести у консоль номер рядка програми та лексему і токен
            print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine,  token))
            return True
        else:
            self.numRow -= 1
            return False

    def parseProgram(self):
        try:
            self.parseDeclarList()
            self.parseStatemetList()
            print('Parser: Синтаксичний аналіз завершився успішно')
            return True
        except SystemExit as e:
            print('Parser: Аварійне завершення програми з кодом {0}'.format(e))

    def parseDeclarList(self):
        print("parseDeclarList():")
        numTabs = 1
        while self.parseDeclaration(numTabs):
            pass
        return True

    def parseDeclaration(self, numTabs):
        if self.numRow >= self.len_tableOfSymb:
            return False
        print('\t'*numTabs+'parseDeclaration:')
        numTabs+=1
        if self.parseType(numTabs):
            self.parseIdentList(numTabs)
            self.parseLexToken(";", "punct", '\t' * numTabs)
            return True
        else:
            return False

    def parseType(self, numTabs):
        print("\t"*numTabs +"parseType():")
        numTabs += 1
        numLine, lex, token = self.getSymb()
        if lex in ['int', 'real', 'bool'] and token == "keyword":
            self.numRow += 1
            print("\t"*numTabs+'в рядку {0} - {1}'.format(numLine, (lex, token)))
            return True
        else:
            return False
        #     self.failParse("невідповідність в Type", (numLine, lex, token, 'int | real | bool'))
        # return True

    def parseIdentList(self, numTabs):
        print("\t"*numTabs+"parseIdentList():")
        numTabs += 1
        if not self.parseToken("ident", '\t' * numTabs):
            numLine, lex, token = self.getSymb()
            self.failParse('невідповідність в IdentList', (numLine, lex, token, 'ident'))
            return False
        while self.getSymb()[1] == "," and self.getSymb()[2] == "punct":
            self.parseLexToken(",", "punct", "\t" * numTabs)
            if not self.parseToken("ident", '\t' * numTabs):
                numLine, lex, token = self.getSymb()
                self.failParse('невідповідність в IdentList', (numLine, lex, token, 'ident'))
                return False
        return True

    def parseStatemetList(self, numTabs=0):
        if self.numRow >= self.len_tableOfSymb:
            self.failParse("відсутній StatementList", ())
        print("\t"*numTabs+"parseStatementList():")
        numTabs += 1
        self.parseStatement(numTabs)
        while self.parseStatement(numTabs):
            pass
        return True

    def parseStatement(self, numTabs):
        if self.numRow >= self.len_tableOfSymb:
            return False
        print("\t"*numTabs+'parseStatement():')
        numTabs += 1
        # прочитаємо поточну лексему в таблиці розбору
        numLine, lex, token = self.getSymb()

        if token == 'ident':
            self.parseAssign(numTabs)
            return True
        elif token == "keyword" and lex == "read":
            self.parseRead(numTabs)
            return True
        elif token == "keyword" and lex == "write":
            self.parseWrite(numTabs)
            return True
        elif (lex, token) == ('for', 'keyword'):
            self.parseFor(numTabs)
            return True
        # якщо лексема - ключове слово 'if'
        # обробити інструкцію розгалудження
        elif (lex, token) == ('if', 'keyword'):
            self.parseIf(numTabs)
            return True
        elif token == 'mark':
            self.parseToken("mark", "\t" * numTabs)
            return True
        elif lex == 'end' and numTabs>3:
            return False
        else:
            self.failParse('невідповідність інструкцій', (numLine, lex, token, 'ident, read, write, for, if or mark'))

    def parseAssign(self, numTabs):
        print("\t"*numTabs+"parseAssign():")
        numTabs += 1
        self.parseToken("ident", "\t" * numTabs)
        self.parseLexToken("=", "assign_op", "\t" * numTabs)
        self.parseExpression(numTabs)
        self.parseLexToken(";", "punct", "\t" * numTabs)

    def parseArithmExpression(self, numTabs):
        print("\t"*numTabs+"parseArithExpression():")
        numTabs += 1
        self.parseToken("add_op", "\t" * numTabs)
        # self.parseTokenIdent("add_op", "\t")

        if not self.parseTerm(numTabs):
            return False
        while self.parseToken("add_op", "\t" * numTabs) and self.parseTerm(numTabs):
            pass
        return True

    def parseTerm(self, numTabs):
        print("\t"*numTabs+"parseTerm():")
        numTabs +=1
        if not self.parseFactor(numTabs):
            return False

        while (self.parseToken("mult_op", "\t" * numTabs) or self.parseToken("pow_op", "\t" * numTabs)) and self.parseFactor(numTabs):
            pass
        return True

    def parseFactor(self, numTabs):
        print("\t"*numTabs+"parseFactor():")
        numTabs += 1
        numLine, lex, token = self.getSymb()
        if token in ['int', 'real',  'ident']:
            self.numRow += 1
            print("\t"*numTabs+ 'в рядку {0} - {1}'.format(numLine, (lex, token)))
        elif lex == '(':
            self.numRow += 1
            print("\t"*numTabs+ 'в рядку {0} - {1}'.format(numLine, (lex, token)))
            self.parseArithmExpression(numTabs)
            self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        else:

            self.failParse("невідповідність у Expression.Factor",(numLine, lex, token, 'int | real | boolval | ident | ('))
        return True

    def parseExpression(self, numTabs):
        print("\t"*numTabs+"parseExpression():")
        numTabs += 1
        count = self.numRow
        if self.parseBoolExpression(numTabs):
            return True
        self.numRow = count
        if self.parseArithmExpression(numTabs):
            return True

    def parseIf(self, numTabs):
        print("\t"*numTabs+"parseIf():")
        numTabs += 1
        if self.parseLexToken("if", "keyword", "\t" * numTabs):
            self.parseBoolExpression(numTabs)
            self.parseLexToken("goto", "keyword", "\t" * numTabs)
            self.parseToken("ident", "\t" * numTabs)
            self.parseLexToken(";", "punct", "\t" * numTabs)
            return True
        return False

    def parseFor(self, numTabs):
        print("\t"*numTabs+"parseFor():")
        numTabs += 1
        self.parseLexToken("for", "keyword", "\t" * numTabs)
        self.parseToken("ident", "\t" * numTabs)
        self.parseLexToken("=", "assign_op", "\t" * numTabs)
        self.parseArithmExpression(numTabs)
        self.parseLexToken("to", "keyword", "\t" * numTabs)
        self.parseArithmExpression(numTabs)
        self.parseLexToken("do", "keyword", "\t" * numTabs)
        self.parseStatemetList(numTabs)
        self.parseLexToken("end", "keyword", "\t" * numTabs)
        self.parseLexToken(";", "punct", "\t" * numTabs)
        return True

    def parseBoolPart(self, numTabs):
        print('\t'*numTabs  + 'parseBooleanPart():')
        numTabs += 1
        numLine, lex, tok = self.getSymb()
        if lex in ('true', 'false') and tok == 'boolval' :
            self.parseLexToken(lex, 'boolval', "\t" * numTabs)
            #
            numLine, lex, tok = self.getSymb()
            if tok == 'rel_op':
                self.parseLexToken(lex, 'rel_op', "\t" * numTabs)
                numLine, lex, tok = self.getSymb()

                if lex in ('true', 'false') and tok == 'boolval':

                    self.parseLexToken(lex, 'boolval', "\t" * numTabs)
                    return True
                else:
                    return self.parseToken('ident', '\t'*numTabs)
                # else:
                #     return self.parseArithmExpression(numTabs)
            else:
                return True
        elif self.parseArithmExpression(numTabs):
            numLine, lex, tok = self.getSymb()
            if tok == 'rel_op':
                self.numRow += 1
                numLine, lex, tok = self.getSymb()
                if lex in ('true', 'false') and tok == 'boolval':
                    # self.failParse('невідповідність у BoolExpr', (numLine, lex, tok, "ArithmExpr"))
                    self.numRow -= 2
                    numLine, lex, tok = self.getSymb()
                    if tok == 'ident':
                        self.numRow += 2
                        numLine, lex, tok = self.getSymb()
                        self.parseLexToken(lex, 'boolval', "\t" * numTabs)
                        return True
                    else:
                        self.failParse('невідповідність у BoolExpr', (numLine, lex, tok, "ArithmExpr"))

                else:

                    numLine, lex, tok = self.getSymb()
                    if lex == '(':
                        self.numRow -= 1
                        return True
                    self.numRow -= 1
                    numLine, lex, tok = self.getSymb()
                    self.parseLexToken(lex, 'rel_op', "\t" * numTabs)
                    return self.parseArithmExpression(numTabs)
            else:
                print('\t'*numTabs + "Not a BooleanExpression--------------------")
                return False
        elif self.parseToken('ident', '\t'*numTabs):
            return True

        else:
            numLine, lex, tok = self.getSymb()
            self.failParse('невідповідність у BoolExpr', (numLine, lex, tok, 'arythExp or boolConst'))

    def parseBoolPartBrackets(self, numTabs):
        ind = False
        numLine, lex, tok = self.getSymb()
        if lex == '(':
            self.parseLexToken("(", "brackets_op", "\t" * numTabs)
            ind = True
        id = self.parseBoolPart(numTabs)
        if ind:
            self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        return id

    def parseBoolExpression(self, numTabs):
        print('\t'*numTabs+'parseBoolExpression:')
        numTabs+=1
        if self.parseBoolPartBrackets(numTabs):
            while self.parseToken('rel_op', "\t" * numTabs) and self.parseBoolPartBrackets(numTabs):
                pass
            return True
        return False

    def parseRead(self, numTabs):
        print("\t"*numTabs+"parseRead():")
        numTabs += 1
        self.parseLexToken("read", "keyword", "\t" * numTabs)
        self.parseLexToken("(", "brackets_op", "\t")
        self.parseIdentList(numTabs)
        self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        self.parseLexToken(";", "punct", "\t" * numTabs)
        return True

    def parseWrite(self, numTabs):
        print("\t"*numTabs+"parseWrite():")
        numTabs += 1
        self.parseLexToken("write", "keyword", "\t" * numTabs)
        self.parseLexToken("(", "brackets_op", "\t" * numTabs)
        self.parseIdentList(numTabs)
        self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        self.parseLexToken(";", "punct", "\t" * numTabs)
        return True


parser = Parser("test.my_lang")
parser.parseProgram()





