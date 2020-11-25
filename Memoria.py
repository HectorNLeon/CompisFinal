import sys

class Memoria(object):
    def __init__(self):
        self.memoria = {}

    def assign(self, dir, value):
        self.memoria[dir] = value

    def get(self, dir):
        if dir not in self.memoria:
            print("ERORR la variable pedida en la direccion", dir,"no tiene nada asignado")
            sys.exit()
        return self.memoria[dir]

    def printInfo(self):
        print(self.memoria)
