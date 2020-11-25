# Hector Noel Leon Quiroz A01251806
# Compilador MeMyself

from scanner import tokens
from CuboSemantico import CuboSemantico
from TablaVariables import TablaVariables
from TablaConstantes import TablaConstantes
from TablaFunciones import TablaFunciones
from Cuadruplos import Cuadruplos
from Direcciones import Direcciones
import ply.yacc as yacc
import sys

dictFunciones = TablaFunciones()
globalVars = TablaVariables()
constantes = TablaConstantes()
cuboSem = CuboSemantico()
cuadruplos = Cuadruplos()
paramCounter = 0

tipoFuncion = ""
tipoVar = ""
nombreFuncion = ""
nombreVar = ""
hasReturn = False
hasFillColor = False
versionControl = []
versionFinal = 0
listaVariables = []
pilaPoper = []
pilaOp = []
pilaTipo = []
pilaSaltos = []
pilaReturn = []
pilaParams = []
pilaLlamadas = []
pilaDim = []
dimCounter = 0
Direccion = {
    "globalint" : Direcciones(2000, 4999),
    "globalfloat" : Direcciones(5000, 7999),
    "globalchar" : Direcciones(8000, 10999),
    "localint": Direcciones(11000, 13999),
    "localfloat": Direcciones(14000, 16999),
    "localchar": Direcciones(17000, 19999),
    "tempint": Direcciones(20000, 22999),
    "tempfloat": Direcciones(23000, 25999),
    "tempchar": Direcciones(26000, 28999),
    "tempbool": Direcciones(29000, 31999),
    "constint": Direcciones(32000, 34999),
    "constfloat": Direcciones(35000, 37999),
    "constchar": Direcciones(38000, 40999),
    "conststring": Direcciones(41000, 43999)
}

precedence = (
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY','DIVIDE'),
    ('right','EQUALS'),
    ('left', 'AND', 'OR'),
    )

def p_PROGRAMA(p):
    '''
    PROGRAMA : PROGRAM ID addProgram SEMICOLON VA FU MAIN LPAREN RPAREN rellenaMain BLOQUE printTables
    VA : VARS addGlobalVars
       | empty
    FU : FUNC FU
       | empty
    '''

def p_VARS(p):
    '''
    VARS : emptyVars VAR VARSA
    VARSA : TIPO COLON ID addVarLista ARREGLO VARSB
    VARSB : COMMA ID addVarLista ARREGLO VARSB
          | SEMICOLON VARSA
          | SEMICOLON
    '''

def p_TIPO(p):
    '''
    TIPO : INT 
         | FLOAT 
         | CHAR
    '''
    global tipoVar
    tipoVar = p[1]

def p_ARREGLO(p):
    '''
    ARREGLO :  LSBRACKET pushParen EXP RSBRACKET popParen pushDim ARREGLO2
            | empty
    ARREGLO2 : LSBRACKET pushParen EXP RSBRACKET pushDim addArreglo popParen
            | addArreglo
    '''

def p_ARREGLOCALL(p):
    '''
    ARREGLOCALL : LSBRACKET pushParen EXP RSBRACKET popParen verifyDim calculateDir ARREGLOC2
            | empty
    ARREGLOC2 : LSBRACKET pushParen EXP RSBRACKET popParen verifyDim calculateDir
            | empty
    '''

def p_TIPOFUNC(p):
    '''
    TIPOFUNC : INT 
             | FLOAT 
             | CHAR 
             | VOID 
    '''
    global tipoFuncion
    tipoFuncion = p[1]

def p_FUNC(p):
    '''
    FUNC :  MODULE TIPOFUNC ID addFunc LPAREN PARAMS addParamsFunc RPAREN SEMICOLON FUNCSB
    FUNCSB : VARS addVarsFunc BLOQUE endFunc
           | addVarsFunc BLOQUE endFunc
    '''

def p_PARAMS(p):
    '''
    PARAMS : emptyVars PARAMSL
           | empty
    PARAMSL : TIPO ID addVarLista
            | PARAMSL COMMA TIPO ID addVarLista
    '''

def p_BLOQUE(p):
    '''
    BLOQUE : LBRACKET BLOQUEA
           | LBRACKET RBRACKET
    BLOQUEA : ESTATUTO BLOQUEA 
            | ESTATUTO RBRACKET
    '''

def p_ESTATUTO(p):
    '''
    ESTATUTO : ASIGNACION 
             | LLAMADA 
             | RETORNO 
             | LECTURA 
             | ESCRITURA 
             | DECISION 
             | REPETICION 
             | FUNCESP
    '''

def p_ASIGNACION(p):
    '''
    ASIGNACION : ID pushPilaOp ARREGLOCALL EQUALS pushEqual EXPRESION popEqual SEMICOLON
    '''

def p_LLAMDA(p):
    '''
    LLAMADA : ID pushEra LPAREN LLAMADAS
            | ID pushEra LPAREN RPAREN SEMICOLON pushGosubLlamada
    LLAMADAS : EXPRESION addParam RPAREN verifyParams SEMICOLON pushGosubLlamada
             | EXPRESION addParam COMMA LLAMADAS 
    '''

def p_RETORNO(p):
    '''
    RETORNO : RETURN LPAREN EXPRESION RPAREN popReturn SEMICOLON 
    '''

def p_LECTURA(p):
    '''
    LECTURA : READ LPAREN LECTURAS
    LECTURAS : ID pushPilaOp COMMA popRead LECTURAS
             | ID pushPilaOp RPAREN SEMICOLON popRead
    '''

def p_ESCRITURA(p):
    '''
    ESCRITURA : WRITE LPAREN ESCRITURAA
    ESCRITURAA : C_STRING pushConstString COMMA popWrite ESCRITURAA
               | C_STRING pushConstString RPAREN SEMICOLON popWrite addWriteEnd
               | EXPRESION COMMA popWrite ESCRITURAA
               | EXPRESION RPAREN SEMICOLON popWrite addWriteEnd
    '''

