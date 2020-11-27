# Hector Noel Leon Quiroz A01251806
# Maquina Virtual MeMyself

from Memoria import Memoria
import sys
import tkinter

memoriaGlobal = Memoria()
memoriaConstante = Memoria()

funciones = {}
cuadruplos = []

pilaMemoriaLocal = []
pilaMemoriaTemp = []
x0 = 0
y0 = 0
actualHeight = 600
actualWidth = 800

# Lee las funciones, cuadruplos y constantes
def readFile(data):
    read = ""
    for i in data:
        if i == "TablaFunciones:":
            read = "TablaFunciones"
        elif i == "TablaConstantes:":
            read = "TablaConstantes"
        elif i == "Cuadruplos:":
            read = "Cuadruplos"
        elif read == "TablaFunciones":
            funcion = i.split(";")
            readFunc(funcion)
        elif read == "TablaConstantes":
            if "\"" in i:
                constante = i.split("\"")
                constante.pop(0)
                constante[1] = constante[1][1:]
            else:
                constante = i.split()
            readConstantes(constante)
        elif read == "Cuadruplos":
            cuadruplo = i.split(";")
            readCuad(cuadruplo)

# Parsea las funcniones
def readFunc(funcion):
    global funciones
    nombre = funcion[0]
    dirGlobal = int(funcion[1])
    resto = funcion[2]
    cuadruplo = 0
    paramStart = 0
    params = []
    for c in range (0, len(resto)):
        if resto[c] == '[':
            if c == 1:
                cuadruplo = int(resto[0])
            else:
                cuadruplo = int(resto[0:c])
            paramStart = c+1
        elif resto[c] == ',':
            params.append(int(resto[paramStart: c]))
            paramStart = c+1
        elif resto[c] == ']':
            if paramStart != 0 and paramStart != c:
                params.append(int(resto[paramStart: c]))
    funciones[nombre] = {"cuad" : cuadruplo, "params": params, "dir": dirGlobal}

# Parsea las constanes
def readConstantes(constante):
    global memoriaConstante
    address = int(constante[1])
    if address > 31999 and address < 35000:
        memoriaConstante.assign(address, int(constante[0]))
    elif address > 34999 and address < 38000:
        memoriaConstante.assign(address, float(constante[0]))
    elif address > 37999 and address < 41000:
        char = constante[0].split("'")
        memoriaConstante.assign(address, char[1])
    else:
        memoriaConstante.assign(address, constante[0])

# Parsea las cuadruplos
def readCuad(cuadruplo):
    global cuadruplos
    for i in range (0, len(cuadruplo)):
        if cuadruplo[i].isdigit():
            cuadruplo[i] = int(cuadruplo[i])
    cuadruplos.append(cuadruplo)

