from lexema import Lexema
from lexema import tableOfSymb
from lexema import tableOfMark


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

    # Прочитати з таблицi розбору поточний запис за його номером numRow
    # Повернути номер рядка програми, лексему та її токен
    def getSymb(self):
        if self.numRow > self.len_tableOfSymb:
            self.failParse('getSymb(): неочікуваний кінець програми', self.numRow)
        # таблиця розбору реалізована у формі словника (dictionary)
        # tableOfSymb[numRow]={numRow: (numLine, lexeme, token, indexOfVarOrConst)
        numLine, lexeme, token, _ = tableOfSymb[self.numRow]
        return numLine, lexeme, token

    def failParse(self, str, tuple):
        if str == 'неочікуваний кінець програми':
            (lexeme, token, numRow) = tuple
            print(
                'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format((lexeme, token), numRow))

            exit(1001)
        if str == 'getSymb(): неочікуваний кінець програми':
            numRow = tuple
            print(
                'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(numRow, tableOfSymb[numRow - 1]))
            exit(1002)

        elif str == 'невідповідність токенів':
            (numLine, lexeme, token, lex, tok) = tuple
            print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - ({3},{4}).'.format(numLine, lexeme, token, lex, tok))
            exit(1)

        elif str == 'невідповідність інструкцій':
            (numLine, lex, tok, expected) = tuple
            print(
                'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,lex,tok,expected))
            exit(2)
        elif str == 'невідповідність у Expression.Factor':
            (numLine, lex, tok, expected) = tuple
            print(
                'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,lex,tok,expected))
            exit(3)

        elif str == 'невідповідність в IdentList':
            (numLine, lex, tok, expected) = tuple
            print(
                'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,lex,tok,expected))
            exit(4)
        elif str == 'відсутній StatementList':
            print('Parser ERROR: \n\t В програмі очікувався хоча б один Statement')
            exit(5)


    # Функцiя перевiряє, чи у поточному рядку таблицi розбору
    # зустрiлась вказана лексема lexeme з токеном token
    # параметр indent - вiдступ при виведеннi у консоль
    def parseLexToken(self, lexeme, token, indent):
        # якщо всi записи таблицi розбору прочитанi,
        # а парсер ще не знайшов якусь лексему
        if self.numRow > self.len_tableOfSymb:
            self.failParse('неочікуваний кінець програми', (lexeme, token, self.numRow))
        # прочитати з таблицi розбору
        # номер рядка програми, лексему та її токен
        numLine, lex, tok = self.getSymb()

        # тепер поточним буде наступний рядок таблицi розбору
        self.numRow += 1
        # чи збiгаються лексема та токен таблицi розбору (lex, tok)
        # з очiкуваними (lexeme,token)
        if (lex, tok) == (lexeme, token):
            # вивести у консоль номер рядка програми та лексему і токен
            print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lexeme, token)))
            return True
        else:
            # згенерувати помилку та iнформацiю про те, що
            # лексема та токен таблицi розбору (lex,tok) вiдрiзняються вiд
            # очiкуваних (lexeme,token)
            self.failParse('невідповідність токенів', (numLine, lex, tok, lexeme, token))
            return False

    # Функцiя перевiряє, чи у поточному рядку таблицi розбору
    # зустрiвся вказаний токен
    # параметр indent - вiдступ при виведеннi у консоль
    def parseToken(self, token, indent):
        # якщо всі записи таблиці розбору прочитані
        if self.numRow > self.len_tableOfSymb:
            numLine, lex, tok = self.getSymb()

            self.failParse('неочікуваний кінець програми', (lex, tok, self.numRow))
        # прочитати з таблицi розбору
        # номер рядка програми, лексему та її токен
        numLine, lex, tok = self.getSymb()

        # тепер поточним буде наступний рядок таблиці розбору
        self.numRow += 1

        # чи збігаються лексема та токен таблиці розбору з заданими
        if tok == token:
            # вивести у консоль номер рядка програми та лексему і токен
            print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine, token))
            return True
        # якщо не збігаються, то дана функція не має сповіщати про помилку,
        # а має повернути false
        else:
            # щоб прочитати відповідну лексему ще раз, але в іншій функції,
            # то потрібно повернутись до неї
            self.numRow -= 1
            return False

    def parseProgram(self):
        try:
            # перевірити наявність та синтаксичну коректність декларації
            self.parseDeclarList()
            # перевірити синтаксичну коректність списку інструкцій StatementList
            self.parseStatemetList()
            print('Parser: Синтаксичний аналіз завершився успішно')
            return True
        # в разі виклику функції exit() обробити її
        except SystemExit as e:
            print('Parser: Аварійне завершення програми з кодом {0}'.format(e))

    # оголошення змінних
    def parseDeclarList(self):
        print("parseDeclarList():")
        numTabs = 1
        while self.parseDeclaration(numTabs):
            pass
        return True

    def parseDeclaration(self, numTabs):
        # якщо всi записи таблицi розбору прочитанi
        if self.numRow > self.len_tableOfSymb:
            return False
        print('\t' * numTabs + 'parseDeclaration:')
        numTabs += 1
        # перевірка на наявність типу
        if self.parseType(numTabs):
            # перевіряє правильність запису ідентифікаторів
            self.parseIdentList(numTabs)
            # перевіряє наявність ; в кінці оголошення
            self.parseLexToken(";", "punct", '\t' * numTabs)
            return True
        # якщо це не тип, то тоді оголошення завершено
        else:
            return False

    def parseType(self, numTabs):
        # прочитати з таблицi розбору
        # номер рядка програми, лексему та її токен
        numLine, lex, token = self.getSymb()
        # перевірити чи лексема відповідає якомусь з типів
        if lex in ['int', 'real', 'bool'] and token == "keyword":
            print("\t" * numTabs + "parseType():")
            numTabs += 1
            self.numRow += 1
            print("\t" * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, token)))
            return True
        else:
            return False

    def parseIdentList(self, numTabs):
        print("\t" * numTabs + "parseIdentList():")
        numTabs += 1
        # перевірка на наявність хоча б одного ідентифікатора
        if not self.parseToken("ident", '\t' * numTabs):
            numLine, lex, token = self.getSymb()
            # помилка невідповідність в IdentList
            self.failParse('невідповідність в IdentList', (numLine, lex, token, 'ident'))
        # поки зустрічається кома між ідентифікаторами
        while self.getSymb()[1] == "," and self.getSymb()[2] == "punct":
            self.parseLexToken(",", "punct", "\t" * numTabs)
            # перевірка на наявність ідентифікатора
            if not self.parseToken("ident", '\t' * numTabs):
                numLine, lex, token = self.getSymb()
                self.failParse('невідповідність в IdentList', (numLine, lex, token, 'ident'))
        return True

    def parseStatemetList(self, numTabs=0):
        print("\t" * numTabs + "parseStatementList():")
        numTabs += 1
        # виклик першої інструкції,
        # оскільки обов'язково має бути хоча б одна
        if not self.parseStatement(numTabs):
            self.failParse('відсутній StatementList', ())
        while self.parseStatement(numTabs):
            pass
        return True

    def parseStatement(self, numTabs):
        # перевірка наявності нових лексем
        if self.numRow > self.len_tableOfSymb:
            return False
        print("\t" * numTabs + 'parseStatement():')
        numTabs += 1
        # прочитаємо поточну лексему в таблиці розбору
        numLine, lex, token = self.getSymb()

        # якщо токен — iдентифiкатор, то
        # обробити iнструкцiю присвоєння
        if token == 'ident':
            self.parseAssign(numTabs)
            # перевірка ; у кінці виразу
            self.parseLexToken(";", "punct", "\t" * numTabs)
            return True
        # якщо токен — ключове слово
        # а лексема - read, то
        # обробити iнструкцiю читання
        elif token == "keyword" and lex == "read":
            self.parseInp(numTabs)
            # перевірка ; у кінці виразу
            self.parseLexToken(";", "punct", "\t" * numTabs)
            return True
        # якщо токен — ключове слово
        # а лексема - write, то
        # обробити iнструкцiю виведення
        elif token == "keyword" and lex == "write":
            self.parseOut(numTabs)
            # перевірка ; у кінці виразу
            self.parseLexToken(";", "punct", "\t" * numTabs)
            return True
        # якщо токен — ключове слово
        # а лексема - for, то
        # обробити iнструкцiю повторень
        elif (lex, token) == ('for', 'keyword'):
            self.parseFor(numTabs)
            # перевірка ; у кінці виразу
            self.parseLexToken(";", "punct", "\t" * numTabs)
            return True
        # якщо лексема - ключове слово 'if'
        # обробити інструкцію розгалудження
        elif (lex, token) == ('if', 'keyword'):
            self.parseIf(numTabs)
            # перевірка ; у кінці виразу
            self.parseLexToken(";", "punct", "\t" * numTabs)
            return True
        # якщо токен - mark
        elif token == 'mark':
            self.parseToken("mark", "\t" * numTabs)
            return True
        # якщо лексема - ключове слово 'end'
        # i воно знаходиться в інструкції повторень
        # вийти з Statement
        elif lex == 'end' and numTabs > 3:
            return False
        else:
            self.failParse('невідповідність інструкцій', (numLine, lex, token, 'ident, read, write, for, if or mark'))

    def parseAssign(self, numTabs):
        print("\t" * numTabs + "parseAssign():")
        numTabs += 1
        # взяти поточну лексему
        numLine, lex, tok = self.getSymb()
        # встановити номер нової поточної лексеми
        self.numRow += 1
        print('\t' * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        # перевірка оператора присвоювання
        self.parseLexToken("=", "assign_op", "\t" * numTabs)
        # розбір виразу
        self.parseExpression(numTabs)

    def parseArithmExpression(self, numTabs):
        print("\t" * numTabs + "parseArithExpression():")
        numTabs += 1
        # може зустрічатись знак
        self.parseToken("add_op", "\t" * numTabs)

        # якщо не Term то це не арифметичний оператор
        if not self.parseTerm(numTabs):
            return False
        # поки зустрічається add_op Term,
        # доти розглядається арифметичний оператор
        while self.parseToken("add_op", "\t" * numTabs) and self.parseTerm(numTabs):
            pass
        return True

    def parseTerm(self, numTabs):
        print("\t" * numTabs + "parseTerm():")
        numTabs += 1
        # якщо не Factor то це не Term
        if not self.parseFactor(numTabs):
            return False
        while (self.parseToken("mult_op", "\t" * numTabs) or self.parseToken("pow_op",
                                                                             "\t" * numTabs)) and self.parseFactor(
            numTabs):
            pass
        return True

    def parseFactor(self, numTabs):
        print("\t" * numTabs + "parseFactor():")
        numTabs += 1
        numLine, lex, token = self.getSymb()
        # перевірка констант та ідентифікаторів
        if token in ['int', 'real', 'ident']:
            self.numRow += 1
            print("\t" * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, token)))
        elif token == 'boolval':
            self.numRow -= 1
            if self.getSymb()[2] == 'rel_op':
                self.numRow += 1
                print("\t" * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, token)))
            self.numRow += 1
        # якщо зустрічається дужка, то викликається арифметичний оператор
        elif lex == '(':
            self.numRow += 1
            print("\t" * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, token)))
            self.parseExpression(numTabs)
            self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        else:
            self.failParse("невідповідність у Expression.Factor",
                           (numLine, lex, token, 'int | real | boolval | ident | ('))
        return True

    def parseExpression(self, numTabs):
        print("\t" * numTabs + "parseExpression():")
        numTabs += 1
        count = self.numRow
        # перевірка на булевий вираз
        if self.parseBoolExpression(numTabs):
            return True
        self.numRow = count
        # перевірка на арифметичний вираз
        if self.parseArithmExpression(numTabs):
            return True

    def parseIf(self, numTabs):
        print("\t" * numTabs + "parseIf():")
        numTabs += 1
        # перевірка ключового слова if
        if self.parseLexToken("if", "keyword", "\t" * numTabs):
            self.parseBoolExpression(numTabs)
            # перевірка ключового слова goto
            self.parseLexToken("goto", "keyword", "\t" * numTabs)
            self.parseToken('ident', '\t' * numTabs)
            return True
            # numLine, lex, tok = self.getSymb()
            # # перевірка чи існує така марка в таблиці марок
            # if lex+':' not in tableOfMark:
            #     self.failParse('неіснуюча марка', (numLine, lex, tok, tableOfMark))
            # else:
            #     self.numRow+=1
            #     return True
        return False

    def parseFor(self, numTabs):
        print("\t" * numTabs + "parseFor():")
        numTabs += 1
        # перевірка ключого слова for
        self.parseLexToken("for", "keyword", "\t" * numTabs)
        # перевірка наявності ідентифікатора
        self.parseToken("ident", "\t" * numTabs)
        # перевірка оператора присвоювання
        self.parseLexToken("=", "assign_op", "\t" * numTabs)
        # виклик фунції арифметичний вираз
        self.parseArithmExpression(numTabs)
        # перевірка ключого слова to
        self.parseLexToken("to", "keyword", "\t" * numTabs)
        # виклик фунції арифметичний вираз
        self.parseArithmExpression(numTabs)
        # перевірка ключого слова do
        self.parseLexToken("do", "keyword", "\t" * numTabs)
        # перевірка списку інструкцій
        self.parseStatemetList(numTabs)
        # перевірка ключого слова end
        self.parseLexToken("end", "keyword", "\t" * numTabs)
        return True

    # def parseBoolPart(self, numTabs):
    #     print('\t' * numTabs + 'parseBooleanPart():')
    #     numTabs += 1
    #     numLine, lex, tok = self.getSymb()
    #     print(tok)
    #
    #     if lex in ['true', 'false']:
    #         self.parseLexToken(lex, tok, '\t'*numTabs)
    #         return True
    #     elif self.getSymb()[2] == 'ident':
    #         self.parseToken('ident', '\t'*numTabs)
    #
    #         if self.getSymb()[2] == 'rel_op':
    #             # self.numRow -=1
    #
    #             return True
    #         self.numRow -= 1
    #
    #     elif self.parseArithmExpression(numTabs):
    #         numLine, lex, tok = self.getSymb()
    #         if tok != 'rel_op':
    #             print('\t' * numTabs + "Not a BooleanExpression--------------------")
    #             return False
    #         else:
    #             self.parseLexToken(lex, tok, '\t'*numTabs)
    #             return self.parseArithmExpression(numTabs)

    #
    # def parseBoolPart(self, numTabs):
    #     print('\t'*numTabs  + 'parseBooleanPart():')
    #     numTabs += 1
    #     numLine, lex, tok = self.getSymb()
    #     if lex in ('true', 'false') and tok == 'boolval':
    #         self.parseLexToken(lex, 'boolval', "\t" * numTabs)
    #         #
    #         numLine, lex, tok = self.getSymb()
    #         if tok == 'rel_op':
    #             self.parseLexToken(lex, 'rel_op', "\t" * numTabs)
    #             numLine, lex, tok = self.getSymb()
    #
    #             if lex in ('true', 'false') and tok == 'boolval':
    #                 self.parseLexToken(lex, 'boolval', "\t" * numTabs)
    #                 return True
    #             elif lex in ('(', ')'):
    #                 self.numRow -=1
    #                 return True
    #             else:
    #                 return self.parseToken('ident', '\t'*numTabs)
    #             # else:
    #             #     return self.parseArithmExpression(numTabs)
    #         else:
    #             return True
    #     elif self.parseArithmExpression(numTabs):
    #         numLine, lex, tok = self.getSymb()
    #         if tok == 'rel_op':
    #             self.numRow += 1
    #             numLine, lex, tok = self.getSymb()
    #             if lex in ('true', 'false') and tok == 'boolval':
    #                 # self.failParse('невідповідність у BoolExpr', (numLine, lex, tok, "ArithmExpr"))
    #                 self.numRow -= 2
    #                 numLine, lex, tok = self.getSymb()
    #                 if tok == 'ident':
    #                     self.numRow += 2
    #                     numLine, lex, tok = self.getSymb()
    #                     self.parseLexToken(lex, 'boolval', "\t" * numTabs)
    #                     return True
    #                 else:
    #                     self.failParse('невідповідність у BoolExpr', (numLine, lex, tok, "ArithmExpr"))
    #             else:
    #                 numLine, lex, tok = self.getSymb()
    #                 if lex == '(':
    #                     self.numRow -= 1
    #                     return True
    #                 self.numRow -= 1
    #                 numLine, lex, tok = self.getSymb()
    #                 self.parseLexToken(lex, 'rel_op', "\t" * numTabs)
    #                 return self.parseArithmExpression(numTabs)
    #         else:
    #             print('\t'*numTabs + "Not a BooleanExpression--------------------")
    #             return False
    #     elif self.parseToken('ident', '\t'*numTabs):
    #         return True
    #
    #     else:
    #         numLine, lex, tok = self.getSymb()
    #         self.failParse('невідповідність у BoolExpr', (numLine, lex, tok, 'arythExp or boolConst'))
    #
    # def parseBoolPartBrackets(self, numTabs):
    #
    #     ind = False
    #     numLine, lex, tok = self.getSymb()
    #     if lex == '(':
    #
    #         self.parseLexToken("(", "brackets_op", "\t" * numTabs)
    #         ind = True
    #     id = self.parseBoolPart(numTabs)
    #     while not self.parseToken('brackets_op', '\t'*numTabs) and ind:
    #
    #         self.parseToken('rel_op', '\t' * numTabs)
    #         self.parseBoolPart(numTabs)
    #     if ind:
    #         self.numRow -=1
    #         self.parseLexToken(")", "brackets_op", "\t" * numTabs)
    #     return id
    #
    # def parseBoolExpression(self, numTabs):
    #     print('\t'*numTabs+'parseBoolExpression:')
    #     numTabs+=1
    #     if self.parseBoolPartBrackets(numTabs):
    #
    #         while self.parseToken('rel_op', "\t" * numTabs) and self.parseBoolPartBrackets(numTabs):
    #             pass
    #         return True
    #     return False

    def parseBoolExpression(self, numTabs):
        print('\t' * numTabs + 'parseBoolExpression():')
        numTabs += 1
        # перевірка на наявність булевого виразу
        if self.parseBoolPart(numTabs):
            # поки є оператор
            while self.parseToken('rel_op', '\t' * numTabs):
                # виконувати булевий вираз
                self.parseBoolPart(numTabs + 1)
            return True
        # повідомлення про відсутність логічного виразу
        print('\t'*numTabs + '-Not a BoolExpression-')
        return False

    def parseBoolPart(self, numTabs):
        print('\t' * numTabs + 'parseBoolPart():')
        numTabs += 1
        # читання поточного елемента
        numLine, lex, tok = self.getSymb()
        # перевірка чи є цей елемент boolval
        if lex in ('true', 'false') and tok == 'boolval':
            self.parseLexToken(lex, 'boolval', '\t' * numTabs)
            return True
        # перевірка чи є цей елемент арифметичним виразом
        elif self.parseArithmExpression(numTabs):

            numLine, lex, tok = self.getSymb()
            # перевірка на наявність булевого оператора
            if tok == 'rel_op':
                self.parseLexToken(lex, 'rel_op', '\t' * numTabs)
                # перевірка арифметичного оператора
                if self.parseArithmExpression(numTabs):
                    return True
            else:
                return False
        else:
            return False

    def parseInp(self, numTabs):
        print("\t" * numTabs + "parseRead():")
        numTabs += 1
        # перевірка ключового слова read
        self.parseLexToken("read", "keyword", "\t" * numTabs)
        # перевірка наявності дужки
        self.parseLexToken("(", "brackets_op", "\t"*numTabs)
        # перевірка списку ідентифікаторів
        self.parseIdentList(numTabs)
        # перевірка наявності дужки
        self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        return True

    def parseOut(self, numTabs):
        print("\t" * numTabs + "parseWrite():")
        numTabs += 1
        # перевірка ключового слова write
        self.parseLexToken("write", "keyword", "\t" * numTabs)
        # перевірка наявності дужки
        self.parseLexToken("(", "brackets_op", "\t" * numTabs)
        # перевірка списку ідентифікаторів
        self.parseIdentList(numTabs)
        # перевірка наявності дужки
        self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        return True


parser = Parser("test.my_lang")
parser.parseProgram()