def p_DECISION(p):
    '''
    DECISION : IF LPAREN EXPRESION RPAREN pushGotoF THEN BLOQUE SINO
    SINO : ELSE rellenarFalso BLOQUE rellenarSalida
         | empty rellenarSalida
    '''
def p_REPETICION(p):
    '''
    REPETICION : COND 
               | NOCOND
    COND : WHILE pushSalto LPAREN EXPRESION RPAREN pushGotoF DO BLOQUE rellenarWhile
    NOCOND : FROM ID pushFromId EQUALS EXPRESION pushVC TO EXPRESION pushVF DO BLOQUE rellenaFrom
    '''

def p_EXPRESION(p):
    '''
    EXPRESION : EXP popCondition
              | EXP GREATER_THAN pushCondition EXPRESION
              | EXP LESS_THAN pushCondition EXPRESION
              | EXP NOT_EQUAL pushCondition EXPRESION 
              | EXP AND pushCondition EXPRESION 
              | EXP OR pushCondition EXPRESION 
              | EXP IS_EQUAL pushCondition EXPRESION 
    '''

def p_EXP(p):
    '''
    EXP : TERMINO popPlusMinus
        | TERMINO popPlusMinus PLUS pushPlusMinus EXP 
        | TERMINO popPlusMinus MINUS pushPlusMinus EXP 
    '''

def p_TERMINO(p):
    '''
    TERMINO : FACTOR popMultDiv
            | FACTOR popMultDiv MULTIPLY pushMultDiv TERMINO 
            | FACTOR popMultDiv DIVIDE pushMultDiv TERMINO 
    '''

def p_FACTOR(p):
    '''
    FACTOR : LPAREN pushParen EXPRESION RPAREN popParen
           | VARCTE
           | LLAMADAMOD
    '''

def p_LLAMADAMOD(p):
    '''
    LLAMADAMOD : ID pushEra LPAREN pushParen LLAMADAMODS
               | ID pushEra LPAREN pushParen RPAREN pushGosub
    LLAMADAMODS : EXPRESION addParam RPAREN popParen verifyParams pushGosub
                | EXPRESION addParam COMMA LLAMADAMODS
    '''

def p_VARCTE(p):
    '''
    VARCTE : ID pushPilaOp ARREGLOCALL
           | C_INT pushConstInt
           | C_FLOAT pushConstFloat
           | C_CHAR pushConstChar
    '''

def p_FUNCESP(p):
    '''
    FUNCESP : FLINE 
            | FPOINT 
            | FCIRCLE 
            | FARC 
            | FPENUP 
            | FPENDOWN 
            | FCOLOR 
            | FSIZE 
            | FCLEAR
    '''

def p_FLINE(p):
    '''
    FLINE : LINE LPAREN EXPRESION COMMA EXPRESION RPAREN popLine SEMICOLON 
    '''

def p_FILLCOLOR(p):
    '''
    FILLCOLOR : COMMA C_STRING pushConstString hasColor
            |  empty
    '''

def p_FPOINT(p):
    '''
    FPOINT : POINT LPAREN EXPRESION FILLCOLOR RPAREN popPoint SEMICOLON 
    '''

def p_FCIRCLE(p):
    '''
    FCIRCLE : CIRCLE LPAREN EXPRESION FILLCOLOR RPAREN popCircle SEMICOLON 
    '''

def p_FARC(p):
    '''
    FARC : ARC LPAREN EXPRESION COMMA EXPRESION FILLCOLOR RPAREN popArc SEMICOLON 
    '''

def p_FPENUP(p):
    '''
    FPENUP : PENUP LPAREN RPAREN popPenup SEMICOLON 
    '''

def p_FPENDOWN(p):
    '''
    FPENDOWN : PENDOWN LPAREN EXPRESION COMMA EXPRESION RPAREN popPendown SEMICOLON 
    '''

def p_FCOLOR(p):
    '''
    FCOLOR : COLOR LPAREN C_STRING pushConstString RPAREN popColor SEMICOLON 
    '''

def p_FSIZE(p):
    '''
    FSIZE : SIZE LPAREN EXPRESION COMMA EXPRESION RPAREN popSize SEMICOLON 
    '''

def p_FCLEAR(p):
    '''
    FCLEAR : CLEAR LPAREN RPAREN popClear SEMICOLON 
    '''

def p_empty(p):
    '''
    empty :
    '''

# Crea un nuevo cuádruplo "goto", agrega el nombre del programa al diccionario de variables globales.
def p_addProgram(p):
    '''addProgram : '''
    global cuadruplos
    nombreP = p[-1]
    cuadruplos.addCuadruplo("goto", -1, -1, -2)
    dictFunciones.agregarFuncion(nombreP, "void", 0, 0)

# Borra todos los elementos de la lista "listaVariables".
def p_emptyVars(p):
    ''' emptyVars : '''
    global listaVariables
    del listaVariables[:]

# Agrega el id y tipo de una variable a la lista "listaVariables".
def p_addVarLista(p):
    '''addVarLista : '''
    global listaVariables
    global nombreVar
    global tipoVar
    nombreVar = p[-1]
    listaVariables.append([nombreVar, tipoVar, False, 0, 0])

# Guarda el id de la función en el diccionario de funciones y agrega una 
# nueva variable con el id de la funciona al diccionario de variables globales.
def p_addFunc(p):
    '''addFunc : '''
    global dictFunciones
    global nombreFuncion
    global tipoFuncion
    global cuadruplos
    nombreFuncion = p[-1]
    dirGlobal = 0
    if not globalVars.varExiste(nombreFuncion):
        if(tipoFuncion != "void"):
            dirGlobal = Direccion["global"+tipoFuncion].getDir()
            globalVars.agregarVariable(nombreFuncion, tipoFuncion, dirGlobal, False, 0,0)
        resultado = dictFunciones.agregarFuncion(nombreFuncion, tipoFuncion, cuadruplos.getCount(), dirGlobal)
        if resultado != "OK":
            print("Ya existe una funcion con el nombre ", resultado)
            sys.exit()
    else:
        print("Ya existe una variable global con el nombre ", nombreFuncion)
        sys.exit()

