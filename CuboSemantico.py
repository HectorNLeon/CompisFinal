class CuboSemantico:
    def __init__(self):
        self.cuboSem = {
            "int" : {
                "int" : {
                    "+" : "int",
                    "-" : "int",
                    "*" : "int",
                    "/" : "float",
                    "==" : "bool",
                    "!=" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    "|" : "error",
                    "&" : "error",
                    "=" : "int"
                },
                "float" : {
                    "+" : "float",
                    "-" : "float",
                    "*" : "float",
                    "/" : "float",
                    "==" : "bool",
                    "!=" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "char" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" : "error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                }
            },
            "float" : {
                "int" : {
                    "+" : "float",
                    "-" : "float",
                    "*" : "float",
                    "/" : "float",
                    "==" : "bool",
                    "!=" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "float" : {
                    "+" : "float",
                    "-" : "float",
                    "*" : "float",
                    "/" : "float",
                    "==" : "bool",
                    "!=" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    "|" : "error",
                    "&" : "error",
                    "=" : "float"
                },
                "char" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error" 
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                }
            },
            "char" : {
                "int" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error" 
                },
                "float" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "char" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "bool",
                    "!=" : "bool",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "char"
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                }
            },
            "bool" : {
                "int" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error" 
                },
                "float" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "char" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "bool",
                    "!=" : "bool",
                    ">" : "error",
                    "<" :"error",
                    "|" : "bool",
                    "&" : "bool",
                    "=" : "bool"
                }
            }
        }

    def semantica(self, tipo1, tipo2, operacion):
        return self.cuboSem[tipo1][tipo2][operacion]

if __name__ == "__main__":
    cuboSem = CuboSemantico()
    print(cuboSem.semantica("int","float","+"))