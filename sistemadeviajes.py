#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Sistema de viajes
#para CarmenSanDiego

from os import system
from time import sleep
from ciudades import ciudades 


def viajar(origen, destino):
    if origen != destino:
        kilometros = distancia(origen, destino)
        horas = kilometros / 600
        sleep(.1)
        if kilometros != -1:
            print 'Viajando desde %s' %(origen,)
            for i in xrange(kilometros/100):
                print '.',
                #sleep(.1)            
            print 'Llegamos a %s en %s Horas' %(destino, horas)
        else:
            print 'No hay una conexion entre esas dos ciudades'
            print 'Vea las conexiones y pruebe haciendo escalas'
    else:
        print 'Ya se encuentra en esa ciudad'
     
        

def distancia(origen, destino):
    try:
        return ciudades[(origen, destino)]
    except KeyError:
        try:
            return ciudades[(destino, origen)]
        except KeyError:
            return -1

opciones = {
    '1': 'Buenos Aires',
    '2': 'Santiago de Chile',
    '3': 'Nueva York',
    '4': 'Tokio'
    }

def menu():
    print u"""
    Ciudades
    
        [1] : Buenos Aires
        [2] : Santiago de Chile
        [3] : Nueva York
        [4] : Tokio 
    """

def menu2():
    print u"""
    Menu
    
        [1] : Viajar
        [2] : Ver conexiones
        [3] : Salir
    """

def elegir_viaje():
    system('clear')
    origen, destino = elegir_origen_y_destino()
    viajar(origen, destino)

def ver_conexiones():
    system('clear')
    menu()
    opcion = raw_input('Elija una ciudad para ver sus conexiones : ')
    
    try:
        ciudad = opciones[opcion]
    except KeyError:
        print 'La opcion no corresponde a una ciudad'
    
    claves = ciudades.keys()
    for clave in claves:
        if ciudad in clave:
            print clave
    
funciones = {
    '1': elegir_viaje,
    '2': ver_conexiones,
    '3': quit 
    }    
    
def elegir_origen_y_destino(opcion = 0):
    def elige_origen():
        menu()
        o = raw_input('Elige origen : ')
        while not o:
            print 'no ingreso un valor'
            o = raw_input('Elige origen : ')
        try:
            origen = opciones[o]
        except KeyError:
            print 'Opcion incorrecta'
        return origen 
            
    def elige_destino():
        menu()
        d = raw_input('Elige destino : ')
        while not d:
            print 'no ingreso un valor'
            d = raw_input('Elige destino : ')
        try:
            destino = opciones[d]
        except KeyError:
            print 'Opcion incorrecta'
        return destino
        
    if opcion == 1:
        elige_origen()
    elif opcion == 2:
        elige_destino()
    else:
        return (elige_origen(), elige_destino())
        
    

def main():
    system('clear')
    menu2()
    opcion = raw_input('Elige opcion : ')
    while opcion != '3':
        try:
            system('clear')
            funciones[opcion]()
        except KeyError:
            print 'Opción fuera de rango'
    
        menu2()
        opcion = raw_input('Ingrese opcion: ')         
        
    
        
    

if __name__ == '__main__':
    main()
    
    
    
