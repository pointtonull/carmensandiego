#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Demo del remake
#de CarmenSanDiego


from os import system
from time import sleep
from time import ctime, mktime
from ciudades import ciudades, origen_y_destino
from misionypistas import mostrar_mision
from ladrones import dossier, orden_arresto 

jugadores = {}

class detective():
    def __init__(self, lugar, hora, rango):
        self.lugar_actual = lugar
        self.hora_actual = hora
        self.rango_actual = rango
    
    
    def viajar(self, origen, destino):
        '''muestra, si es posible, el viaje entre 2 ciudades 
        y cuanto dura en horas'''
        if origen != destino:
            kilometros = self.distancia(origen, destino)
            horas = kilometros / 600
            sleep(1)
            if kilometros != -1:
                print 'Viajando desde %s' %(origen,)
                for i in xrange(kilometros/100):
                    print '.',
                    #sleep(.1)            
                print 'Llegamos a %s en %s Horas' %(destino, horas)
                self.lugar_actual = destino
            else:
                print 'No hay una conexion entre esas dos ciudades'
                print 'Vea las conexiones y pruebe haciendo escalas'
        else:
            print 'Ya se encuentra en esa ciudad'
    
     
    def distancia(self, origen, destino):
        '''Averigua la distancia en kilometros, si es que existe una conexion
        directa, entre dos ciudades'''
        try:
            return ciudades[(origen, destino)]
        except KeyError:
            try:
                return ciudades[(destino, origen)]
            except KeyError:
                return -1

    def elegir_destino(self):
        system('clear')
        destino = origen_y_destino(2)
        self.viajar(self.lugar_actual, destino)

    def ver_conexiones(self):
        '''dada una ciudad, muestra todas las conexiones directas 
        con otras ciudades'''
        system('clear')
        ciudad = self.lugar_actual
        claves = ciudades.keys()
        for clave in claves:
            if ciudad in clave:
                print clave
    
    def pistas(self):
        print 'Falta implementar'
    
    def arresto(self):
        orden_arresto()
    


def juego_nuevo():
    system('clear')
    print u"""
    +------------------------------+
    |Cuartel General de la interpol|
    +------------------------------+
        
    %s
        
    Identificate por favor
    """ %(ctime())
    nombre = raw_input('Nombre : ')
    if nombre not in jugadores.keys():
        jugadores[nombre] = detective('Buenos Aires', ctime(), 'Novato')
        print 'Tu nombre no se encuentra en la base de datos'
        sleep(1)
        print ''
        print 'Tu rango actual es %s' %(jugadores[nombre].rango_actual,)
        sleep(3)
    else:
        print 'Has sido identificado'
        sleep(1)
        print ''
        print 'Tu rango actual es %s' %(jugadores[nombre].rango_actual,)
        sleep(3)
    system('clear')
    mostrar_mision()
    sleep(8)
    print 'Buena suerte %s %s'%(jugadores[nombre].rango_actual, nombre)
    sleep(2)
    control_central(jugadores[nombre])



def menu_central(novato):
    print u"""
    %s | %s
        
        +---+ +------+ +------+ +-------+ +------+ +-------+
        |   | |      | |      | |       | |      | |       |
        |ver| |Viajar| |Pistas| |Arresto| |misión| |Dossier|
        |   | |      | |      | |       | |      | |       |
        +---+ +------+ +------+ +-------+ +------+ +-------+
         [1]     [2]      [3]      [4]      [5]       [6]
          
        +-----+
        |     |
        |Salir|
        |     |
        +-----+
          [7] 
    """ %(novato.lugar_actual, novato.hora_actual)

def control_central(novato):
    system('clear')
    menu_central(novato)
    opcion = raw_input('Ingrese opcion : ')
    while opcion != '7':
        if opcion == '1':
            novato.ver_conexiones()
        elif opcion == '2':
            novato.elegir_destino()
        elif opcion == '3':
            novato.pistas()
        elif opcion == '4':
            novato.arresto()
        elif opcion == '5':
            mostrar_mision()
        elif opcion == '6':
            dossier()
        else:
            print 'opcion fuera de rango'
            system('clear')
        menu_central(novato)
        opcion = raw_input('Ingrese opcion : ')


def menu():
        '''simple menu con las opciones del programa'''
        print u"""
        Demo Juanita la Ladrona
        
            [1] : Nuevo juego
            [2] : Salir
        """    

funciones = {
    '1': juego_nuevo,
    '2': quit
    }    
    

def main():
    system('clear')
    menu()
    opcion = raw_input('Elige opcion : ')
    while opcion != '2':
        try:
            system('clear')
            funciones[opcion]()
        except KeyError:
            print 'Opción fuera de rango'
        
        system('clear')
        menu()
        opcion = raw_input('Elige opcion : ')

if __name__ == '__main__':
    main()
    
    
    
