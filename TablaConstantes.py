from TablaVariables import TablaVariables

class TablaConstantes(TablaVariables):

    def __init__(self):
        TablaVariables.__init__(self)
    
    def exportConstantes(self, filename):
        f= open(filename,"a+")
        f.write("TablaConstantes:\n")
        for name in self.varDict:
            constante = str(name) + " " + str(self.varDict[name]["dir"]) + "\n"
            f.write(constante)
        f.close()