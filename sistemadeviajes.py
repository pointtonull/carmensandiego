#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Sistema de viajes
#para CarmenSanDiego

from os import system
from time import sleep

ciudades = {
    ('Buenos Aires', 'Santiago de Chile'): 1139, 
    ('Santiago de Chile','Nueva York'): 8206,
    ('Nueva York', 'Buenos Aires'): 8491
         }
          

def viajar(origen, destino):
    print 'Viajando desde %s' %(origen,)
    kilometros = distancia(origen, destino)
    horas = kilometros / 600
    sleep(1)
    if kilometros != -1:
        for i in xrange(kilometros):
            print '.',
            sleep(.00001)            
        print 'Llegamos a %s en %s Horas' %(destino, horas)
    else:
        print 'No hay una conexion entre esas dos ciudades'

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
    '3': 'Nueva York'
    }

def menu():
    print u"""
    Ciudades
    
        [1] : Buenos Aires
        [2] : Santiago de Chile
        [3] : Nueva York 
    """

def main():
    system('clear')
    menu()
    o = raw_input('Elige origen : ')
    try:
        origen = opciones[o]
    except KeyError:
        print 'opcion incorrecta'
    system('clear')
    menu()
    d = raw_input('Elige destino : ')
    try:
        destino = opciones[d]
    except KeyError:
        print 'opcion incorrecta'
    system('clear')
    viajar(origen, destino)
    

if __name__ == '__main__':
    main()
    
    
    