# Agrega los parámetros guardados en la lista "listaVariables" al
# diccionario de parámetros dentro del diccionario de la función.
def p_addParamsFunc(p):
    '''addParamsFunc : '''
    global dictFunciones
    global nombreFuncion
    global listaVariables
    for variables in listaVariables:
        if variables[2]:
            print("Syntax Error: Un arreglo no puede ser un parametro", p.lineno(0))
            sys.exit()
        variables.append(Direccion["local"+variables[1]].getDir())
        if dictFunciones.funcionExiste(variables[0]):
            print("Ya existe una funcion con el nombre", variables[0])
            sys.exit()
    resultado = dictFunciones.agregarParamTable(nombreFuncion, listaVariables)
    if resultado != "OK":
        print("Ya existe un parametro en la funcion", nombreFuncion,"con el nombre", resultado)
        sys.exit()
    listaVariables = []

# Agrega las variables guardadas en la lista "listaVariables" al
# diccionario de variables locales dentro del diccionario de la función.
def p_addVarsFunc(p):
    '''addVarsFunc : '''
    global dictFunciones
    global listaVariables
    global nombreFuncion
    global Direccion
    #print(listaVariables)
    for variables in listaVariables:
        variables.append(Direccion["local"+variables[1]].getDir())
        if variables[2]:
            Direccion["local"+variables[1]].increaseDir(variables[3] * (variables[4] if variables[4] else 1))
        if dictFunciones.funcionExiste(variables[0]):
            print("Ya existe una funcion con el nombre", variables[0])
            sys.exit()
    resultado = dictFunciones.agregarVariables(nombreFuncion, listaVariables)
    if resultado != "OK":
        print("Ya existe una variable con el nombre", resultado)
        sys.exit()
# Verifica return y agrega el cuádruplo Endfunc y resetea las direcciones locales y temporales
def p_endFunc(p):
    '''endFunc : '''
    global tipoFuncion
    global hasReturn
    global cuadruplos
    global dictFunciones
    global nombreFuncion
    global Direccion
    global pilaReturn
    if tipoFuncion != "void" and hasReturn == False:
        print("Syntax error: La funcion", nombreFuncion, "ocupa return", p.lineno(0))
        sys.exit()
    elif tipoFuncion != "void" and hasReturn:
        while len(pilaReturn):
            fill = pilaReturn.pop()
            cuadruplos.addTo(fill,cuadruplos.getCount())

    if nombreFuncion != "main":
        cuadruplos.addCuadruplo("Endfunc", -1, -1, -1)
    
    Direccion["tempint"].resetActual()
    Direccion["tempfloat"].resetActual()
    Direccion["tempchar"].resetActual()
    Direccion["localint"].resetActual()
    Direccion["localfloat"].resetActual()
    Direccion["localchar"].resetActual()
    hasReturn = False

# Asigna direcciones a todas las variables en "listaVariables" y las
# agrega al diccionario de variables globales.
def p_addGlobalVars(p):
    '''addGlobalVars : '''
    global dictFunciones
    global listaVariables
    global nombreFuncion
    #print(listaVariables)
    for variable in listaVariables:
        if not globalVars.varExiste(variable[0]):
            globalVars.agregarVariable(variable[0], variable[1], 
                                        Direccion["global"+variable[1]].getDir(), 
                                        variable[2], variable[3], variable[4])
            if variable[2]:
                Direccion["global"+variable[1]].increaseDir(variable[3] * (variable[4] if variable[4] else 1))
        else:
            print("Ya existe una variable con el nombre", variable[0])
            sys.exit()
    listaVariables = []

# Si el tope de pilaPoper es una condición  y los tipos son compatibles
# para los dos siguientes valores de pilaOp se crea el cuádruplo.
def p_popCondition(p):
    '''popCondition : '''
    global pilaPoper
    global pilaOp
    global pilaTipo
    global cuadruplos
    global cuboSem
    global Direccion
    if len(pilaPoper) > 0:
        topPoper = pilaPoper[-1]
    else: topPoper = "None"
    if topPoper != '(':
        if  topPoper == '<'  or topPoper == '>' or topPoper == '==' or topPoper == '!=' or topPoper == '|' or topPoper == '&':
            op = pilaPoper.pop()
            opDerecho = pilaOp.pop()
            opIzquierdo = pilaOp.pop()
            tipoDerecho = pilaTipo.pop()
            tipoIzquierdo = pilaTipo.pop()
            tipoRes = cuboSem.semantica(tipoIzquierdo, tipoDerecho, op)
            if  tipoRes == "error":
                print("Type mismatch error: Los tipos de los operandos no son compatibles")
                sys.exit()
            nuevaDir = Direccion["temp"+tipoRes].getDir()
            if nuevaDir == -1:
                print("Stack overflow: se acabo la memoria")
                sys.exit()
            cuadruplos.addCuadruplo(op, opIzquierdo, opDerecho, nuevaDir)
            pilaOp.append(nuevaDir)
            pilaTipo.append(tipoRes)

# Si el tope de pilaPoper es '=' y los tipos son compatibles para los dos
# siguientes valores de pilaOp se crea el cuadruplo "=".
def p_popEqual(p):
    '''popEqual : '''
    global pilaPoper
    global pilaOp
    global pilaTipo
    global cuadruplos
    global cuboSem
    if len(pilaPoper) > 0:
        topPoper = pilaPoper[-1]
    else: topPoper = "None"
    if topPoper != '(':
        if  topPoper == '=':
            op = pilaPoper.pop()
            opDerecho = pilaOp.pop()
            opIzquierdo = pilaOp.pop()
            tipoDerecho = pilaTipo.pop()
            tipoIzquierdo = pilaTipo.pop()
            tipoRes = cuboSem.semantica(tipoIzquierdo, tipoDerecho, op)
            if  tipoRes == "error":
                
                print(op, opIzquierdo, opDerecho, tipoIzquierdo, tipoDerecho, tipoRes)
                print("Type mismatch error: Se esta asignando un tipo de variable diferente a la declarada")
                sys.exit()
            nuevaDir = Direccion["temp"+tipoRes].getDir()
            if nuevaDir == -1:
                print("Stack overflow: Sobrepasaste el espacio de memoria para las variables")
                sys.exit()
            cuadruplos.addCuadruplo(op, opDerecho, -1, opIzquierdo)

