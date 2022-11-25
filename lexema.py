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
       (1, ':'):14, (14, 'other'): 15,
       (0, 'other'): 101
       }

initState = 0  # q0 - стартовий стан
F = {2, 4, 7, 8, 9, 11, 13, 15, 101, 102, 103}  # множина заключних станiв
Fstar = {2, 4, 7, 13, 15}  # зiрочка
Ferror = {101, 102, 103}  # обробка помилок

# Таблиця лексем мови
tableOfLanguageTokens = {'end': 'keyword', 'int': 'keyword', 'real': 'keyword', 'bool': 'keyword',
                         'true': 'boolval', 'false': 'boolval', 'read': 'keyword', 'write': 'keyword', 'for': 'keyword',
                         'to': 'keyword', 'do': 'keyword', 'if': 'keyword', 'goto': 'keyword',
                         '=': 'assign_op', '.': 'punct', ':': 'punct', ';': 'punct', ',': 'punct',
                         ' ': 'ws', '\t': 'ws', '\n': 'nl',
                         '-': 'add_op', '+': 'add_op', '*': 'mult_op', '/': 'mult_op',
                         'div': 'mult_op', '^': 'pow_op', '(': 'brackets_op', ')': 'brackets_op',
                         '<': 'rel_op', '>': 'rel_op', '<=': 'rel_op', '>=': 'rel_op', '==': 'rel_op', '!=': 'rel_op'}

# Решту токенiв визначаємо не за лексемою, а за заключним станом
tableIdentFloatInt = {2: 'ident', 4: 'int', 7: 'real', 15:'mark'}

tableOfId={}   # Таблиця ідентифікаторів
tableOfConst={} # Таблиць констант
tableOfSymb={}  # Таблиця символів програми (таблиця розбору)


class Lexema:
    def __init__(self, name_file):
        f = open(name_file, 'r')
        self.sourceCode = f.read()
        f.close()
        self.FSucces = (True, 'Lexer')
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
            else:  # якщо keyword
                print('{0:<3d} {1:<10s} {2:<10s} '.format(self.numLine, self.lexeme, token))
                tableOfSymb[len(tableOfSymb) + 1] = (self.numLine, self.lexeme, token, '')
            self.lexeme = ''
            self.numChar = self.putCharBack()  # зірочка
            self.state = initState
        if self.state in (9, 11, 13):
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
        if token == 'ident':
            indx = tableOfId.get(self.lexeme)
            if indx is None:
                indx = len(tableOfId) + 1
                tableOfId[self.lexeme] = indx
        if token == 'boolval' or self.state == 4 or self.state == 7:
            indx = tableOfConst.get(self.lexeme)
            if indx is None:
                indx = len(tableOfConst) + 1
                tableOfConst[self.lexeme] = indx
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
        try:
            while self.numChar < self.lenCode:
                self.char = self.nextChar()  # прочитати наступний символ
                self.state = self.nextState(self.classOfChar())  # обчислити наступний стан
                if self.is_final():  # якщо стан заключний
                    self.processing()  # виконати семантичні процедури
                # if state in Ferror:	    # якщо це стан обробки помилки
                # break					#      то припинити подальшу обробку
                elif self.state == initState:
                    self.lexeme = ''  # якщо стан НЕ заключний, а стартовий - нова лексема
                else:
                    self.lexeme += self.char  # якщо стан НЕ закл. і не стартовий - додати символ до лексеми
            print('Lexer: Лексичний аналіз завершено успішно')
        except SystemExit as e:
            # Встановити ознаку неуспішності
            self.FSucces = (False, 'Lexer')
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


# запуск лексичного аналізатора
# lex = Lexema("test3.my_lang")
# lex.lex()

# Таблиці: розбору, ідентифікаторів та констант
print('-' * 30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('tableOfId:{0}'.format(tableOfId))
print('tableOfConst:{0}'.format(tableOfConst))