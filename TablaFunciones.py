from TablaVariables import TablaVariables

class TablaFunciones(object):
    def __init__(self):
        self.funcDict = {}

    def agregarFuncion(self, name, returnType, cuadNumber,dirGlobal):
        
        if not self.funcionExiste(name):
            self.funcDict[name] = {
                "returnType": returnType,
                "varTable": TablaVariables(),
                "paramTable": TablaVariables(),
                "numberParams" : 0,
                "cuadNumber": cuadNumber,
                "dirGlobal": dirGlobal
            }
            return "OK"
        else:
            if name == "main":
                return "main"
            else:
                return name

    def funcionExiste(self, name):
        if name in self.funcDict:
            return True
        else:
            return False

    def agregarVariables(self, nombreFuncion, listaVars):
        for variable in listaVars:
            if not self.funcDict[nombreFuncion]["varTable"].varExiste(variable[0]):
                self.funcDict[nombreFuncion]["varTable"].agregarVariable(variable[0], variable[1], variable[5], variable[2], variable[3], variable[4])
            #print("Se le esta agregando las variables", variable[0], variable[1])
            else: 
                return variable[0]
        return "OK"

    def getFuncion(self, name):
        if name in self.funcDict:
            return self.funcDict[name]
        else:
            return "ERROR"
        
    def buscarVariable(self, name, nombreFuncion):
        resultado = self.funcDict[nombreFuncion]["varTable"].buscarVariable(name)
        if(resultado == "ERROR"):
            resultado = self.funcDict[nombreFuncion]["paramTable"].buscarVariable(name)
        return resultado

    def agregarParamTable(self, nombreFunc, listaVariables):
        for elem in listaVariables:
            if not self.funcDict[nombreFunc]["paramTable"].varExiste(elem[0]):
                self.funcDict[nombreFunc]["paramTable"].agregarVariable(elem[0], elem[1], elem[5], elem[2], elem[3], elem[4])
            else: 
                return elem[0]
        self.funcDict[nombreFunc]["numberParams"] = self.funcDict[nombreFunc]["paramTable"].lenOfVars()
        return "OK"
    
    def printFunciones(self):
        for funciones in self.funcDict:
            print(funciones)

    def printFuncDetails(self):
        for funciones in self.funcDict:
            print("NombreFunc:", funciones, "Tipo", self.funcDict[funciones]["returnType"], "numberParams", self.funcDict[funciones]["numberParams"])
            print("Params:")
            self.funcDict[funciones]["paramTable"].printVars()
            print("Vars:")
            self.funcDict[funciones]["varTable"].printVars()
    
    def exportFunciones(self, filename):
        f= open(filename,"w+")
        f.write("TablaFunciones:\n")
        for functionName in self.funcDict:
            funcion = str(functionName) +  ";"+str(self.funcDict[functionName]["dirGlobal"])+";"+str(self.funcDict[functionName]["cuadNumber"])+"["
            for parameter in self.funcDict[functionName]["paramTable"].varDict:
                funcion += str(self.funcDict[functionName]["paramTable"].varDict[parameter]["dir"]) + ","
            if funcion[-1] == ',':
                funcion = funcion[:-1]
            funcion += "]\n"
            f.write(funcion)
        f.close()
        