# Corre los cuadruplos
def runContext():
    global pilaMemoriaLocal
    global pilaMemoriaTemp
    global memoriaGlobal
    global x0
    global y0
    global actualHeight
    global actualWidth
    top = None
    C = None

    pilaMemoriaLocal.append(Memoria())
    pilaMemoriaTemp.append(Memoria())
    llamadaFuncion = []
    ip = 0
    dirGlobal = 0
    lastIp = []
    while ip < len(cuadruplos):
        cuadruplo = cuadruplos[ip]
        ip += 1
        if cuadruplo[0] == "goto":
            ip = cuadruplo[3]
        elif cuadruplo[0] == "gotof":
            if not getValor(cuadruplo[1]):
                ip = cuadruplo[3]
        elif cuadruplo[0] == "read":
            resultado = readValor(cuadruplo[3])
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "write":
            resultado = getValor(cuadruplo[3])
            print(resultado, end="")
        elif cuadruplo[0] == "writeEnd":
            print("")
        elif cuadruplo[0] == "ver":
            indice = getValor(cuadruplo[1])
            if (indice < getValor(cuadruplo[2])) or (indice >= getValor(cuadruplo[3])):
                print("ERROR: El indice en el arreglo esta fuera de las dimensiones declaradas")
                sys.exit()
        elif cuadruplo[0] == "era":
            llamadaFuncion.append([cuadruplo[1]])
        elif cuadruplo[0] == "parameter":
            llamadaFuncion[-1].append(getValor(cuadruplo[1]))
        elif cuadruplo[0] == "gosub":
            nombre = llamadaFuncion[-1][0]
            lastIp.append(ip)
            ip = funciones[nombre]["cuad"]
            dirGlobal = funciones[nombre]["dir"]
            pilaMemoriaLocal.append(Memoria())
            pilaMemoriaTemp.append(Memoria())
            index = 1
            for param in funciones[nombre]["params"]:
                assignValor(llamadaFuncion[-1][index], param)
                index += 1
            llamadaFuncion.pop()
        elif cuadruplo[0] == "return":
            returnVal = getValor(cuadruplo[3])
            assignValor(returnVal, dirGlobal)
        elif cuadruplo[0] == "Endfunc":
            pilaMemoriaLocal.pop()
            pilaMemoriaTemp.pop()
            ip = lastIp.pop()
        elif cuadruplo[0] == "line":
            if C == None:
                print("ERROR: Inicializa primero el canvas con la funcion size")
                sys.exit()
            line = C.create_line(x0, y0,getValor(cuadruplo[1]), getValor(cuadruplo[2]))
        elif cuadruplo[0] == "point":
            if C == None:
                print("ERROR: Inicializa primero el canvas con la funcion size")
                sys.exit()
            size = getValor(cuadruplo[1])
            fillColor = "black"
            if cuadruplo[2] != "-1":
                fillColor = getValor(cuadruplo[2])
            diametro = (actualHeight/100)*size
            if x0-(diametro/2) > 0 and y0-(diametro/2) > 0:
                point = C.create_oval(x0-(diametro/2),  y0-(diametro/2), x0+(diametro/2), y0+(diametro/2), fill=fillColor)
            elif x0-(diametro/2) > 0:
                point =C.create_oval(x0-(diametro/2),  0, x0+(diametro/2), diametro,fill=fillColor)
            elif y0-(diametro/2) > 0:
                point =C.create_oval(0,  y0-(diametro/2), diametro, y0+(diametro/2),fill=fillColor)
            else:
                point =C.create_oval(0,  0, diametro, diametro,fill=fillColor)
        elif cuadruplo[0] == "circle":
            if C == None:
                print("ERROR: Inicializa primero el canvas con la funcion size")
                sys.exit()
            size = getValor(cuadruplo[1])
            fillColor = None
            if cuadruplo[2] != "-1":
                fillColor = getValor(cuadruplo[2])
            diametro = (actualHeight/10)*size
            if x0-(diametro/2) > 0 and y0-(diametro/2) > 0:
                oval = C.create_oval(x0-(diametro/2),  y0-(diametro/2) , x0+(diametro/2), y0+(diametro/2), fill=fillColor)
            elif x0-(diametro/2) > 0:
                oval = C.create_oval(x0-(diametro/2),  1, x0+(diametro/2), diametro, fill=fillColor)
            elif y0-(diametro/2) > 0:
                oval= C.create_oval(1,  y0-(diametro/2), diametro, y0+(diametro/2), fill=fillColor)
            else:
                oval= C.create_oval(1,  1, diametro, diametro, fill=fillColor)
        elif cuadruplo[0] == "arc":
            if C == None:
                print("ERROR: Inicializa primero el canvas con la funcion size")
                sys.exit()
            fillColor = None
            if cuadruplo[3] != "-1":
                fillColor = getValor(cuadruplo[3])
            size = getValor(cuadruplo[1])
            ext = getValor(cuadruplo[2])
            xStart = (actualWidth/10)*size
            yStart = (actualHeight/10)*size
            if x0-(xStart/2) > 0 and y0-(yStart/2) > 0:
                arc = C.create_arc(x0-(xStart/2),  y0-(yStart/2), x0+(xStart/2), y0+(yStart/2), start=0, extent=ext, fill=fillColor)
            elif x0-(xStart/2) > 0:
                arc = C.create_arc(x0-(xStart/2),  0, x0+(xStart/2), yStart, start=0, extent=ext, fill=fillColor)
            elif y0-(yStart/2) > 0:
                arc = C.create_arc(0,  y0-(yStart/2), xStart, y0+(yStart/2), start=0, extent=ext, fill=fillColor)
            else:
                arc = C.create_arc(0,  0, xStart, yStart, start=0, extent=ext, fill=fillColor)
        elif cuadruplo[0] == "penup":
            if C == None:
                print("ERROR: Inicializa primero el canvas con la funcion size")
                sys.exit()
            C.pack()
            top.mainloop()
        elif cuadruplo[0] == "pendown":
            if C == None:
                print("ERROR: Inicializa primero el canvas con la funcion size")
                sys.exit()
            x0=getValor(cuadruplo[1])
            y0=getValor(cuadruplo[2])
        elif cuadruplo[0] == "color":
            if C == None:
                print("ERROR: Inicializa primero el canvas con la funcion size")
                sys.exit()
            C.config(bg=getValor(cuadruplo[3]))
        elif cuadruplo[0] == "size":
            actualHeight = getValor(cuadruplo[2])
            actualWidth = getValor(cuadruplo[1])
            top = tkinter.Tk()
            C = tkinter.Canvas(top, bg="white", height=actualHeight, width=actualWidth)
        elif cuadruplo[0] == "clear":
            if C == None:
                print("ERROR: Inicializa primero el canvas con la funcion size")
                sys.exit()
            C.delete("all")
        elif cuadruplo[0] == "+":
            resultado = getValor(cuadruplo[1]) + getValor(cuadruplo[2])
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "-":
            resultado = getValor(cuadruplo[1]) - getValor(cuadruplo[2])
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "*":
            #print(getValor(cuadruplo[1]), "*", getValor(cuadruplo[2]))
            resultado = getValor(cuadruplo[1]) * getValor(cuadruplo[2])
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "/":
            resultado = getValor(cuadruplo[1]) / getValor(cuadruplo[2])
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "<":
            resultado = (getValor(cuadruplo[1]) < getValor(cuadruplo[2]))
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == ">":
            resultado = (getValor(cuadruplo[1]) > getValor(cuadruplo[2]))
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "!=":
            resultado = (getValor(cuadruplo[1]) != getValor(cuadruplo[2]))
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "&":
            resultado = (getValor(cuadruplo[1]) and getValor(cuadruplo[2]))
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "|":
            resultado = (getValor(cuadruplo[1]) or getValor(cuadruplo[2]))
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "==":
            resultado = (getValor(cuadruplo[1]) is getValor(cuadruplo[2]))
            assignValor(resultado, cuadruplo[3])
        elif cuadruplo[0] == "=":
            if (cuadruplo[3] != "VC") and (cuadruplo[3] != "VF"):
                assignValor(getValor(cuadruplo[1]), cuadruplo[3])
    
    pilaMemoriaLocal.pop()
    pilaMemoriaTemp.pop()

