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


    def getOrientation(self):
        return self.ori
    
#LO HICE PARA COMPROBAR EL CONSTRUCTOR YA QUE LLEVABA TIEMPO SIN PROGRAMAR Y MENOS EN PYTHON
#def show(self):
#    print(self.fila, " y ", self.col)
#C=Variable(1,3,'vertical')
#C.show()