# Si el tope de pilaPoper es '*' o '/'  y los tipos son compatibles
# para los dos siguientes valores de pilaOp se crea el cuádruplo.
def p_popMultDiv(p):
    '''popMultDiv : '''
    global pilaPoper
    global pilaOp
    global pilaTipo
    global cuadruplos
    global cuboSem

    if len(pilaPoper) > 0:
        topPoper = pilaPoper[-1]
    else: topPoper = "None"
    if topPoper != '(':
        if  topPoper == '*' or topPoper == '/':
            op = pilaPoper.pop()
            opDerecho = pilaOp.pop()
            opIzquierdo = pilaOp.pop()
            tipoDerecho = pilaTipo.pop()
            tipoIzquierdo = pilaTipo.pop()
            tipoRes = cuboSem.semantica(tipoIzquierdo, tipoDerecho, op)
            if  tipoRes == "error":
                print("Type mismatch")
                sys.exit()
            nuevaDir = Direccion["temp"+tipoRes].getDir()
            if nuevaDir == -1:
                print("Stack overflow: Sobrepasaste el espacio de memoria para las variables")
                sys.exit()
            cuadruplos.addCuadruplo(op, opIzquierdo, opDerecho, nuevaDir)
            pilaOp.append(nuevaDir)
            pilaTipo.append(tipoRes)

# Si el tope de pilaPoper es '+' o '-' y los tipos son compatibles
# para los dos siguientes valores de pilaOp se crea el cuádruplo.
def p_popPlusMinus(p):
    '''popPlusMinus : '''
    global pilaPoper
    global pilaOp
    global pilaTipo
    global cuadruplos
    global cuboSem

    if len(pilaPoper) > 0:
        topOper = pilaPoper[-1]
    else: topOper = "None"
    if topOper != '(':
        if  topOper == '+' or topOper == '-':
            op = pilaPoper.pop()
            opDerecho = pilaOp.pop()
            opIzquierdo = pilaOp.pop()
            tipoDerecho = pilaTipo.pop()
            tipoIzquierdo = pilaTipo.pop()
            tipoRes = cuboSem.semantica(tipoIzquierdo, tipoDerecho, op)
            if  tipoRes == "error":
                print("Type mismatch")
                sys.exit()
            nuevaDir = Direccion["temp"+tipoRes].getDir()
            if nuevaDir == -1:
                print("Stack overflow: Sobrepasaste el espacio de memoria para las variables")
                sys.exit()
            cuadruplos.addCuadruplo(op, opIzquierdo, opDerecho, nuevaDir)
            pilaOp.append(nuevaDir)
            pilaTipo.append(tipoRes)

#Agrega '=' a pilaPoper
def p_pushEqual(p):
    ''' pushEqual : '''
    global pilaPoper
    pilaPoper.append(p[-1])

# Agrega '*' o '/' a pilaPoper
def p_pushMultDiv(p):
    ''' pushMultDiv : '''
    global pilaPoper
    pilaPoper.append(p[-1])

# Agrega '+' o '-' a pilaPoper
def p_pushPlusMinus(p):
    ''' pushPlusMinus : '''
    global pilaPoper
    pilaPoper.append(p[-1])

# Agrega una condicion a pilaPoper
def p_pushCondition(p):
    ''' pushCondition : '''
    global pilaPoper
    pilaPoper.append(p[-1])

# Se agrega la constante a la tabla de constantes si es que no existe,
# luego se guarda el valor y el tipo en pilaOp y pilaTipo.
def p_pushConstInt(p):
    '''pushConstInt : '''
    global pilaOp
    global pilaTipo
    global constantes
    const = p[-1]
    constante = constantes.buscarVariable(const)
    if constante == "ERROR":
        dirConstant = Direccion["constint"].getDir()
        constantes.agregarVariable(const, "int", dirConstant, False, 0, 0)
        pilaOp.append(dirConstant)
        pilaTipo.append("int")
    else:
        pilaOp.append(constante["dir"])
        pilaTipo.append("int")

# Se agrega la constante a la tabla de constantes si es que no existe,
# luego se guarda el valor y el tipo en pilaOp y pilaTipo.
def p_pushConstFloat(p):
    '''pushConstFloat : '''
    global pilaOp
    global pilaTipo
    global constantes
    const = p[-1]
    constante = constantes.buscarVariable(const)
    if constante == "ERROR":
        dirConstant = Direccion["constfloat"].getDir()
        constantes.agregarVariable(const, "float", dirConstant, False, 0, 0)
        pilaOp.append(dirConstant)
        pilaTipo.append("float")
    else:
        pilaOp.append(constante["dir"])
        pilaTipo.append("float")

# Se agrega la constante a la tabla de constantes si es que no existe,
# luego se guarda el valor y el tipo en pilaOp y pilaTipo.
def p_pushConstChar(p):
    '''pushConstChar : '''
    global pilaOp
    global pilaTipo
    global constantes
    const = p[-1]
    constante = constantes.buscarVariable(const)
    if constante == "ERROR":
        dirConstant = Direccion["constchar"].getDir()
        constantes.agregarVariable(const, "char", dirConstant, False, 0, 0)
        pilaOp.append(dirConstant)
        pilaTipo.append("char")
    else:
        pilaOp.append(constante["dir"])
        pilaTipo.append("char")

