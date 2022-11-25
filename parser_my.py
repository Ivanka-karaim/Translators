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
            print(1234567890)
            self.failParse('getSymb(): неочікуваний кінець програми', self.numRow)
        # таблиця розбору реалізована у формі словника (dictionary)
        # tableOfSymb[numRow]={numRow: (numLine, lexeme, token, indexOfVarOrConst)
        numLine, lexeme, token, _ = tableOfSymb[self.numRow]
        return numLine, lexeme, token

    def failParse(self, str, tuple):
        if str == 'неочікуваний кінець програми':
            (lexeme, token, numRow) = tuple
            print(
                'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format(
                    (lexeme, token), numRow))
            exit(1001)
        if str == 'getSymb(): неочікуваний кінець програми':
            numRow = tuple
            print(
                'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(
                    numRow, tableOfSymb[numRow - 1]))
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

    def parseToken(self, lexeme, token, indent):
        # доступ до поточного рядка таблиці розбору


        # якщо всі записи таблиці розбору прочитані,
        # а парсер ще не знайшов якусь лексему
        if self.numRow > self.len_tableOfSymb:
            print(1234567890)
            self.failParse('неочікуваний кінець програми', (lexeme, token, self.numRow))

        # прочитати з таблиці розбору
        # номер рядка програми, лексему та її токен
        numLine, lex, tok = self.getSymb()

        # тепер поточним буде наступний рядок таблиці розбору
        self.numRow += 1

        # чи збігаються лексема та токен таблиці розбору з заданими
        if (lex, tok) == (lexeme, token):
            # вивести у консоль номер рядка програми та лексему і токен
            print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lexeme, token)))
            return True
        else:
            # згенерувати помилку та інформацію про те, що
            # лексема та токен таблиці розбору (lex,tok) відрізняються від
            # очікуваних (lexeme,token)
            print(1234567890)
            self.failParse('невідповідність токенів', (numLine, lex, tok, lexeme, token))
            return False

    def parseTokenIdent(self, token,  indent):
        # доступ до поточного рядка таблиці розбору


        # якщо всі записи таблиці розбору прочитані,
        # а парсер ще не знайшов якусь лексему
        if self.numRow > self.len_tableOfSymb:
            print(1234567890)
            self.failParse('неочікуваний кінець програми3673', (token,  self.numRow))

        # прочитати з таблиці розбору
        # номер рядка програми, лексему та її токен
        numLine, lex, tok = self.getSymb()

        # тепер поточним буде наступний рядок таблиці розбору
        self.numRow += 1

        # чи збігаються лексема та токен таблиці розбору з заданими
        if tok == token:
            # вивести у консоль номер рядка програми та лексему і токен
            print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine,  token))
            return True
        else:
            # згенерувати помилку та інформацію про те, що
            # лексема та токен таблиці розбору (lex,tok) відрізняються від
            # очікуваних (lexeme,token)
            self.numRow -= 1
            return False

    def parseProgram(self):
        try:

            # перевірити синтаксичну коректність списку інструкцій StatementList
            # parseStatementList()
            self.parseDeclarList()
            self.parseStatemetList()

            # повідомити про синтаксичну коректність програми
            print('Parser: Синтаксичний аналіз завершився успішно')
            return True
        except SystemExit as e:
            # Повідомити про факт виявлення помилки
            print('Parser: Аварійне завершення програми з кодом {0}'.format(e))

    def parseDeclarList(self):
        print("parseDeclarList():")
        numTabs = 1
        while self.parseDeclaration(numTabs):
            pass
        return True

    def parseDeclaration(self, numTabs):
        # взяти поточну лексему
        if self.numRow >= self.len_tableOfSymb:
            return False

        numLine, lex, token = self.getSymb()
        if lex in ['int', 'real', 'bool'] and token == "keyword":
            print("\t"*numTabs+"parseDeclaration():")
            numTabs += 1
            self.parseType(numTabs)
            if not self.parseIdentList(numTabs):
                print(1234567890)
                self.failParse("Parser Error: \n\t In line {numLine} expected a list of identifiers in an declaration" ,numLine )
            self.parseToken(";", "punct", '\t'*numTabs)
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
        else:
            print(1234567890)
            self.failParse("strhrt", 34)
        return True

    def parseIdentList(self, numTabs):
        print("\t"*numTabs+"parseIdentList():")
        numTabs += 1
        if not self.parseTokenIdent("ident",'\t'*numTabs):
            return False
        # numLine, lex, token = self.getSymb()
        # print(self.getSymb()[1])
        while self.getSymb()[1] == "," and self.getSymb()[2] == "punct":
            self.parseToken(",", "punct", "\t"*numTabs)
            self.parseTokenIdent("ident", "\t"*numTabs)
        return True

    def parseStatemetList(self, numTabs=0):
        if self.numRow >= self.len_tableOfSymb:
            return False
        print("\t"*numTabs+"parseStatementList():")
        numTabs += 1
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
        # якщо токен - ідентифікатор
        # обробити інструкцію присвоювання
        # print(self.getSymb()[1])

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
            self.parseTokenIdent("mark", "\t"*numTabs)
            return True


            # тут - ознака того, що всі інструкції були коректно
        # розібрані і була знайдена остання лексема програми.
        # тому parseStatement() має завершити роботу

    def parseAssign(self, numTabs):
        print("\t"*numTabs+"parseAssign():")
        numTabs += 1
        self.parseTokenIdent("ident", "\t"*numTabs)
        if self.parseToken("=", "assign_op", "\t"*numTabs):
            self.parseExpression(numTabs)
            self.parseToken(";", "punct", "\t"*numTabs)
            return True
        else:
            print(1234567890)
            self.failParse("retert", 324)

    def parseArithmExpression(self, numTabs):
        print("\t"*numTabs+"parseArithExpression():")
        numTabs += 1
        self.parseTokenIdent( "add_op", "\t" * numTabs)
        # self.parseTokenIdent("add_op", "\t")

        if not self.parseTerm(numTabs):
            return False
        while self.parseTokenIdent("add_op", "\t"*numTabs) and self.parseTerm(numTabs):
            pass
        return True

    def parseTerm(self, numTabs):
        print("\t"*numTabs+"parseTerm():")
        numTabs +=1
        if not self.parseFactor(numTabs):
            return False
        # numLine, lex, token = self.getSymb()

        while (self.parseTokenIdent("mult_op", "\t"*numTabs) or self.parseTokenIdent("pow_op", "\t"*numTabs)) and self.parseFactor(numTabs):
            pass
        return True

    def parseFactor(self, numTabs):
        print("\t"*numTabs+"parseFactor():")
        numTabs += 1
        numLine, lex, token = self.getSymb()
        if token in ['int', 'real', 'boolval', 'ident']:
            self.numRow += 1
            print("\t"*numTabs+ 'в рядку {0} - {1}'.format(numLine, (lex, token)))
        elif lex == '(':
            self.numRow += 1
            print("\t"*numTabs+ 'в рядку {0} - {1}'.format(numLine, (lex, token)))
            self.parseExpression(numTabs)
            self.parseToken(")", "brackets_op", "\t"*numTabs)
        else:
            print(1234567890)
            self.failParse("363", 2463)
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
        else:
            print(1234567890)
            self.failParse("2435", 4325)

    def parseIf(self, numTabs):
        print("\t"*numTabs+"parseIf():")
        numTabs += 1
        if self.parseToken("if", "keyword", "\t"*numTabs):
            self.parseBoolExpression(numTabs)
            self.parseToken("goto", "keyword", "\t"*numTabs)
            self.parseTokenIdent("ident", "\t"*numTabs)
            self.parseToken(";", "punct", "\t" * numTabs)
            return True
        return False

    def parseFor(self, numTabs):
        print("\t"*numTabs+"parseFor():")
        numTabs += 1
        self.parseToken("for", "keyword", "\t"*numTabs)
        self.parseTokenIdent("ident" , "\t"*numTabs)
        self.parseToken("=", "assign_op", "\t"*numTabs)
        self.parseArithmExpression(numTabs)
        self.parseToken("to", "keyword", "\t"*numTabs)
        self.parseArithmExpression(numTabs)
        self.parseToken("do", "keyword", "\t" * numTabs)
        self.parseStatemetList(numTabs)
        self.parseToken("end", "keyword", "\t" * numTabs)
        self.parseToken(";", "punct", "\t" * numTabs)
        return True

    # def parseBoolExpression(self):
    #     print("parseBoolExpression():")
    #     if self.parseTokenIdent("boolval", "\t"):
    #         while self.parseTokenIdent("rel_op", "\t") and self.parseExpression():
    #             pass
    #         return True
    #     elif self.parseArithmExpression():
    #
    #         return self.parseTokenIdent("rel_op", "\t") and self.parseExpression()
    #     else:
    #
    #         self.failParse("5464", 35)

    def parseBoolExpression(self, numTabs):
        print('\t'*numTabs  + 'parseBooleanExpression():')
        numTabs += 1
        numLine, lex, tok = self.getSymb()
        if lex in ('true', 'false') and tok == 'boolval':
            self.parseToken(lex, 'boolval', "\t"*numTabs)
            numLine, lex, tok = self.getSymb()
            if tok == 'rel_op':
                self.parseToken(lex, 'rel_op', "\t"*numTabs)
                numLine, lex, tok = self.getSymb()
                if lex in ('true', 'false') and tok == 'boolval':
                    self.parseToken(lex, 'boolval', "\t"*numTabs)
                    return True
                else:
                    return self.parseArithmExpression(numTabs)
            else:
                return True

        elif self.parseArithmExpression(numTabs):
            numLine, lex, tok = self.getSymb()
            if tok == 'rel_op':
                self.parseToken(lex, 'rel_op', "\t"*numTabs)
                numLine, lex, tok = self.getSymb()
                if lex in ('true', 'false') and tok == 'boolval':
                    self.parseToken(lex, 'boolval',"\t"*numTabs)
                    return True
                else:
                    return self.parseArithmExpression(numTabs)
            else:
                print('\t'*numTabs  + "Not a BooleanExpression--------------------")
                return False
        else:
            numLine, lex, tok = self.getSymb()
            print(1234567890)
            self.failParse('невідповідність у BoolExpr', (numLine, lex, tok, 'arythExp or boolConst'))

    def parseRead(self, numTabs):
        print("\t"*numTabs+"parseRead():")
        numTabs += 1
        self.parseToken("read", "keyword", "\t"*numTabs)
        self.parseToken("(", "brackets_op", "\t")
        if not self.parseIdentList(numTabs):
            print(1234567890)
            self.failParse("6356", 54)
        self.parseToken(")", "brackets_op", "\t"*numTabs)
        self.parseToken(";", "punct", "\t"*numTabs)
        return True

    def parseWrite(self, numTabs):
        print("\t"*numTabs+"parseWrite():")
        numTabs += 1
        self.parseToken("write", "keyword", "\t"*numTabs)
        self.parseToken("(", "brackets_op", "\t"*numTabs)
        if not self.parseIdentList(numTabs):
            print(1234567890)
            self.failParse("6356", 54)
        self.parseToken(")", "brackets_op", "\t"*numTabs)
        self.parseToken(";", "punct", "\t"*numTabs)
        return True


parser = Parser("test3.my_lang")
parser.parseProgram()





