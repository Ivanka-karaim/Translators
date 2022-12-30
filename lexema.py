FSuccess = (True, 'Lexer')

# state-transition function
stf = {(0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'other'): 2,
       (0, 'Digit'): 3, (3, 'Digit'): 3, (3, 'other'): 4, (3, '.'): 5, (5, 'Digit'): 6, (5, 'other'): 102,
       (6, 'Digit'): 6, (6, 'other'): 7,
       (0, 'nl'): 8,
       (0, 'ws'): 0,
       (0, '+'): 9, (0, '-'): 9, (0, '*'): 9, (0, '/'): 9, (0, '^'): 9, (0, ')'): 9,
       (0, '('): 9, (0, ';'): 9, (0, ':'): 9, (0, ','): 9,
       (0, '!'): 10, (10, '='): 12, (10, 'other'): 103,
       (0, '>'): 12, (0, '='): 12, (0, '<'): 12,
       (12, '='): 11, (12, 'other'): 13,
       (1, ':'): 14, (14, 'other'): 15,
       (0, 'other'): 101
       }

initState = 0  # q0 - стартовий стан
F = {2, 4, 7, 8, 9, 11, 13, 15, 101, 102, 103}  # множина заключних станiв
Fstar = {2, 4, 7, 13, 15}  # зiрочка
Ferror = {101, 102, 103}  # обробка помилок

# Таблиця лексем мови
tableOfLanguageTokens = {'end': 'keyword', 'int': 'keyword', 'real': 'keyword', 'bool': 'keyword',
                         'true': 'bool', 'false': 'bool', 'read': 'keyword', 'write': 'keyword', 'for': 'keyword',
                         'to': 'keyword', 'do': 'keyword', 'if': 'keyword', 'goto': 'keyword',
                         '=': 'assign_op', '.': 'punct', ':': 'punct', ';': 'punct', ',': 'punct',
                         ' ': 'ws', '\t': 'ws', '\n': 'nl',
                         '-': 'add_op', '+': 'add_op', '*': 'mult_op', '/': 'mult_op',
                         'div': 'mult_op', '^': 'pow_op', '(': 'brackets_op', ')': 'brackets_op',
                         '<': 'rel_op', '>': 'rel_op', '<=': 'rel_op', '>=': 'rel_op', '==': 'rel_op', '!=': 'rel_op'}

# Решту токенiв визначаємо не за лексемою, а за заключним станом
tableIdentFloatInt = {2: 'ident', 4: 'int', 7: 'real', 15: 'mark'}

tableOfId = {}  # Таблиця ідентифікаторів
tableOfConst = {}  # Таблиць констант
tableOfSymb = {}  # Таблиця символів програми (таблиця розбору)
tableOfLabel = {}


class Lexema:
    def __init__(self, name_file):
        f = open(name_file, 'r')
        self.sourceCode = f.read()
        f.close()
        self.state = initState  # поточний стан
        self.lenCode = len(self.sourceCode) - 1  # номер останнього символа у файлі з кодом програми
        self.numLine = 1  # лексичний аналіз починаємо з першого рядка
        self.numChar = -1  # з першого символа (в Python'і нумерація - з 0)
        self.char = ''  # ще не брали жодного символа
        self.lexeme = ''  # ще не починали розпізнавати лексеми

    def nextChar(self):
        self.numChar += 1
        return self.sourceCode[self.numChar]

    def putCharBack(self):
        return self.numChar - 1

    def nextState(self, classCh):
        try:
            return stf[(self.state, classCh)]
        except KeyError:
            return stf[(self.state, 'other')]

    def is_final(self):
        if self.state in F:
            return True
        else:
            return False

    def processing(self):
        if self.state == 8:  # \n
            self.numLine += 1
            self.state = initState
        if self.state in (2, 4, 7, 13, 15):  # keyword, ident, float, int
            token = self.getToken()

            if token != 'keyword' and token != 'assign_op' and token != 'rel_op':
                index = self.indexIdConst(token)
                print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(self.numLine, self.lexeme, token, index))
                tableOfSymb[len(tableOfSymb) + 1] = (self.numLine, self.lexeme, token, index)
                # if self.state == 15:
                #     tableOfMark.append(self.lexeme)
            else:  # якщо keyword

                print('{0:<3d} {1:<10s} {2:<10s} '.format(self.numLine, self.lexeme, token))
                tableOfSymb[len(tableOfSymb) + 1] = (self.numLine, self.lexeme, token, '')
            self.lexeme = ''
            self.numChar = self.putCharBack()  # зірочка
            self.state = initState
        if self.state in (9, 11, 12):
            if self.state != 13:
                self.lexeme += self.char
            token = self.getToken()
            print('{0:<3d} {1:<10s} {2:<10s} '.format(self.numLine, self.lexeme, token))
            tableOfSymb[len(tableOfSymb) + 1] = (self.numLine, self.lexeme, token, '')
            self.lexeme = ''
            self.state = initState

        if self.state in Ferror:  # (101,102,103):  # ERROR
            self.fail()

    def getToken(self):
        try:
            return tableOfLanguageTokens[self.lexeme]
        except KeyError:
            return tableIdentFloatInt[self.state]

    def indexIdConst(self, token):
        indx = 0
        indx1 =None
        if token == 'ident':
            indx1 = tableOfId.get(self.lexeme)
            if indx1 is None:
                indx = len(tableOfId) + 1
                tableOfId[self.lexeme] = (indx,'type_undef','val_undef')
        if self.state == 4 or self.state == 7 or token == 'bool':
            indx1 = tableOfConst.get(self.lexeme)
            if indx1 is None:

                indx = len(tableOfConst) + 1
                if self.state == 7:
                    val = float(self.lexeme)
                elif self.state == 4:
                    val = int(self.lexeme)
                else:
                    val = self.lexeme
                tableOfConst[self.lexeme] = (indx, token, val)
        if not (indx1 is None):
            if len(indx1) == 2:
                indx, _ = indx1
            else:
                indx, _, _ = indx1
        return indx


    def fail(self):
        print(self.numLine)
        if self.state == 101:
            print('Lexer: у рядку ', self.numLine, ' неочікуваний символ ' + self.char)
            exit(101)
        if self.state == 102:
            print('Lexer: у рядку ', self.numLine, ' очікувалося число, а не ' + self.char)
            exit(102)
        if self.state == 103:
            print('Lexer: у рядку ', self.numLine, ' очікувався символ =, а не ' + self.char)
            exit(103)

    def lex(self):
        global FSuccess
        try:
            # print(self.lenCode)
            while self.numChar < self.lenCode:
                self.char = self.nextChar()  # прочитати наступний символ
                self.state = self.nextState(self.classOfChar())  # обчислити наступний стан
                if self.is_final():  # якщо стан заключний
                    self.processing()  # виконати семантичні процедури
                # if state in Ferror:	    # якщо це стан обробки помилки
                # break					#      то припинити подальшу обробку
                elif self.state == initState:
                    # print("34535")
                    self.lexeme = ''  # якщо стан НЕ заключний, а стартовий - нова лексема
                else:
                    self.lexeme += self.char  # якщо стан НЕ закл. і не стартовий - додати символ до лексеми
            print('Lexer: Лексичний аналіз завершено успішно')
        except SystemExit as e:
            # Встановити ознаку неуспішності
            FSuccess = (False, 'Lexer')
            # Повідомити про факт виявлення помилки
            print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))

    def classOfChar(self):
        if self.char in 'abcdefghijklmnopqrstuvwxyz':
            res = "Letter"
        elif self.char in "0123456789":
            res = "Digit"
        elif self.char in " \t":
            res = "ws"
        elif self.char in "\n":
            res = "nl"
        elif self.char in "+-:=*/()^><!.:;,":
            res = self.char
        else:
            res = 'символ не належить алфавiту'
        return res

    def getSourceCode(self):
        return self.sourceCode