# Se agrega la constante a la tabla de constantes si es que no existe,
# luego se guarda el valor y el tipo en pilaOp y pilaTipo.
def p_pushConstString(p):
    '''pushConstString : '''
    global pilaOp
    global pilaTipo
    global constantes
    const = p[-1]
    constante = constantes.buscarVariable(const)
    if constante == "ERROR":
        dirConstant = Direccion["conststring"].getDir()
        constantes.agregarVariable(const, "string", dirConstant, False, 0, 0)
        pilaOp.append(dirConstant)
        pilaTipo.append("string")
    else:
        pilaOp.append(constante["dir"])
        pilaTipo.append("string")
        
# Agrega la id a pilaOp y el tipo a pilaTipo.
def p_pushPilaOp(p):
    '''  pushPilaOp : '''
    global dictFunciones
    global nombreFuncion
    global pilaOp
    global pilaTipo
    global pilaDim
    varName = p[-1]
    variable = "ERROR"
    if len(nombreFuncion):
            variable = dictFunciones.buscarVariable(varName, nombreFuncion) 
    if variable != "ERROR":
        #print(variable)
        pilaOp.append(variable["dir"])
        pilaTipo.append(variable["type"])
        if variable["isArray"]:
            pilaDim.append(variable["dim1"])
            pilaDim.append(variable["dim2"])
    elif globalVars.buscarVariable(varName) != "ERROR":
        variable = globalVars.buscarVariable(varName)
        if variable["isArray"]:
            pilaDim.append(variable["dim1"])
            pilaDim.append(variable["dim2"])
        #print(variable)
        pilaOp.append(variable["dir"])
        pilaTipo.append(variable["type"])
    else:    
        print("La variable", varName, "no ha sido declarada en linea", p.lineno(0))
        sys.exit()

# Agrega '(' a pilaPoper
def p_pushParen(p):
    '''pushParen : '''
    global pilaPoper
    pilaPoper.append('(')

# Saca '(' de pilaPoper si es el elemento en el tope.
def p_popParen(p):
    '''popParen : '''
    global pilaPoper
    if len(pilaPoper) > 0:
        topPoper = pilaPoper[-1]
    else: topPoper = "None"
    if topPoper == '(':
        pilaPoper.pop()

# Se guarda el parámetro y su tipo en pilaParams
def p_addParam(p):
    ''' addParam : '''
    global pilaParams
    global pilaOp
    global pilaTipo
    param = pilaOp.pop()
    tipoParam = pilaTipo.pop()
    pilaParams.append([param, tipoParam])

# Verifica que los parámetros en pilaParams sean la cantidad y el tipo
# correcto, y luego crea un cuádruplo "parameter" para cada uno.
def p_verifyParams(p):
    ''' verifyParams : '''
    global dictFunciones
    global pilaLlamadas
    global pilaParams
    nombreFuncion = pilaLlamadas[-1]
    funcion = dictFunciones.getFuncion(nombreFuncion)
    if funcion == "ERROR":
        print("ERROR: La funcion",nombreFuncion,"no ha sido declarada en la linea ", p.lineno(0))
        sys.exit()
    paramTypes = funcion["paramTable"].getAllTypes()
    if funcion["paramTable"].lenOfVars() < len(pilaParams) | funcion["paramTable"].lenOfVars() > len(pilaParams):
        print("Syntax error: El numero de parametros en la funcion",nombreFuncion,"es mayor o menor al requerido en linea", p.lineno(0))
        sys.exit()
    i = 1
    for params in pilaParams:
        if paramTypes[i-1] != params[1]:
            print("Type mismatch: El paramentro #", i, "de la funcion", nombreFuncion, "es del tipo incorrecto en linea", p.lineno(0))
            sys.exit()
        else:
            cuadruplos.addCuadruplo("parameter", params[0], -1, "par"+str(i))
        i += 1
    pilaParams = []

# Crea el cuádruplo 'gosub' con el nombre de la función y crea el
# cuádruplo '=' para la variable global de la función.
def p_pushGosub(p):
    '''pushGosub : '''
    global dictFunciones
    global pilaLlamadas
    global pilaParams
    global cuadruplos
    global pilaOp
    global pilaTipo
    nombreFuncion = pilaLlamadas[-1]
    funcion = dictFunciones.getFuncion(nombreFuncion)
    returnType = funcion["returnType"]
    cuadruplos.addCuadruplo("gosub", nombreFuncion, -1, -1)
    variableFuncion  = globalVars.buscarVariable(nombreFuncion)
    if(returnType != "void"):
        nuevaDir = Direccion["temp"+returnType].getDir()
        if nuevaDir == -1:
            print("Stack overflow: Sobrepasaste el espacio de memoria para las variables")
            sys.exit()

        cuadruplos.addCuadruplo("=", variableFuncion["dir"], -1, nuevaDir)
        pilaOp.append(nuevaDir)
        pilaTipo.append(returnType)
    pilaLlamadas.pop()

# Crea el cuádruplo "gosub" con el nombre de la función
def p_pushGosubLlamada(p):
    '''pushGosubLlamada : '''
    global dictFunciones
    global pilaLlamadas
    global pilaParams
    global cuadruplos
    global pilaOp
    global pilaTipo

    nombreFuncion = pilaLlamadas[-1]
    pilaLlamadas.pop()
    cuadruplos.addCuadruplo("gosub", nombreFuncion, -1, -1)

# Agrega el id a pilaLlamadas y crea el cuádruplo, "era" con el nombre de la función.
def p_pushEra(p):
    ''' pushEra : '''
    global cuadruplos
    global pilaLlamadas
    nombreFuncion = p[-1]
    pilaLlamadas.append(nombreFuncion)
    cuadruplos.addCuadruplo("era", nombreFuncion, -1, -1)

# Se saca la id y el tipo de pilaOp y pilaTipo y se crea el cuadruplo "write"
def p_popWrite(p):
    '''popWrite : '''
    global cuadruplos
    global pilaOp
    op = pilaOp.pop()
    pilaTipo.pop()
    cuadruplos.addCuadruplo("write", -1, -1, op)

