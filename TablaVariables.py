class TablaVariables(object):
    def __init__(self):
        self.varDict = {}

    def agregarVariable(self, name, varType, dir, isArray, dim1, dim2):
        self.varDict[name] = {
            "type": varType,
            "dir": dir,
            "isArray": isArray,
            "dim1": dim1,
            "dim2": dim2
        }

    def varExiste(self, name):
        if name in self.varDict:
            return True
        else:
            return False

    def buscarVariable(self, name):
        if self.varExiste(name):
            return self.varDict[name]
        else:
            return "ERROR"

    def buscarVariableDir(self, dir):
        for vars in self.varDict:
            if self.varDict[vars]["dir"] == dir:
                return self.varDict[vars]
        return "ERROR"
    
    def buscarVariableDirName(self, dir):
        for vars in self.varDict:
            if self.varDict[vars]["dir"] == dir:
                return vars
        return "ERROR"
    
    def getAllTypes(self):
        result = []
        for vars in self.varDict:
            result.append(self.varDict[vars]["type"])
        return result

    def lenOfVars(self):
        return len(self.varDict)
        
    def printVars(self):
        for vars in self.varDict:
            print("NombreVar:", vars, "Tipo:", self.varDict[vars]["type"])
