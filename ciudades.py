#!/usr/bin/env python
#-*- coding: utf-8 -*-

ciudades = {
    ('Buenos Aires', 'Rio de Janeiro'): 1960, 
    ('Rio de Janeiro', 'Londres'): 9240,
    ('Nueva York', 'Londres'): 5570,
    ('Buenos Aires', 'Mexico DF'): 7360,
    ('Rio de Janeiro', 'Beijing'): 17300,
    ('Nueva York', 'Paris'): 5840,
    ('Londres', 'Nueva Delhi'): 6700,
    ('Beijing', 'Nueva Delhi'): 3790,
    ('Sidney', 'Tokio'): 7780,
    ('Beijing', 'Tokio'): 2100,
    ('Paris', 'Tokio'): 9720,
    ('Mexico DF', 'Paris'): 9200,
    ('Mexico DF', 'Nueva Delhi'): 14650,
    ('Buenos Aires', 'El Cairo'): 11790,
    ('Sidney', 'El Cairo'): 14370,
    ('Nueva York', 'El Cairo'): 9000
         }
         
opciones = {
    '1': 'Buenos Aires',
    '2': 'Rio de Janeiro',
    '3': 'Nueva York',
    '4': 'Tokio',
    '5': 'Londres',
    '6': 'Paris',
    '7': 'El Cairo',
    '8': 'Sidney',
    '9': 'Nueva Delhi',
    '10': 'Beijing',
    '11': 'Mexico DF'
    }

def menu_ciudades():
    print u"""
    Ciudades
    
        [1]  : Buenos Aires     [6]  : Paris       [11] : Mexico DF
        [2]  : Rio de janeiro   [7]  : El Cairo
        [3]  : Nueva York       [8]  : Sidney
        [4]  : Tokio            [9]  : Nueva Delhi
        [5]  : Londres          [10] : Beijing
                    
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