# Se crea el cuadruplo "writeEnd"
def p_addWriteEnd(p):
    '''addWriteEnd : '''
    global cuadruplos
    cuadruplos.addCuadruplo("writeEnd", -1, -1, -1)

# Se saca la id y el tipo de pilaOp y pilaTipo y se crea el cuadruplo "read".
def p_popRead(p):
    '''popRead : '''
    global cuadruplos
    global pilaOp
    op = pilaOp.pop()
    pilaTipo.pop()
    cuadruplos.addCuadruplo("read", -1, -1, op)

# La variable hasColor = true
def p_hasColor(p):
    '''hasColor :'''
    global hasFillColor
    hasFillColor = True

# Se saca las id y los tipos de pilaOp y pilaTipo, se crea el cuadruplo "line".
def p_popLine(p):
    '''popLine : '''
    global cuadruplos
    global pilaOp
    op1 = pilaOp.pop()
    op2 = pilaOp.pop()
    tipo1 = pilaTipo.pop()
    tipo2 = pilaTipo.pop()
    if tipo1 !=  "int" and tipo1 != "float" or (tipo2 !=  "int" and tipo2 != "float"):
        print("Type error: Solo int o float para la funcion line")
        sys.exit()
    cuadruplos.addCuadruplo("line", op2, op1, -1)

# Se saca las id y los tipos de pilaOp y pilaTipo, el color y se crea el cuadruplo "point".
def p_popPoint(p):
    '''popPoint : '''
    global cuadruplos
    global pilaOp
    global hasFillColor
    color = -1
    if hasFillColor:
        color = pilaOp.pop()
        pilaTipo.pop()
        hasFillColor = True
    op = pilaOp.pop()
    tipo = pilaTipo.pop()
    if tipo !=  "int" and tipo != "float":
        print("Type error: Solo int o float para la funcion point")
        sys.exit()
    cuadruplos.addCuadruplo("point", op, color, -1)

# Se saca las id y los tipos de pilaOp y pilaTipo, el color y se crea el cuadruplo "circle".
def p_popCircle(p):
    '''popCircle : '''
    global cuadruplos
    global pilaOp
    global hasFillColor
    color = -1
    if hasFillColor:
        color = pilaOp.pop()
        pilaTipo.pop()
        hasFillColor = True
    op = pilaOp.pop()
    tipo = pilaTipo.pop()
    if tipo !=  "int" and tipo != "float":
        print("Type error: Solo int o float para la funcion circle")
        sys.exit()
    cuadruplos.addCuadruplo("circle", op, color, -1)

# Se saca las id y los tipos de pilaOp y pilaTipo, el color y se crea el cuadruplo "arc".
def p_popArc(p):
    '''popArc : '''
    global cuadruplos
    global pilaOp
    global hasFillColor
    color = -1
    if hasFillColor:
        color = pilaOp.pop()
        pilaTipo.pop()
        hasFillColor = True
    op1 = pilaOp.pop()
    op2 = pilaOp.pop()
    tipo1 = pilaTipo.pop()
    tipo2 = pilaTipo.pop()
    if tipo1 !=  "int" and tipo1 != "float" or (tipo2 !=  "int" and tipo2 != "float"):
        print("Type error: Solo int o float para la funcion arc")
        sys.exit()
    cuadruplos.addCuadruplo("arc", op2, op1, color)

# Se crea el cuadruplo "penup".
def p_popPenup(p):
    '''popPenup : '''
    global cuadruplos
    cuadruplos.addCuadruplo("penup", -1, -1, -1)

# Se saca las id y los tipos de pilaOp y pilaTipo y se crea el cuadruplo "arc".
def p_popPendown(p):
    '''popPendown : '''
    global cuadruplos
    global pilaOp
    op1 = pilaOp.pop()
    op2 = pilaOp.pop()
    tipo1 = pilaTipo.pop()
    tipo2 = pilaTipo.pop()
    if tipo1 !=  "int" and tipo1 != "float" or (tipo2 !=  "int" and tipo2 != "float"):
        print("Type error: Solo int o float para la funcion pendown")
        sys.exit()
    cuadruplos.addCuadruplo("pendown", op2, op1, -1)

# Se saca la id y el tipo de pilaOp y pilaTipo y se crea el cuadruplo "color".
def p_popColor(p):
    '''popColor : '''
    global cuadruplos
    global pilaOp
    op = pilaOp.pop()
    pilaTipo.pop()
    cuadruplos.addCuadruplo("color", -1, -1, op)

# Se saca las id y los tipos de pilaOp y pilaTipo y se crea el cuadruplo "size".
def p_popSize(p):
    '''popSize : '''
    global cuadruplos
    global pilaOp
    op1 = pilaOp.pop()
    op2 = pilaOp.pop()
    tipo1 = pilaTipo.pop()
    tipo2 = pilaTipo.pop()
    if tipo1 !=  "int"  or tipo2 !=  "int" :
        print("Type error: Solo int para la funcion size")
        sys.exit()
    cuadruplos.addCuadruplo("size", op2, op1, -1)

# Se crea el cuadruplo "clear".
def p_popClear(p):
    '''popClear : '''
    global cuadruplos
    cuadruplos.addCuadruplo("clear", -1, -1, -1)

# Verifica el tipo de retorno de la funcion, crea el cuadruplo "return",
# crea el cuadruplo "goto" y agrega el numero  de cuadruplo a la pilaReturn
def p_popReturn(p):
    '''popReturn : '''
    global pilaOp
    global cuadruplos
    global hasReturn
    global pilaTipo
    global tipoFuncion
    global dictFunciones
    global nombreFuncion
    global pilaReturn
    elem = pilaOp.pop()
    elemTipo = pilaTipo.pop()
    hasReturn = True
    if tipoFuncion != elemTipo:
        print("Type mismatch: El elemento que se regresa es diferente al tipo de funcion declarada", p.lineno(0))
        sys.exit()
    cuadruplos.addCuadruplo("return", -1, -1, elem)
    cuadruplos.addCuadruplo("goto", -1, -1, -2)
    pilaReturn.append(cuadruplos.getCount()-1)