# Regresa el valor de la direccion solicitada
def getValor(direccion):
    global pilaMemoriaLocal
    global pilaMemoriaTemp
    global memoriaGlobal
    global memoriaConstante

    if(isinstance(direccion, str)):
        pointer = direccion[1:]
        direccion = getValor(int(pointer))

    if direccion > 1999 and direccion < 11000:
        return memoriaGlobal.get(direccion)
    elif direccion > 10999 and direccion < 20000:
        return pilaMemoriaLocal[-1].get(direccion)
    elif direccion > 19999 and direccion < 32000:
        return pilaMemoriaTemp[-1].get(direccion)
    elif direccion > 31999 and direccion < 44000:
        return memoriaConstante.get(direccion)

# Le asigna el valor enviado a la direccion solicitada
def assignValor(valor, direccion):
    global pilaMemoriaLocal
    global pilaMemoriaTemp
    global memoriaGlobal
    global memoriaConstante

    if(isinstance(direccion, str)):
        pointer = direccion[1:]
        direccion = getValor(int(pointer))

    if direccion > 1999 and direccion <  11000:
        memoriaGlobal.assign(direccion,valor)
    elif direccion > 10999 and direccion < 20000:
        pilaMemoriaLocal[-1].assign(direccion, valor)
    elif direccion > 19999 and direccion < 32000:
        pilaMemoriaTemp[-1].assign(direccion, valor)
    elif direccion > 31999 and direccion < 44000:
        memoriaConstante.assign(direccion, valor)

# Lee un input del usuario y lo regresa segun su tipo
def readValor(direccion):
    resultado = input()
    if (direccion > 1999 and direccion <  5000) or (direccion > 10999 and direccion <  14000):
        return int(resultado)
    elif (direccion > 4999 and direccion <  4999) or (direccion > 13999 and direccion <  17000):
        return float(resultado)
    return resultado


if __name__ == "__main__":
    f=open("exec.hl", "r")
    fl = f.read()
    f.close()
    program = fl.split("\n")
    readFile(program)
    runContext()