def tableToPrint(Tbl):
    if Tbl == "Symb":
        tableOfSymbToPrint()
    elif Tbl == "Id":
        tableOfIdToPrint()
    elif Tbl == "Const":
        tableOfConstToPrint()
    elif Tbl == "Label":
        tableOfLabelToPrint()
    else:
        tableOfSymbToPrint()
        tableOfIdToPrint()
        tableOfConstToPrint()
        tableOfLabelToPrint()
    return True


def tableOfSymbToPrint():
    print("\n Таблиця символів")
    s1 = '{0:<10s} {1:<10s} {2:<10s} {3:<10s} {4:<5s} '
    s2 = '{0:<10d} {1:<10d} {2:<10s} {3:<10s} {4:<5s} '
    print(s1.format("numRec", "numLine", "lexeme", "token", "index"))
    for numRec in tableOfSymb:  # range(1,lns+1):
        numLine, lexeme, token, index = tableOfSymb[numRec]
        print(s2.format(numRec, numLine, lexeme, token, str(index)))


def tableOfIdToPrint():
    print("\n Таблиця ідентифікаторів")
    s1 = '{0:<10s} {1:<15s} {2:<15s} {3:<10s} '
    print(s1.format("Ident", "Type", "Value", "Index"))
    s2 = '{0:<10s} {2:<15s} {3:<15s} {1:<10d} '
    for id in tableOfId:
        index, type, val = tableOfId[id]
        print(s2.format(id, index, type, str(val)))


def tableOfConstToPrint():
    print("\n Таблиця констант")
    s1 = '{0:<10s} {1:<10s} {2:<10s} {3:<10s} '
    print(s1.format("Const", "Type", "Value", "Index"))
    s2 = '{0:<10s} {2:<10s} {3:<10} {1:<10d} '
    for cnst in tableOfConst:
        index, type, val = tableOfConst[cnst]
        print(s2.format(str(cnst), index, type, val))


def tableOfLabelToPrint():
    if len(tableOfLabel) == 0:
        print("\n Таблиця міток - порожня")
    else:
        s1 = '{0:<10s} {1:<10s} '
        print("\n Таблиця міток")
        print(s1.format("Label", "Value"))
        s2 = '{0:<10s} {1:<10d} '
        for lbl in tableOfLabel:
            val = tableOfLabel[lbl]
            print(s2.format(lbl, val))
#
# # запуск лексичного аналізатора
# lex = Lexema("test.my_lang")
# lex.lex()
#
# # Таблиці: розбору, ідентифікаторів та констант
# print('-' * 30)
# print('tableOfSymb:{0}'.format(tableOfSymb))
# print('tableOfId:{0}'.format(tableOfId))
# print('tableOfConst:{0}'.format(tableOfConst))
# # print('tableOfMark:{0}'.format(tableOfMark))
