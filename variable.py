######################################################################### 
# Clase variable
######################################################################### 
class Variable:
    def __init__(self, fila, col, ori, tam, longitud):
        self.fila=fila
        self.col=col
        self.ori=ori #orientación
        self.tam=tam #tamaño dominio
        self.longitud=longitud
        self.podada = []


    def getOrientation(self):
        return self.ori
    