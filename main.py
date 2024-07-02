import pygame
import tkinter
import time
import copy
from variable import *
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
from tablero import *
from dominio import *
from pygame.locals import *

GREY=(190, 190, 190)
NEGRO=(100,100, 100)
BLANCO=(255, 255, 255)

MARGEN=5 #ancho del borde entre celdas
MARGEN_INFERIOR=60 #altura del margen inferior entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda
FILS=4 # número de filas del crucigrama
COLS=4 # número de columnas del crucigrama

LLENA='*' 
VACIA='-'

#########################################################################
# Detecta si se pulsa el botón de FC
######################################################################### 
def pulsaBotonFC(pos, anchoVentana, altoVentana):
    if pos[0]>=anchoVentana//4-25 and pos[0]<=anchoVentana//4+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de AC3
######################################################################### 
def pulsaBotonAC3(pos, anchoVentana, altoVentana):
    if pos[0]>=3*(anchoVentana//4)-25 and pos[0]<=3*(anchoVentana//4)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de reset
######################################################################### 
def pulsaBotonReset(pos, anchoVentana, altoVentana):
    if pos[0]>=(anchoVentana//2)-25 and pos[0]<=(anchoVentana//2)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si el ratón se pulsa en la cuadrícula
######################################################################### 
def inTablero(pos):
    if pos[0]>=MARGEN and pos[0]<=(TAM+MARGEN)*COLS+MARGEN and pos[1]>=MARGEN and pos[1]<=(TAM+MARGEN)*FILS+MARGEN:        
        return True
    else:
        return False
    
######################################################################### 
# Busca posición de palabras de longitud tam en el almacen
######################################################################### 
def busca(almacen, tam):
    enc=False
    pos=-1
    i=0
    while i<len(almacen) and enc==False:
        if almacen[i].tam==tam: 
            pos=i
            enc=True
        i=i+1
    return pos
    
######################################################################### 
# Crea un almacen de palabras
######################################################################### 
def creaAlmacen():
    f= open('traza.txt', 'r', encoding="utf-8")
    lista=f.read()
    f.close()
    listaPal=lista.split()
    almacen=[]
   
    for pal in listaPal:        
        pos=busca(almacen, len(pal)) 
        if pos==-1: #no existen palabras de esa longitud
            dom=Dominio(len(pal))
            dom.addPal(pal.upper())            
            almacen.append(dom)
        elif pal.upper() not in almacen[pos].lista: #añade la palabra si no está duplicada        
            almacen[pos].addPal(pal.upper())           
    
    return almacen

######################################################################### 
# Imprime el contenido del almacen
######################################################################### 
def imprimeAlmacen(almacen):
    for dom in almacen:
        print (dom.tam)
        lista=dom.getLista()
        for pal in lista:
            print (pal, end=" ")
        print()


######################################################################### 
# Contador variables
######################################################################### 
def contador_variables(tablero, almacen):
    variables = []  
    # Para contar las variables en dirección horizontal
    for fila in range(tablero.getAlto()):
        col = 0
        while col < tablero.getAncho():
            if tablero.Ocupada(fila, col):
                col += 1
            else:
                longitud = 0
                while col+longitud < tablero.getAncho() and not tablero.Ocupada(fila, col+longitud):
                    longitud += 1
                if longitud > 1:
                        variables.append(Variable(fila, col, "h", dominio(almacen, longitud), longitud))
                col += longitud

    # Para contar las variables en dirección vertical
    for col in range(tablero.getAncho()):
        fila = 0
        while fila < tablero.getAlto():
            if tablero.Ocupada(fila, col):
                fila += 1
            else:
                longitud = 0
                while fila+longitud < tablero.getAlto() and not tablero.Ocupada(fila+longitud, col):
                    longitud += 1
                if longitud > 1:
                    variables.append(Variable(fila, col, "v", dominio(almacen, longitud), longitud))
                fila += longitud

    return variables

#########################################################################
# Devuelve el tamaño del dominio de la variable
######################################################################### 
def dominio(almacen, tam):
    return next((copy.deepcopy(i.lista) for i in almacen if i.tam == tam), None)
#UTILIZO FUNCIÓN NEXT PARA DEVOLVER EL PRIMER ELEMENTO QUE CUMPLA LA CONDICIÓN, EN ESTE CASO EL TAMAÑO DEL DOMINIO, SI NO SE ENCUENTRA NINGUNO DEVUELVE NONE

######################################################################### 
# Print de variables disponibles
######################################################################### 
def print_variables(variables):
    # Para imprimir la información de las variables encontradas
    i=0
    for variable in variables:
        i=i+1
        if(variable.ori == "h"): #Para poder imprimir la orientación de la variable de forma más clara
            orien="horizontal"
        else:
            orien="vertical"

        print(f"Nombre {i}: Posición {variable.fila}  {variable.col}, tipo: {orien}, Longitud: {variable.longitud}, dominio: {variable.tam}") 

######################################################################### 
# FC
######################################################################### 
def FC(tablero, variables, i):
    variable = variables[i]

    for a in variable.tam:
        palabra = a

        if len(variables)-1 == i:
            palabraEscrita(tablero, variable, palabra)
            return True
        
        elif forward(variables, i, palabra):
                palabraEscrita(tablero, variable, palabra)
                if FC(tablero, variables, i+1):
                    return True
        restaura(variables, palabra,i)

    return False

######################################################################### 
# Forward
######################################################################### 
def forward(variables, pos, palabra):
    for i in range(pos+1, len(variables)):
        it = 0
        Vacio = True
        aEliminar = []
        for l in variables[i].tam:
            if verifica(variables, palabra, l, pos, i): 
                #print("entrando")
                Vacio = False
            else:
                variables[i].podada.append([variables[i].tam[it], palabra])
                aEliminar.append(l)
            it += 1

        variables[i].tam = [l for l in variables[i].tam if l not in aEliminar]  #Eliminamos valores

        if not variables[i].tam: #Si no hay valores en el dominio, devolvemos False
            return False
    
    if Vacio:
        return False
    
    return True

######################################################################### 
# Función verifica junto a sus auxiliares
######################################################################### 
def verifica(variables, palabra, auxD, pos, auxP): 
    if misma_orientacion(variables, pos, auxP):
        return True
    
    celdasX, celdasY = obtener_celdas(variables, pos, palabra, auxP, auxD)
    hay_colision, celda = colision(celdasX, celdasY)
    
    if not hay_colision:
        return True
    
    return misma_celda_colision(palabra, auxD, celdasX, celdasY, celda)

def misma_orientacion(variables, pos, auxP): #Función auxiliar que verifica si dos celdas tienen la misma orientación
    return variables[pos].ori == variables[auxP].ori

def obtener_celdas(variables, pos, palabra, auxP, auxD): #Función auxiliar que obtiene las celdas ocupadas por las palabras
    ocupadasX = []
    ocupadasY = []

    for i in range(len(palabra)):
        if variables[pos].ori != 'h':
            ocupadasX.append([variables[pos].fila + i, variables[pos].col])
        else:
            ocupadasX.append([variables[pos].fila, variables[pos].col + i])
    
    for i in range(len(auxD)):
        if variables[auxP].ori != 'h':
            ocupadasY.append([variables[auxP].fila + i, variables[auxP].col])
        else:
            ocupadasY.append([variables[auxP].fila, variables[auxP].col + i])

    return ocupadasX, ocupadasY

def colision(lista1, lista2):
    # Convierto las listas a tuplas para poder compararlas
    conjunto1 = {tuple(elemento) for elemento in lista1}
    conjunto2 = {tuple(elemento) for elemento in lista2}
    
    interseccion = conjunto1.intersection(conjunto2)
    
    if interseccion:
        return True, list(interseccion.pop())
    else:
        return False, None

def misma_celda_colision(palabra, auxD, celdasX, celdasY, celda): #Función que verifica si la misma celda en dos listas tiene la misma letra
    if palabra[celdasX.index(celda)] == auxD[celdasY.index(celda)]:
        return True
    return False

######################################################################### 
# Restaura
######################################################################### 
def restaura(variables, pal, i):
    for l in range(i+1, len(variables)):
        aEliminar = []
        for x in variables[l].podada:
            if pal in x:
                reins = x[0]
                variables[l].tam.append(reins)
                aEliminar.append(x)
        eliminar(variables, l, aEliminar) #Eliminamos valores 

def eliminar(variables, l, aEliminar): 
    for pb in aEliminar:
        variables[l].podada.remove(pb)

######################################################################### 
# palabraEscrita, función que escribe la palabra en el tablero
######################################################################### 
def palabraEscrita(tablero, variable, palabra):
    if variable.ori == 'h': # Si es horizontal
        for i in range(0, variable.longitud):
            tablero.setCelda(variable.fila, variable.col + i, palabra[i])
    else:   
        for i in range(0, variable.longitud):
            tablero.setCelda(variable.fila + i, variable.col, palabra[i])


######################################################################### 
# AC3
######################################################################### 
def AC3(palabras, indice):
    if indice == len(palabras):
        return True
    
    hayCambio= False
    aEliminar = []
    variable_actual =palabras[indice]

    for valor in variable_actual.tam: 
        for indice_auxiliar, variable_auxiliar in enumerate(palabras): 
            if indice_auxiliar == indice:
                continue
                
            podados = [b for b in variable_auxiliar.tam if not verifica(palabras, valor, b, indice, indice_auxiliar)]
            if variable_auxiliar.tam == podados:
                aEliminar.append(valor)
                break

    if aEliminar:
        #print(f'Eliminando {aEliminar}')
        hayCambio = eliminarAC3(variable_actual, aEliminar)


    if len(variable_actual.tam) == 0:
        return False

    if hayCambio:
        return AC3(palabras, 0)

    return AC3(palabras, indice+1)

##############################################################################
# eliminarAC3, función que elimina los valores
##############################################################################
def eliminarAC3(variable_actual, aEliminar):
    for valor in aEliminar:
        variable_actual.tam.remove(valor)
    return True

#########################################################################  
# Principal
#########################################################################
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    pygame.init()
    
    reloj=pygame.time.Clock()
    
    anchoVentana=COLS*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+FILS*(TAM+MARGEN)+MARGEN
    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Crucigrama")
    
    botonFC=pygame.image.load("botonFC.png").convert()
    botonFC=pygame.transform.scale(botonFC,[50, 30])
    
    botonAC3=pygame.image.load("botonAC3.png").convert()
    botonAC3=pygame.transform.scale(botonAC3,[50, 30])
    
    botonReset=pygame.image.load("botonReset.png").convert()
    botonReset=pygame.transform.scale(botonReset,[50,30])
    
    palabras=[]
    almacen=creaAlmacen()
    #imprimeAlmacen(almacen)
    game_over=False
    tablero=Tablero(FILS, COLS)    
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición y calcular coordenadas matriciales                               
                pos=pygame.mouse.get_pos()                
                if pulsaBotonFC(pos, anchoVentana, altoVentana):
                    print("FC")
                    if len(palabras) == 0: #Para que si se pulsa primero en el botón del AC3 y a continuación en el botón del forward checking, este último pueda trabajar con los dominios ya reducidos por el AC3
                        palabras=contador_variables(tablero, almacen)
                    #print_variables(palabras) 
                    startFC = time.perf_counter()
                    res= FC(tablero, palabras, 0) #aquí llamar al forward checking
                    endFC = time.perf_counter()
                    print(f'Tiempo FC: {round(endFC-startFC, 7)} segundos')
                    if res==False:
                        MessageBox.showwarning("Alerta", "No hay solución")                                  
                elif pulsaBotonAC3(pos, anchoVentana, altoVentana):                    
                    print("AC3")
                    palabras = contador_variables(tablero, almacen)
                    print("DOMINIOS ANTES DEL AC3")   
                    print_variables(palabras)       
                    startAC3 = time.perf_counter()
                    res = AC3(palabras, 0)
                    endAC3 = time.perf_counter()
                    print("DOMINIOS DESPUES DEL AC3")
                    print_variables(palabras)
                    print(f'Tiempo AC3: {round(endAC3-startAC3, 7)}  segundos')
                    if res==False:
                        MessageBox.showwarning("Alerta", "No hay solución")   
                elif pulsaBotonReset(pos, anchoVentana, altoVentana):                   
                    tablero.reset()
                    palabras.clear()
                    MessageBox.showwarning("Alerta", "Se ha reseteado") 
                elif inTablero(pos):
                    colDestino=pos[0]//(TAM+MARGEN)
                    filDestino=pos[1]//(TAM+MARGEN)                    
                    if event.button==1: #botón izquierdo
                        if tablero.getCelda(filDestino, colDestino)==VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button==3: #botón derecho
                        c=askstring('Entrada', 'Introduce carácter')
                        tablero.setCelda(filDestino, colDestino, c.upper())   
            
        ##código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        pygame.draw.rect(screen, GREY, [0, 0, COLS*(TAM+MARGEN)+MARGEN, altoVentana],0)
        for fil in range(tablero.getAlto()):
            for col in range(tablero.getAncho()):
                if tablero.getCelda(fil, col)==VACIA: 
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif tablero.getCelda(fil, col)==LLENA: 
                    pygame.draw.rect(screen, NEGRO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                else: #dibujar letra                    
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    fuente= pygame.font.Font(None, 70)
                    texto= fuente.render(tablero.getCelda(fil, col), True, NEGRO)            
                    screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])             
        #pintar botones        
        screen.blit(botonFC, [anchoVentana//4-25, altoVentana-45])
        screen.blit(botonAC3, [3*(anchoVentana//4)-25, altoVentana-45])
        screen.blit(botonReset, [anchoVentana//2-25, altoVentana-45])
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True: #retardo cuando se cierra la ventana
            pygame.time.delay(500)
    
    pygame.quit()
 
if __name__=="__main__":
    main()
 