# Verifica que el tipo del tope sea bool, crea el cuádruplo "gotof" y agrega
# el número del cuádruplo a pilaSaltos.
def p_pushGotoF(p):
    '''pushGotoF :'''
    global pilaSaltos
    global pilaOp
    global pilaTipo
    global cuadruplos
    tipoTop = pilaTipo.pop() 
    if(tipoTop == "bool"):
        op = pilaOp.pop()
        cuadruplos.addCuadruplo("gotof", op, -1, -2)
        pilaSaltos.append(cuadruplos.getCount()-1)
    else:
        print("Type mismatch: Se espera un bool como condicion", p.lineno(0))
        sys.exit()

# Crea el cuádruplo "goto", saca el elemento de la pilaSaltos y rellena
# el cuadruplo "gotof" que apunta con el siguiente número del
# cuádruplo, por último agrega el número de cuádruplo actual a la
# pilaSaltos.
def p_rellenarFalso(p):
    '''rellenarFalso :'''
    global pilaSaltos
    global cuadruplos
    
    cuadruplos.addCuadruplo("goto", -1, -1, -2)
    falso = pilaSaltos.pop()
    pilaSaltos.append(cuadruplos.getCount()-1)
    cuadruplos.addTo(falso, cuadruplos.getCount())

# Saca el elemento de la pilaSaltos y rellena el cuádruplo "goto" que
# apunta con el siguiente número del cuádruplo. 
def p_rellenaSalida(p):
    '''rellenarSalida :'''
    global pilaSaltos
    global cuadruplos

    salida = pilaSaltos.pop()
    cuadruplos.addTo(salida, cuadruplos.getCount())

# Agrega el número de cuadruplo actual a pilaSaltos
def p_pushSalto(p):
    '''pushSalto :'''
    global pilaSaltos
    global cuadruplos

    pilaSaltos.append(cuadruplos.getCount())

# Crea el cuádruplo "goto" con el número agregado en pushSalto  y
# rellena el "gotof" de pushGoToF
def p_rellenarWhile(p):
    '''rellenarWhile :'''
    global pilaSaltos
    global cuadruplos
    
    falso = pilaSaltos.pop()
    start = pilaSaltos.pop()
    cuadruplos.addCuadruplo("goto", -1, -1, start)
    cuadruplos.addTo(falso, cuadruplos.getCount())

# Verifica la variable y agrega la id a pilaOp y el tipo a pilaTipo.
def p_pushFromId(p):
    '''pushFromId :'''
    global dictFunciones
    global nombreFuncion
    global pilaOp
    global pilaTipo
    varName = p[-1]
    variable = "ERROR"
    if len(nombreFuncion):
        variable = dictFunciones.buscarVariable(varName, nombreFuncion) 
    if variable != "ERROR":
        #print(variable)
        if variable["type"] != "int":
            print("La variable", varName, "ocupa ser int para funcionar en el from", p.lineno(0))
            sys.exit()
        pilaOp.append(variable["dir"])
        pilaTipo.append(variable["type"])
    elif globalVars.buscarVariable(varName) != "ERROR":
        variable = globalVars.buscarVariable(varName)
        #print(variable)
        if variable["type"] != "int":
            print("La variable", varName, "ocupa ser int para funcionar en el from", p.lineno(0))
            sys.exit()
        pilaOp.append(variable["dir"])
        pilaTipo.append(variable["type"])

    else:    
        print("La variable", varName, "no ha sido declarada en linea", p.lineno(0))
        sys.exit()

# Verifica el tipo de la constante con la variable y agrega un cuádruplo "=".
def p_pushVC(p):
    '''pushVC :'''
    global pilaSaltos
    global pilaOp
    global pilaTipo
    global cuadruplos
    global cuboSem
    global versionControl   

    expType = pilaTipo.pop()  
    exp = pilaOp.pop()
    vcontrol = pilaOp.pop()
    controlType = pilaTipo.pop()
    tipoRes = cuboSem.semantica(expType, controlType, "=")
    if tipoRes == "error":
        print("Type mismatch en la declaracion del from", p.lineno(0))
        sys.exit()
    versionControl.append(vcontrol)
    cuadruplos.addCuadruplo("=", exp, -1, vcontrol)
    cuadruplos.addCuadruplo("=", vcontrol, -1, "VC")

# Agrega el cuádruplo "<" para comparar  VC con VF y agrega el número del
# cuádruplo a pilaSaltos, luego agrega el cuádruplo "gotof"  y agrega el
# número del cuádruplo a pilaSaltos.
def p_pushVF(p):
    '''pushVF :'''
    global pilaSaltos
    global pilaOp
    global pilaTipo
    global cuadruplos
    global cuboSem
    global versionControl
    global versionFinal
    expType = pilaTipo.pop()  
    exp = pilaOp.pop()
    if expType != "int":
        print("Type mismatch en la declaracion del from to", p.lineno(0))
        sys.exit()
    versionFinal = exp
    cuadruplos.addCuadruplo("=", exp, -1, "VF")
    nuevaDir = Direccion["tempbool"].getDir()
    if nuevaDir == -1:
        print("Stack overflow: Sobrepasaste el espacio de memoria para las variables")
        sys.exit()
    cuadruplos.addCuadruplo("<", versionControl[-1], versionFinal, nuevaDir)
    pilaSaltos.append(cuadruplos.getCount()-1)
    cuadruplos.addCuadruplo("gotof", nuevaDir, -1, -2)
    pilaSaltos.append(cuadruplos.getCount()-1)

