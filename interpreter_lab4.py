from parser_my import  Parser, tableOfId, tableOfConst, postfixCode, tableOfLabel
from lexema import tableToPrint
from stack01 import Stack
parser = Parser()
stack = Stack()

toView = True

def postfixInterpreter(name):

    FSuccess = parser.postfixTranslator(name)
    # чи була успішною трансляція
    if (True,'Translator') == FSuccess:
        print(tableOfConst)
        print('\nПостфіксний код: \n{0}'.format(postfixCode))
        return postfixProcessing()
    else:
        # Повідомити про факт виявлення помилки
        print('Interpreter: Translator завершив роботу аварійно')
        return False

print('-'*30)

def postfixProcessing():
    global stack, postfixCode
    maxNumb=len(postfixCode)
    try:
        i = 0
        while i < maxNumb:

            lex,tok = postfixCode[i]
            print(lex)
            if tok in ('int','float','ident', 'boolval', 'mark'):
               stack.push((lex,tok))

            elif tok == "neg":
                doInvertValue()

            elif tok == "out":
                doPrint()

            elif tok == "in":
                doInput()

            elif tok in ["jf", "punct", "jump"]:

                value = doJumps(lex, tok, i)
                i = value
                print(i)
            else:
                doIt(lex,tok)

            if toView: configToPrint(i+1,lex,tok,maxNumb)
            i += 1

        return True
    except SystemExit as e:
        # Повідомити про факт виявлення помилки
        print('RunTime: Аварійне завершення програми з кодом {0}'.format(e))
    return True

def doJumps(lex, tok, iterationNum):
    next = 0
    if tok == "jump":
        (lexLabel, tokLabel) = stack.pop()
        next = tableOfLabel[lexLabel] - 1
    elif tok == "punct":
        stack.pop()
        next = iterationNum
    elif tok == "jf":
        (lexLabel, tokLabel) = stack.pop()
        (lexExpr, tokExpr) = stack.pop()
        print(lexExpr)
        value = lexExpr
        print(value)
        if value == "true":
            next = tableOfLabel[lexLabel] - 1
        else:
            next = iterationNum

    return next



def doInput():
    (lex, tok) = stack.pop()
    (index, type, v) = tableOfId[lex]
    if type == 'type_undef':
        failRunTime('неініціалізована змінна', (lex, tableOfId[lex], (lex, tok), lex, (lex, tok)))
    else:
        value = input()
        if type == "int":
            value = int(value)
        elif type == "real":
            value = float(value)
        elif type == "bool":
            value = bool(value)

        tableOfId[lex] = (index, type, value)


def doInvertValue():
    (lex, tok) = stack.pop()
    ( index, type, value) = tableOfConst.get(lex)
    print(index)
    if type == 'type_undef':
        failRunTime('неініціалізована змінна', (lex, tableOfId[lex], (lex, tok), lex, (lex, tok)))
    elif value == 'val_undef':
        failRunTime('неініціалізована змінна', (lex, tableOfId[lex], (lex, tok), lex, (lex, tok)))
    elif isinstance(value, int) or isinstance(value, float) :
        value = -value
        if str(value) not in tableOfConst:
            tableOfConst[str(value)] = (len(tableOfConst)+1, type, value)
        stack.push((str(value), type))
        return True
    else:
        print("error")

def doPrint():
    (lex, tok) = stack.pop()
    (index, type, value) = tableOfId[lex]
    if type == 'type_undef':
        failRunTime('неініціалізована змінна', (lex, tableOfId[lex], (lex, tok), lex, (lex, tok)))
    elif value == 'val_undef':
        failRunTime('неініціалізована змінна', (lex, tableOfId[lex], (lex, tok), lex, (lex, tok)))
    else:
        print(lex+" = "+str(value))
        return True

def configToPrint(step,lex,tok,maxN):
    if step == 1:
        print('='*30+'\nInterpreter run\n')
        tableToPrint('All')

    print('\nКрок інтерпретації: {0}'.format(step))
    if tok in ('int','float'):
        print('Лексема: {0} у таблиці констант: {1}'.format((lex,tok),lex + ':' +str(tableOfConst[lex])))
    elif tok in ('ident'):
        print('Лексема: {0} у таблиці ідентифікаторів: {1}'.format((lex,tok),lex + ':' +str(tableOfId[lex])))
    else:
        print('Лексема: {0}'.format((lex,tok)))

    print('postfixCode={0}'.format(postfixCode))
    stack.print()

    if  step == maxN:
            for Tbl in ('Id','Const','Label'):
                tableToPrint(Tbl)
    return True





def doIt(lex,tok):
    global stack, postfixCode, tableOfId, tableOfConst, tableOfLabel
    if (lex,tok) == ('=', 'assign_op'):
        # зняти з вершини стека запис (правий операнд = число)
        (lexL,tokL) = stack.pop()

        # зняти з вершини стека ідентифікатор (лівий операнд)
        (lexR,tokR) = stack.pop()

        # виконати операцію:
        # оновлюємо запис у таблиці ідентифікаторів
        # ідентифікатор/змінна
        # (index не змінюється,
        # тип - як у константи,
        # значення - як у константи)
        # print(tableOfConst[lexL])
        print(lexL)
        if tokL == "ident":
            tableOfId[lexR] = (tableOfId[lexR][0],  tableOfId[lexL][1], tableOfId[lexL][2])
        else:
            tableOfId[lexR] = (tableOfId[lexR][0], tableOfConst[lexL][1], tableOfConst[lexL][2])
    elif tok in ('add_op','mult_op', 'pow_op', 'rel_op'):
        # зняти з вершини стека запис (правий операнд)
        (lexR,tokR) = stack.pop()
        # зняти з вершини стека запис (лівий операнд)
        (lexL,tokL) = stack.pop()
        processing_exception((lexL,tokL),lex,tok, (lexR,tokR))
    # elif tok =='rel_op':
    #     # зняти з вершини стека запис (правий операнд)
    #     (lexR, tokR) = stack.pop()
    #     # зняти з вершини стека запис (лівий операнд)
    #     (lexL, tokL) = stack.pop()
    #     processing_boolexception((lexL,tokL),lex,(lexR,tokR))

    return True

