#!/usr/bin/env python
#-*- coding: utf-8 -*-

caco = {
    '1' : ('Carmen SanDiego', 'Femenino', 'Tenis', 'Rojo',
        'Descapotable', 'Collar'),
    '2' : ('Merey LaRoc', 'Femenino', 'Alpinismo', 'Castaño', 'Limusina',
        'Joyas'),
    '3' : ('Dazzle Annie Nonker', 'Femenino', 'Tenis', 'Rubio', 'Limusina',
        'Tatuaje'),
    '4' : ('Lady Agatha Wayland', 'Femenino', 'Musica', 'Rojo', 'Deportivo',
        'Anillo'),
    '5' : ('Katherine Drib', 'Femenino', 'Alpinismo', 'Castaño', 'Moto',
        'Tatuaje'),
    '6' : ['Len "Red" Bulk', 'Masculino', 'Alpinismo', 'Rojo', 
        'Descapotable', 'Tatuaje'],
    '7' : ('Scar Graynolt', 'Masculino', 'Croquet', 'Rojo', 'Limusina',
        'Anillo'),
    '8' : ('Ihor Ihorovitch', 'Masculino', 'Croquet', 'Rubio', 'Limusina',
        'Tatuaje'),
    '9' : ('Fast Eddie B', 'Masculino', 'Croquet', 'Negro', 'Descapotable',
        'Joyas'),
    '10': ('Nick Brunch', 'Masculino', 'Alpinismo', 'Negro', 'Moto',
        'Anillo')
    }

def dossier():
    print u"""
        [1] : Carmen SanDiego          [6]  : Len 'Red' Bulk
        [2] : Merey LaRoc              [7]  : Scar Graynolt
        [3] : Dazzle Annie Nonker      [8]  : Ihor Ihorovitch 
        [4] : Lady Agatha Wayland      [9]  : Fast Eddie B.
        [5] : Katherine Drib           [10] : Nick Brunch 
    """
    opcion = raw_input('Elija uno para ver su ficha : ')
    try:
        mostrar_ladron(caco[opcion])
    except KeyError:
        print 'Opcion fuera de rango'
        
def mostrar_ladron(ladron):
    print """
    *Nombre* : %s
    *Sexo* : %s  *Hobby* : %s
    *Pelo* : %s  *Coche* : %s
    *señas* : %s
    """ %(ladron)

sexo = {
    '1': 'Femenino',
    '2': 'Masculino'
    }

def elegir_sexo():
    print u"""
    Sexo
        [1] : Femenino
        [2] : Masculino
    """
    opcion = raw_input('Sexo : ')
    if not opcion:
        return ''
    try:
        return sexo[opcion]
    except KeyError:
        print 'Opcion fuera de rango'

hobby = {
    '1': 'Tenis',
    '2': 'Alpinismo',
    '3': 'Paracaidismo',
    '4': 'Musica',
    '5': 'Croquet'
    }

def elegir_hobby():
    print u"""
    Hobby
        [1] : Tenis
        [2] : Alpinismo
        [3] : Paracaidismo
        [4] : Musica
        [5] : Croquet
    """
    opcion = raw_input('Hobby : ')
    if not opcion:
        return ''
    try:
        return hobby[opcion]
    except KeyError:
        print 'Opcion fuera de rango'

pelo = {
    '1': 'Castaño',
    '2': 'Rojo',
    '3': 'Rubio',
    '4': 'Negro'
    }

def elegir_pelo():
    print u"""
    Pelo
        [1] : Castaño
        [2] : Rojo
        [3] : Rubio
        [4] : Negro
    """
    opcion = raw_input('Color de pelo : ')
    if not opcion:
        return ''
    try:
        return pelo[opcion]
    except KeyError:
        print 'Opcion fuera de rango'

senias = {
    '1': 'Joyas',
    '2': 'Anillo',
    '3': 'Collar',
    '4': 'Tatuaje',
    '5': 'Cojera'
    }

def elegir_senias():
    print u"""
    Señas
        [1] : Joyas
        [2] : Anillo
        [3] : Collar
        [4] : Tatuaje
        [5] : Cojera
    """
    opcion = raw_input('Señas : ')
    if not opcion:
        return ''
    try:
        return senias[opcion]
    except KeyError:
        print 'Opcion fuera de rango'
    
coche = {
    '1': 'Descapotable',
    '2': 'Limusina',
    '3': 'Deportivo',
    '4': 'moto'
    }

def elegir_coche():
    print u"""
    Coches
        [1] : Descapotable
        [2] : Limusina
        [3] : Deportivo
        [4] : moto
    """
    opcion = raw_input('Elija coche : ')
    if not opcion:
        return ''
    try:
        return coche[opcion]
    except KeyError:
        print 'Opcion fuera de rango'    

def buscar_ladron(descripcion):
    lista = []
    for ladron in caco.values():
        match = [x for x in descripcion if x in ladron]
        if len(match) == len(descripcion):
            lista.append(ladron[0])
    return lista 
    
            

def orden_arresto():
    sexo = elegir_sexo()
    hobby = elegir_hobby()
    pelo = elegir_pelo()
    senias = elegir_senias()
    coche = elegir_coche()
    
    descripcion = tuple([x for x in (sexo,hobby,pelo,coche,senias) if x])
    if descripcion:
        ladron = buscar_ladron(descripcion)
        return ladron
    else:
        print 'No ingreso ninguna caracteristica'

if __name__ == '__main__':
    orden_arresto()
