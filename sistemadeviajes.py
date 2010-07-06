#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Sistema de viajes
#para CarmenSanDiego

from os import system
from time import sleep
from ciudades import ciudades, menu_ciudades, opciones, origen_y_destino 


def viajar(origen, destino):
    '''muestra, si es posible, el viaje entre 2 ciudades 
    y cuanto dura en horas'''
    if origen != destino:
        kilometros = distancia(origen, destino)
        horas = kilometros / 600
        sleep(1)
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
    '''Averigua la distancia en kilometros, si es que existe una conexion
    directa, entre dos ciudades'''
    try:
        return ciudades[(origen, destino)]
    except KeyError:
        try:
            return ciudades[(destino, origen)]
        except KeyError:
            return -1

def menu():
    '''simple menu con las opciones del programa'''
    print u"""
    Menu
    
        [1] : Viajar
        [2] : Ver conexiones
        [3] : Salir
    """

def elegir_viaje():
    system('clear')
    origen, destino = origen_y_destino()
    viajar(origen, destino)

def ver_conexiones():
    '''dada una ciudad, muestra todas las conexiones directas 
    con otras ciudades'''
    system('clear')
    menu_ciudades()
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
    

        
    

def main():
    system('clear')
    menu()
    opcion = raw_input('Elige opcion : ')
    while opcion != '3':
        try:
            system('clear')
            funciones[opcion]()
        except KeyError:
            print 'Opción fuera de rango'
    
        menu()
        opcion = raw_input('Ingrese opcion: ')         
        
    
        
    

if __name__ == '__main__':
    main()
    
    
    
