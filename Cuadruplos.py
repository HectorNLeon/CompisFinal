class Cuadruplos(object):
    def __init__(self):
        self.stack = []
        self.count = 0

    def addCuadruplo(self, op, opDerecha, opIzquierda, to):
        self.stack.append([op,opDerecha,opIzquierda,to])
        self.count += 1
    
    def addTo(self, count, to):
        self.stack[count][3] = to
    
    def printCuadruplos(self):
        i = 0
        for cuadruplo in self.stack:
            print(i, ")","Cuadruplo:", cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
            i += 1
       
    def getCount(self):
        return self.count

    def exportCuadruplos(self, filename):
        f= open(filename,"a+")
        f.write("Cuadruplos:\n")
        for cuadruplo in self.stack:
            cuad = str(cuadruplo[0]) + ";" + str(cuadruplo[1]) + ";" + str(cuadruplo[2]) + ";" + str(cuadruplo[3]) + "\n"
            f.write(cuad)
        f.close()