def failRunTime(str,tuple):
    if str == 'невідповідність типів':
        ((lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Типи операндів відрізняються у {0} {1} {2}'.format((lexL,tokL),lex,(lexR,tokR)))
        exit(1)
    elif str == 'неініціалізована змінна':
        (lx,rec,(lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Значення змінної {0}:{1} не визначене. Зустрылось у {2} {3} {4}'.format(lx,rec,(lexL,tokL),lex,(lexR,tokR)))
        exit(2)
    elif str == 'ділення на нуль':
        ((lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Ділення на нуль у {0} {1} {2}. '.format((lexL,tokL),lex,(lexR,tokR)))
        exit(3)


def processing_exception(ltL,lex,tok,ltR):
    global stack, postfixCode, tableOfId, tableOfConst, tableOfLabel
    lexL,tokL = ltL
    lexR,tokR = ltR
    # if (tokL, tokR) in (('int', 'float'), ('float', 'int')):
    #     failRunTime('невідповідність типів', ((lexL, tokL), lex, (lexR, tokR)))
    if tokL == 'ident':
        # print(('===========',tokL , tableOfId[lexL][1]))
        # tokL = tableOfId[lexL][1]
        if tableOfId[lexL][1] == 'type_undef':
            failRunTime('неініціалізована змінна',(lexL,tableOfId[lexL],(lexL,tokL),lex,(lexR,tokR)))
        else:
            valL,tokL = (tableOfId[lexL][2],tableOfId[lexL][1])
    else:
        valL = tableOfConst[lexL][2]
    if tokR == 'ident':
        # print(('===========',tokL , tableOfId[lexL][1]))
        # tokL = tableOfId[lexL][1]
        if tableOfId[lexR][1] == 'type_undef':
            failRunTime('неініціалізована змінна',(lexR,tableOfId[lexR],(lexL,tokL),lex,(lexR,tokR)))
        else:
            valR,tokR = (tableOfId[lexR][2],tableOfId[lexR][1])
    else:
        valR = tableOfConst[lexR][2]
    # if :
        # print(('lexL',lexL,tableOfConst))
        # valL = tableOfConst[lexL][2]
        # valR = tableOfConst[lexR][2]
    if tok == 'rel_op':
        getBoolValue((valL,lexL,tokL),lex,(valR,lexR,tokR))
    else:
        getValue((valL,lexL,tokL),lex,(valR,lexR,tokR))


def getBoolValue(vtL,lex,vtR):
    valL, lexL, tokL = vtL
    valR, lexR, tokR = vtR
    print(lex)
    # print(tokR)
    if (tokL, tokR) in (('int', 'boolval'), ('boolval', 'int'), ('real', 'boolval'), ('boolval', 'real')):
        failRunTime('невідповідність типів', ((lexL, tokL), lex, (lexR, tokR)))
    elif lex == '>':
        value = valL > valR
    elif lex == '<':
        value = valL < valR
    elif lex == '==':
        print(valL)
        print(valR)
        value = valL == valR
    elif lex == '!=':
        value = valL != valR
    elif lex == '>=':
        value = valL >= valR
    elif lex == '<=':
        value = valL <= valR
    else:
        pass
    stack.push((str(value).lower(), "boolval"))
    toTableOfConst(value, tokL)


def getValue(vtL,lex,vtR):
    global stack, postfixCode, tableOfId, tableOfConst, tableOfLabel

    valL,lexL,tokL = vtL
    valR,lexR,tokR = vtR

    if (tokL,tokR) in (('int','real'),('real','int')):
            failRunTime('невідповідність типів',((lexL,tokL),lex,(lexR,tokR)))
    elif lex == '+':
        value = valL + valR
    elif lex == '-':
        value = valL - valR
    elif lex == '*':
        value = valL * valR
    elif lex == '/' and valR ==0:
        failRunTime('ділення на нуль',((lexL,tokL),lex,(lexR,tokR)))
    elif lex == '/' and tokL=='real':
        value = valL / valR
    elif lex == '/' and tokL=='int':
        value = int(valL / valR)
    elif lex == '^':
        value = pow(valL, valR)
    else:
        pass
    stack.push((str(value),tokL))
    toTableOfConst(value,tokL)

        # tableOfId[lexR] = (tableOfId[lexR][0],  tableOfConst[lexL][1], tableOfConst[lexL][2])

def toTableOfConst(val,tok):
    lexeme = str(val)
    indx1=tableOfConst.get(lexeme)
    if indx1 is None:
        indx = len(tableOfConst)+1
        tableOfConst[lexeme]=(indx,tok,val)


postfixInterpreter("test2.my_lang")