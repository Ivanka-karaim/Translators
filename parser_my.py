from lexema import Lexema
from lexema import tableOfSymb, tableToPrint, FSuccess, tableOfId, tableOfConst
from lexema import tableOfLabel

postfixCode = []
toView = False
class Parser:
    def __init__(self):
        self.numRow = 1

        # print('-' * 30)
        # print('tableOfSymb:{0}'.format(tableOfSymb))
        # print('-' * 30)
        # довжина таблиці символів програми
        # він же - номер останнього запису
        self.len_tableOfSymb = 0
        self.lex = ''



        # print(('len_tableOfSymb', self.len_tableOfSymb))

    # Прочитати з таблицi розбору поточний запис за його номером numRow
    # Повернути номер рядка програми, лексему та її токен

    def postfixTranslator(self, name):
        global len_tableOfSymb, FSuccess
        self.lex = Lexema(name)
        self.lex.lex()
        self.len_tableOfSymb = len(tableOfSymb)
        # print(tableOfId)

        # чи був успішним лексичний розбір
        if (True, 'Lexer') == FSuccess:
            FSuccess = self.parseProgram()
            self.serv()
            return FSuccess

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
            # print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lexeme, token)))
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
            # print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine, token))
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

            # повідомити про успішність
            # синтаксичного аналізу
            # та трансляції програми ПОЛІЗ
            print('Translator: Переклад у ПОЛІЗ та синтаксичний аналіз завершились успішно')
            FSuccess = (True, 'Translator')
            return FSuccess
            # print('Parser: Синтаксичний аналіз завершився успішно')
            # return True
        # в разі виклику функції exit() обробити її
        except SystemExit as e:
            print('Parser: Аварійне завершення програми з кодом {0}'.format(e))

    # оголошення змінних
    def parseDeclarList(self):
        # print("parseDeclarList():")
        numTabs = 1
        while self.parseDeclaration(numTabs):
            pass
        return True

    def parseDeclaration(self, numTabs):
        # якщо всi записи таблицi розбору прочитанi
        if self.numRow > self.len_tableOfSymb:
            return False
        # print('\t' * numTabs + 'parseDeclaration:')
        numTabs += 1
        # перевірка на наявність типу
        numLine, lex, tok = self.getSymb()

        if self.parseType(numTabs):
            # print(523)
            # перевіряє правильність запису ідентифікаторів
            self.parseIdentList(numTabs, lex)
            # перевіряє наявність ; в кінці оголошення
            self.parseLexToken(";", "punct", '\t' * numTabs)
            return True
        # якщо це не тип, то тоді оголошення завершено
        else:
            return False

    def parseType(self, numTabs):
        # прочитати з таблицi розбору
        # номер рядка програми, лексему та її токен
        # self.numRow -= 1
        numLine, lex, token = self.getSymb()
        # перевірити чи лексема відповідає якомусь з типів
        if lex in ['int', 'real', 'bool'] and token == "keyword":
            # print("\t" * numTabs + "parseType():")
            numTabs += 1
            self.numRow += 1
            # print("\t" * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, token)))
            return True
        else:
            return False

    def parseIdentList(self, numTabs, type):
        # print("\t" * numTabs + "parseIdentList():")
        # print(tableOfId)
        numTabs += 1
        # перевірка на наявність хоча б одного ідентифікатора
        numLine, lex, tok = self.getSymb()

        if not self.parseToken("ident", '\t' * numTabs):
            numLine, lex, token = self.getSymb()
            # помилка невідповідність в IdentList
            self.failParse('невідповідність в IdentList', (numLine, lex, token, 'ident'))
        # поки зустрічається кома між ідентифікаторами
        num, types, val = tableOfId.get(lex)
        if not types == "type_undef":
            print("error")
            pass
        tableOfId[lex] = (num, type, val)

        while self.getSymb()[1] == "," and self.getSymb()[2] == "punct":
            self.parseLexToken(",", "punct", "\t" * numTabs)
            # перевірка на наявність ідентифікатора
            numLine, lex, tok = self.getSymb()
            if not self.parseToken("ident", '\t' * numTabs):
                numLine, lex, token = self.getSymb()
                self.failParse('невідповідність в IdentList', (numLine, lex, token, 'ident'))
            num, types, val = tableOfId.get(lex)
            if not types == "type_undef":
                print("error")
                pass
            tableOfId[lex] = (num, type, val)
        return True



    def parseStatemetList(self, numTabs=0):
        # print("\t" * numTabs + "parseStatementList():")
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
        # print("\t" * numTabs + 'parseStatement():')
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
            # print(525442)
            tableOfLabel[lex.split(":")[0]] = len(postfixCode)
            postfixCode.append((lex.split(":")[0], token))
            self.numRow+=1
            # self.parseToken("mark", "\t" * numTabs)
            return True
        # якщо лексема - ключове слово 'end'
        # i воно знаходиться в інструкції повторень
        # вийти з Statement
        elif lex == 'end' and numTabs > 3:
            return False
        else:
            self.failParse('невідповідність інструкцій', (numLine, lex, token, 'ident, read, write, for, if or mark'))

    def parseAssign(self, numTabs):
        global toView, postfixCode
        # print("\t" * numTabs + "parseAssign():")
        numTabs += 1
        # взяти поточну лексему
        numLine, lex, tok = self.getSymb()

        postfixCode.append((lex, tok))

        if toView: self.configToPrint(lex, self.numRow)
        # встановити номер нової поточної лексеми
        self.numRow += 1
        # print('\t' * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        # перевірка оператора присвоювання
        if self.parseLexToken("=", "assign_op", "\t" * numTabs):

            # розбір виразу
            self.parseExpression(numTabs)

            postfixCode.append(('=', 'assign_op'))
            if toView: self.configToPrint('=', self.numRow)
            return True
        else:
            return False

    def parseArithmExpression(self, numTabs):
        # print("\t" * numTabs + "parseArithExpression():")
        numTabs += 1
        # може зустрічатись знак
        # self.parseToken("add_op", "\t" * numTabs)
        x = None
        numLine, lex, tok = self.getSymb()

        if lex == '-' and tok == 'add_op':
            x = ("NEG", "neg")
            self.numRow += 1
        # якщо не Term то це не арифметичний оператор
        if not self.parseTerm(numTabs):
            return False
        if x is not None:
            postfixCode.append(x)
        # поки зустрічається add_op Term,
        # доти розглядається арифметичний оператор
        # while self.parseToken("add_op", "\t" * numTabs) and self.parseTerm(numTabs):
        #
        #     pass
        F = True
        while F:
            numLine, lex, tok = self.getSymb()
            if tok in ('add_op'):
                self.numRow += 1
                # print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
                self.parseTerm(numTabs)  # Трансляція (тут нічого не робити)
                # ця функція сама згенерує
                # та додасть ПОЛІЗ доданка

                # Трансляція
                postfixCode.append((lex, tok))
                # lex - бінарний оператор  '+' чи '-'
                # додається після своїх операндів
                if toView: self.configToPrint(lex, self.numRow)
            else:
                F = False
        return True
        # return True


    def parseTerm(self, numTabs):
        # print("\t" * numTabs + "parseTerm():")
        numTabs += 1
        # якщо не Factor то це не Term
        if not self.parseFactor(numTabs):
            return False
        F = True
        # продовжувати розбирати Множники (Factor)
        # розділені лексемами '*' або '/'
        while F:
            _numLine, lex, tok = self.getSymb()
            if tok in ('mult_op'):
                self.numRow += 1
                # print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
                self.parseFactor(numTabs)  # Трансляція (тут нічого не робити)
                # ця функція сама згенерує та додасть ПОЛІЗ множника

                # Трансляція
                postfixCode.append((lex, tok))
                # lex - бінарний оператор  '*' чи '/'
                # додається після своїх операндів
                if toView: self.configToPrint(lex, self.numRow)
            elif tok in ('pow_op'):
                self.numRow += 1
                self.parseFactor(numTabs)
                i = 1
                while self.parseToken('pow_op', '\t'*numTabs) and self.parseFactor(numTabs):
                    i += 1
                for j in range(i):
                    postfixCode.append(("^", "pow_op"))



            else:
                F = False
        # while (self.parseToken("mult_op", "\t" * numTabs) or self.parseToken("pow_op",
        #                                                                      "\t" * numTabs)) and self.parseFactor(
        #     numTabs):
        #     pass
        return True

    def parseFactor(self, numTabs):
        # print("\t" * numTabs + "parseFactor():")
        numTabs += 1
        numLine, lex, token = self.getSymb()
        # перевірка констант та ідентифікаторів
        if token in ['int', 'real', 'ident']:
            postfixCode.append((lex,token))      # Трансляція
                                # ПОЛІЗ константи або ідентифікатора
                                # відповідна константа або ідентифікатор
            if toView: self.configToPrint(lex,self.numRow)
            self.numRow += 1
            # print("\t" * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, token)))
        elif token == 'boolval':
            self.numRow -= 1
            if self.getSymb()[2] == 'rel_op':
                postfixCode.append((lex, token))  # Трансляція
                # ПОЛІЗ константи або ідентифікатора
                # відповідна константа або ідентифікатор
                if toView: self.configToPrint(lex, self.numRow)
                self.numRow += 1
                # print("\t" * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, token)))
            self.numRow += 1
        # якщо зустрічається дужка, то викликається арифметичний оператор
        elif lex == '(':
            self.numRow += 1
            # print("\t" * numTabs + 'в рядку {0} - {1}'.format(numLine, (lex, token)))
            self.parseExpression(numTabs)
            self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        else:
            self.failParse("невідповідність у Expression.Factor",
                           (numLine, lex, token, 'int | real | boolval | ident | ('))
        return True

    def parseExpression(self, numTabs):
        # print("\t" * numTabs + "parseExpression():")
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
        # print("\t" * numTabs + "parseIf():")
        numTabs += 1
        # перевірка ключового слова if
        if self.parseLexToken("if", "keyword", "\t" * numTabs):
            self.parseBoolExpression(numTabs)
            # перевірка ключового слова goto
            # m = self.createLabel()
            # postfixCode.append(m)
            # postfixCode.append(("JF", "jf"))
            self.parseLexToken("goto", "keyword", "\t" * numTabs)

            self.createGotoLabel()
            self.parseToken('ident', '\t' * numTabs)
            # self.setValueToLabel(m)
            return True

        return False

    def createGotoLabel(self):
        numLine, lex, tok = self.getSymb()
        if tok == 'ident':
            # tableOfLabel[lex] = 'val_undef'
            print(tableOfId)
            if lex in tableOfId:
                tableOfId.pop(lex)
            tableOfSymb[self.numRow] = (numLine, lex, "mark", '')
        self.numRow += 1
        postfixCode.append((lex, "mark"))
        postfixCode.append(("JF", "jf"))
        return lex, "mark"

    def createLabel(self):
        num = len(tableOfLabel)+1
        lex = "m"+str(num)
        if lex not in tableOfLabel:
            tableOfLabel[lex] = 'val_undef'
        return lex, "mark"

    def setValueToLabel(self, lbl):
        lex, _tok = lbl
        tableOfLabel[lex] = len(postfixCode)


    def parseFor(self, numTabs):
        # print("\t" * numTabs + "parseFor():")
        numTabs += 1
        # перевірка ключого слова for
        tableOfId["value_step"] = (len(tableOfId) + 1, "int", 1)
        count = self.numRow


        self.parseLexToken("for", "keyword", "\t" * numTabs)
        self.parseToken("ident", "\t"*numTabs)
        self.parseLexToken("=", "assign_op", "\t" * numTabs)
        self.parseArithmExpression(numTabs)
        self.parseLexToken("to", "keyword", "\t" * numTabs)

        self.parseArithmExpression(numTabs)
        postfixCode.append(("<", "rel_op"))
        mark = self.createLabel()
        postfixCode.append((mark[0], mark[1]))
        postfixCode.append(("JF", "jf"))

        postfixCode.append(("value_step", "ident"))
        tableOfConst["-1"] = (len(tableOfConst)+1, "int", -1)
        postfixCode.append(("-1", "int"))
        postfixCode.append(("=", "assign_op"))
        self.setValueToLabel(mark)

        self.numRow = count
        ############################################
        self.parseLexToken("for", "keyword", "\t" * numTabs)
        # перевірка наявності ідентифікатора
        numLine, lex, tok = self.getSymb()
        if self.parseToken("ident", "\t" * numTabs):
            postfixCode.append((lex, tok))

        # перевірка оператора присвоювання
        self.parseLexToken("=", "assign_op", "\t" * numTabs)
        # виклик фунції арифметичний вираз
        self.parseArithmExpression(numTabs)
        postfixCode.append(("=", "assign_op"))

        tableOfId["r1"] = (len(tableOfId)+1, "int", 0)
        if "0" not in tableOfConst:
            tableOfConst["0"] = (len(tableOfId)+1, "int", 0)
        postfixCode.append(("r1", "ident"))
        postfixCode.append(("1", "int"))
        postfixCode.append(("=", "assign_op"))

        m1 = self.createLabel()
        postfixCode.append((m1[0], m1[1]))
        postfixCode.append((":", "punct"))
        tableOfId["r2"] = (len(tableOfId) + 1, "int", 0)
        self.setValueToLabel(m1)
        postfixCode.append(("r2", "ident"))

        postfixCode.append(("value_step", "ident"))

        self.parseLexToken("to", "keyword", "\t" * numTabs)
        postfixCode.append(("=", "assign_op"))
        postfixCode.append(("r1", "ident"))
        postfixCode.append(("0", "int"))
        postfixCode.append(("!=", "rel_op"))
        m2 = self.createLabel()
        postfixCode.append((m2[0], m2[1]))
        postfixCode.append(("JF", "jf"))
        postfixCode.append((lex, tok))
        postfixCode.append((lex, tok))
        postfixCode.append(("r2", "ident"))
        postfixCode.append(("+", "add_op"))
        postfixCode.append(("=", "assign_op"))
        postfixCode.append((m2[0], m2[1]))
        postfixCode.append((":", "punct"))
        self.setValueToLabel(m2)
        postfixCode.append(("r1", "ident"))
        postfixCode.append(("0", "int"))
        postfixCode.append(("=", "assign_op"))
        postfixCode.append((lex, tok))

        self.parseArithmExpression(numTabs)
        self.parseLexToken("do", "keyword", "\t" * numTabs)
        postfixCode.append(("-", "add_op"))
        postfixCode.append(("r2", "ident"))
        postfixCode.append(("*", "mult_op"))
        postfixCode.append(("0", "int"))
        postfixCode.append((">=", "rel_op"))
        m3 = self.createLabel()
        postfixCode.append((m3[0], m3[1]))
        postfixCode.append(("JF", "jf"))

        self.parseStatemetList(numTabs)
        self.parseLexToken("end", "keyword", "\t" * numTabs)

        postfixCode.append((m1[0], m1[1]))
        postfixCode.append(("JUMP", "jump"))
        postfixCode.append((m3[0], m3[1]))
        postfixCode.append((":", "punct"))
        self.setValueToLabel(m3)


        # перевірка ключого слова to


        # виклик фунції арифметичний вираз


        return True

    # def parseFor(self, numTabs):
    #     # print("\t" * numTabs + "parseFor():")
    #     numTabs += 1
    #     # перевірка ключого слова for
    #     self.parseLexToken("for", "keyword", "\t" * numTabs)
    #     # перевірка наявності ідентифікатора
    #     numLine, lex, tok = self.getSymb()
    #     if self.parseToken("ident", "\t" * numTabs):
    #         postfixCode.append((lex, tok))
    #
    #     # перевірка оператора присвоювання
    #     self.parseLexToken("=", "assign_op", "\t" * numTabs)
    #     # виклик фунції арифметичний вираз
    #     self.parseArithmExpression(numTabs)
    #     postfixCode.append(("=", "assign_op"))
    #
    #     tableOfId["r1"] = (len(tableOfId)+1, "int", 0)
    #     if "0" not in tableOfConst:
    #         tableOfConst["0"] = (len(tableOfId)+1, "int", 0)
    #     postfixCode.append(("r1", "ident"))
    #     tableOfId["value_step"] = (len(tableOfId)+1, "int", 1)
    #     postfixCode.append(("value_step", "ident"))
    #     postfixCode.append(("=", "assign_op"))
    #     m = self.createLabel()
    #     postfixCode.append((m[0], m[1]))
    #     postfixCode.append((":", "punct"))
    #     self.setValueToLabel(m)
    #
    #     # перевірка ключого слова to
    #     self.parseLexToken("to", "keyword", "\t" * numTabs)
    #     postfixCode.append(("r1", "ident"))
    #     # виклик фунції арифметичний вираз
    #     self.parseArithmExpression(numTabs)
    #     postfixCode.append((lex, tok))
    #     postfixCode.append(("-", "add_op"))
    #     postfixCode.append(("*", "mult_op"))
    #     postfixCode.append(("0", "int"))
    #     postfixCode.append((">", "rel_op"))
    #     m2 = self.createLabel()
    #     postfixCode.append((m2[0], m2[1]))
    #     postfixCode.append(("JF", "jf"))
    #     # перевірка ключого слова do
    #     self.parseLexToken("do", "keyword", "\t" * numTabs)
    #     # перевірка списку інструкцій
    #     self.parseStatemetList(numTabs)
    #     postfixCode.append((lex, tok))
    #     postfixCode.append((lex, tok))
    #     postfixCode.append(("r1", "ident"))
    #     postfixCode.append(("+", "add_op"))
    #     postfixCode.append(("=", "assign_op"))
    #     postfixCode.append((m[0], m[1]))
    #     postfixCode.append(("JUMP", "jump"))
    #     # перевірка ключого слова end
    #     self.parseLexToken("end", "keyword", "\t" * numTabs)
    #     self.setValueToLabel(m2)
    #     postfixCode.append((m2[0], m2[1]))
    #     postfixCode.append((":", "punct"))
    #
    #
    #     return True



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
        # print('\t' * numTabs + 'parseBoolExpression():')
        numTabs += 1
        # перевірка на наявність булевого виразу
        if self.parseBoolPart(numTabs):
            # поки є оператор
            while True:
                numLine, lex, tok = self.getSymb()
                if tok == 'rel_op':

                    self.numRow += 1
                    self.parseBoolPart(numTabs+1)
                    postfixCode.append((lex, tok))
                else:
                    break
        return True

            # while self.parseToken('rel_op', '\t' * numTabs):
            #     # виконувати булевий вираз
            #     self.parseBoolPart(numTabs + 1)
            # return True
        # повідомлення про відсутність логічного виразу
        # print('\t'*numTabs + '-Not a BoolExpression-')
        # return False

    def parseBoolPart(self, numTabs):
        global postfixCode
        # print('\t' * numTabs + 'parseBoolPart():')
        numTabs += 1
        # читання поточного елемента
        numLine, lex, tok = self.getSymb()
        # перевірка чи є цей елемент boolval
        count = len(postfixCode)
        if lex in ('true', 'false') and tok == 'boolval':
            # self.parseLexToken(lex, 'boolval', '\t' * numTabs)
            postfixCode.append((lex, tok))
            self.numRow += 1
            return True

        # перевірка чи є цей елемент арифметичним виразом
        elif self.parseArithmExpression(numTabs):

            numLine, lex, tok = self.getSymb()
            # перевірка на наявність булевого оператора
            if tok == 'rel_op':
                # self.parseLexToken(lex, 'rel_op', '\t' * numTabs)

                self.numRow += 1
                # перевірка арифметичного оператора
                if self.parseArithmExpression(numTabs):
                    postfixCode.append((lex, tok))
                    return True
            else:
                # post = []
                # i = 0
                # while i < count:
                #     post.append(postfixCode[i])
                #     i += 1
                # postfixCode = post
                return False
        else:

            return False

    def parseInp(self, numTabs):
        # print("\t" * numTabs + "parseRead():")
        numTabs += 1
        # перевірка ключового слова read
        self.parseLexToken("read", "keyword", "\t" * numTabs)
        # перевірка наявності дужки
        self.parseLexToken("(", "brackets_op", "\t"*numTabs)
        # перевірка списку ідентифікаторів
        numLine, lex, tok = self.getSymb()
        if not self.parseToken('ident', '\t'*numTabs):
            return False
        postfixCode.append((lex, tok))
        postfixCode.append(("IN", "in"))
        while self.getSymb()[1] == ',' and self.getSymb()[2] == 'punct':
            self.parseLexToken(',', 'punct', '\t'*numTabs)
            numLine,  lex, tok = self.getSymb()
            if not self.parseToken('ident', '\t'*numTabs):
                numLine, lex, tok = self.getSymb()
                self.failParse('невідповідність в IdentList', (numLine, lex, tok, 'ident'))
            postfixCode.append((lex, tok))
            postfixCode.append(("IN", "in"))

        # self.parseIdentList(numTabs)
        # перевірка наявності дужки
        self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        return True

    def parseOut(self, numTabs):
        # print("\t" * numTabs + "parseWrite():")
        numTabs += 1
        # перевірка ключового слова write
        self.parseLexToken("write", "keyword", "\t" * numTabs)
        # перевірка наявності дужки
        self.parseLexToken("(", "brackets_op", "\t" * numTabs)
        # перевірка списку ідентифікаторів
        numLine, lex, tok = self.getSymb()
        if not self.parseToken('ident', '\t' * numTabs):
            return False
        postfixCode.append((lex, tok))
        postfixCode.append(("OUT", "out"))
        while self.getSymb()[1] == ',' and self.getSymb()[2] == 'punct':
            self.parseLexToken(',', 'punct', '\t' * numTabs)
            numLine, lex, tok = self.getSymb()
            if not self.parseToken('ident', '\t' * numTabs):
                numLine, lex, tok = self.getSymb()
                self.failParse('невідповідність в IdentList', (numLine, lex, tok, 'ident'))
            postfixCode.append((lex, tok))
            postfixCode.append(("OUT", "out"))
        # self.parseIdentList(numTabs)
        # перевірка наявності дужки
        self.parseLexToken(")", "brackets_op", "\t" * numTabs)
        return True

    def serv(self):
        global postfixCode
        # tableToPrint('All')
        tableToPrint('Label')
        tableToPrint('Id')
        print('\nПочатковий код програми: \n{0}'.format(self.lex.getSourceCode()))
        print('\nКод програми у постфіксній формі (ПОЛІЗ): \n{0}'.format(postfixCode))
        # for lbl in tableOfLabel:
        #     print('postfixCode[{0}:{1}]={2}'.format(lbl, tableOfLabel[lbl], postfixCode[tableOfLabel[lbl]]))
        return True

    def configToPrint(self,lex, numRow):
        stage = '\nКрок трансляції\n'
        stage += 'лексема: \'{0}\'\n'
        stage += 'tableOfSymb[{1}] = {2}\n'
        stage += 'postfixCode = {3}\n'
        # tpl = (lex,numRow,str(tableOfSymb[numRow]),str(postfixCode))
        print(stage.format(lex, numRow, str(tableOfSymb[numRow]), str(postfixCode)))


# parser = Parser("test3.my_lang")
# parser.parseProgram()
# parser = Parser()
# parser.postfixTranslator("test3.my_lang")

