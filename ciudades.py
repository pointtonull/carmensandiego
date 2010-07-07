#!/usr/bin/env python
#-*- coding: utf-8 -*-

ciudades = {
    ('Buenos Aires', 'Santiago de Chile'): 1139, 
    ('Santiago de Chile', 'Nueva York'): 8206,
    #('Nueva York', 'Buenos Aires'): 8491,
    #('Buenos Aires', 'Tokio'): 18374,
    ('Santiago de Chile', 'Tokio'): 17227,
    ('Nueva York', 'Tokio'): 10858
         }
opciones = {
    '1': 'Buenos Aires',
    '2': 'Santiago de Chile',
    '3': 'Nueva York',
    '4': 'Tokio'
    }

def menu_ciudades():
    print u"""
    Ciudades
    
        [1] : Buenos Aires
        [2] : Santiago de Chile
        [3] : Nueva York
        [4] : Tokio 
    """

def origen_y_destino(opcion = 0):
    ''' funcion para elegir ciudades de destino y origen de un menu, si
    se pasa como parametro un 1, retorna solo el origen, si se le pasa un 2
    retorna el destino y sin parametros devuelve una tupla (origen, destino)
    '''
   
    def elige_origen():
        menu_ciudades()
        o = raw_input('Elige origen : ')
        while not o:
            print 'no ingreso un valor'
            o = raw_input('Elige origen : ')
        try:
            origen = opciones[o]
            return origen
        except KeyError:
            print 'Opcion incorrecta'
         
            
    def elige_destino():
        menu_ciudades()
        d = raw_input('Elige destino : ')
        while not d:
            print 'no ingreso un valor'
            d = raw_input('Elige destino : ')
        try:
            destino = opciones[d]
            return destino
        except KeyError:
            print 'Opcion incorrecta'
        
        
    if opcion == 1:
        elige_origen()
    elif opcion == 2:
        elige_destino()
    else:
        return (elige_origen(), elige_destino())