# Agrega el cuádruplo "+" para sumar VC más 1, rellena el "gotof" de
# pushVF y crea el cuádruplo "goto" con el número agregado en pushVF.
def p_rellenaFrom(p):
    '''rellenaFrom :'''
    global pilaSaltos
    global cuadruplos
    global versionControl
    global constantes

    constante = constantes.buscarVariable(1)
    if constante == "ERROR":
        dirConstant = Direccion["constint"].getDir()
        constantes.agregarVariable(1, "int", dirConstant, False, 0, 0)
    else:
        dirConstant = constante["dir"]

    nuevaDir = Direccion["tempint"].getDir()
    if nuevaDir == -1:
        print("Stack overflow: Sobrepasaste el espacio de memoria para las variables")
        sys.exit()
    cuadruplos.addCuadruplo("+", versionControl[-1], dirConstant , nuevaDir)
    cuadruplos.addCuadruplo("=", nuevaDir, -1 , versionControl[-1])
    versionControl.pop()
    fin = pilaSaltos.pop()
    start = pilaSaltos.pop()
    cuadruplos.addCuadruplo("goto", -1, -1, start)
    cuadruplos.addTo(fin, cuadruplos.getCount())

# Agrega el número de cuádruplo al "goto" que se agregó en addProgram.
def p_rellenaMain(p):
    '''rellenaMain : '''
    global cuadruplos
    cuadruplos.addTo(0, cuadruplos.getCount())

# Saca el valor de la dimension de pilaOp y lo agrega a pilaDim
def p_pushDim(p):
    '''pushDim :'''
    global pilaDim
    global pilaOp
    global constantes
    dim = pilaOp.pop()
    dimension = constantes.buscarVariableDirName(dim)
    pilaDim.append(dimension)

# Declara la variable como arreglo en el diccionario de variables y agrega las dimensiones de pilaDim
def p_addArreglo(p):
    '''addArreglo :'''
    global pilaDim
    global pilaOp
    global listaVariables
    listaVariables[-1][2] = True
    i=1
    for dim in pilaDim:
        listaVariables[-1][2+i] = dim
        i+=1
    pilaDim = []

# Agrega el cuadruplo "ver" que verifica que el índice deseado este entre las
# dimensiones del arreglo.
def p_verifyDim(p):
    '''verifyDim :'''
    global pilaDim
    global pilaOp
    global cuadruplos
    global dimCounter
    global pilaTipo
    global constantes

    op = pilaOp[-1]
    dim = pilaDim[dimCounter]
    constante = constantes.buscarVariable(0)
    if constante == "ERROR":
        dirConstant = Direccion["constint"].getDir()
        constantes.agregarVariable(0, "int", dirConstant, False, 0, 0)
    else:
        dirConstant = constante["dir"]

    constante2 = constantes.buscarVariable(dim)
    if constante2 == "ERROR":
        dirConstant2 = Direccion["constint"].getDir()
        constantes.agregarVariable(dim, "int", dirConstant2,False, 0, 0)
    else:
        dirConstant2 = constante2["dir"]

    cuadruplos.addCuadruplo("ver", op, dirConstant, dirConstant2)

# Agrega los cuádruplos necesarios para calcular la dirección del índice que se pide.
def p_calculateDir(p):
    '''calculateDir :'''
    global pilaOp
    global cuadruplos
    global constantes
    global dimCounter
    global pilaTipo
    global pilaDim

    op = pilaOp.pop()
    pilaTipo.pop()

    nuevaDir = Direccion["tempint"].getDir()
    if (pilaDim[1] != 0) and (dimCounter == 0):
        constante = constantes.buscarVariable(pilaDim[1])
        if constante == "ERROR":
            dirConstant = Direccion["constint"].getDir()
            constantes.agregarVariable(pilaDim[1], "int", dirConstant,False, 0, 0)
        else:
            dirConstant = constante["dir"]
        cuadruplos.addCuadruplo("*", op, dirConstant, nuevaDir)
        pilaOp.append(nuevaDir)
        pilaTipo.append("int")
        dimCounter += 1

    elif (pilaDim[1] != 0) and (dimCounter == 1):
        opDerecho = pilaOp.pop()
        dirBase = pilaOp.pop()
        pilaTipo.pop()
        tipoDirBase = pilaTipo.pop()
        cuadruplos.addCuadruplo("+", op, opDerecho, nuevaDir)
        
        nuevaDir2 = Direccion["tempint"].getDir()

        constante = constantes.buscarVariable(dirBase)
        if constante == "ERROR":
            dirConstant = Direccion["constint"].getDir()
            constantes.agregarVariable(dirBase, "int", dirConstant,False, 0, 0)
        else:
            dirConstant = constante["dir"]
        
        cuadruplos.addCuadruplo("+", nuevaDir, dirConstant, nuevaDir2)
        pilaOp.append("*"+str(nuevaDir2))
        pilaTipo.append(tipoDirBase)
        dimCounter = 0
        pilaDim = []
    else:
        dirBase = pilaOp.pop() 
        tipoDirBase = pilaTipo.pop()

        nuevaDir = Direccion["tempint"].getDir()
        constante = constantes.buscarVariable(dirBase)
        if constante == "ERROR":
            dirConstant = Direccion["constint"].getDir()
            constantes.agregarVariable(dirBase, "int", dirConstant,False, 0, 0)
        else:
            dirConstant = constante["dir"]
        
        cuadruplos.addCuadruplo("+", op, dirConstant, nuevaDir)
        pilaOp.append("*"+str(nuevaDir))
        pilaTipo.append(tipoDirBase)
        dimCounter = 0
        pilaDim = []

# Exporta las funciones, constantes y cuadruplos
def p_printTables(p):
    '''printTables : '''
    #constantes.printVars()
    #cuadruplos.printCuadruplos()
    dictFunciones.exportFunciones("exec.hl")
    constantes.exportConstantes("exec.hl")
    cuadruplos.exportCuadruplos("exec.hl")



def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")
    sys.exit()

parser = yacc.yacc()

""" with open('prueba.txt', 'r') as file:
    data = file.read().replace('\n', '') """



filename = sys.argv[1]

f = open(filename,'r')
data = f.read()
f.close()

parser.parse(data)

""" while True:
    try:
        s = input('')
    except EOFError:
        break """