#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Sistema de viajes
#para CarmenSanDiego

from os import system
from time import sleep
from time import ctime, mktime
from ciudades import ciudades, menu_ciudades, opciones, origen_y_destino 

jugadores = {}

class detective():
    def __init__(self, lugar, hora):
        self.lugar_actual = lugar
        self.hora_actual = hora
    
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

    def elegir_viaje(self):
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
        pass
    
    def arresto(self):
        pass
    


def juego_nuevo():
    system('clear')
    print u"""
    +------------------------------+
    |Cuartel General de la interpol|
    +------------------------------+
        
    Lunes 9:00 am
        
    Identificate por favor
    """
    nombre = raw_input('Nombre : ')
    jugadores[nombre] = detective('Buenos Aires', ctime())
    print 'Tu nombre no se encuentra en la base de datos'
    sleep(1)
    print ''
    print 'Tu rango actual es Novato'
    sleep(3)
    system('clear')
    print u"""
                                *** Noticias ***
        Tesoro nacional robado en Buenos Aires
        
        El botin ha sido identificado como el sable curvo de San Martin.    
        Un sospechoso de sexo femenino fue visto en la escena del crimen
        ----------------------------------------------------------------
        
        Tu misión:
            Perseguir al ladron desde Buenos Aires
            hasta su escondite y arrestarlo. Tienes hasta el domingo
            a las 23:00 para arrestarlo.
        ----------------------------------------------------------------
        
        Buena suerte novato %s
    """ %(nombre,)
    sleep(10)
    control_central(jugadores[nombre])



def control_central(novato):
    system('clear')
    print u"""
    
        %s | %s
        
        +-----+ +------+ +------+ +-------+ +-----+
        |     | |      | |      | |       | |     |
        | ver | |Viajar| |Pistas| |Arresto| |Salir|
        |     | |      | |      | |       | |     |
        +-----+ +------+ +------+ +-------+ +-----+
          [1]      [2]      [3]      [4]      [5]
    """ %(novato.lugar_actual, novato.hora_actual)
    opcion = raw_input('Ingrese opcion : ')
    while opcion != '5':
        if opcion == '1':
            novato.ver_conexiones()
        elif opcion == '2':
            novato.elegir_viaje()
        elif opcion == '3':
            novato.pistas()
        elif opcion == '4':
            novato.arresto()
        else:
            print 'opcion fuera de rango'
            system('clear')
        print u"""
            
            +-----+ +------+ +------+ +-------+ +-----+
            |     | |      | |      | |       | |     |
            | ver | |Viajar| |Pistas| |Arresto| |Salir|
            |     | |      | |      | |       | |     |
            +-----+ +------+ +------+ +-------+ +-----+
              [1]      [2]      [3]      [4]      [5]
        """
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
    if opcion != '2':
        try:
            system('clear')
            funciones[opcion]()
        except KeyError:
            print 'Opción fuera de rango'
    

if __name__ == '__main__':
    main()
    
    
    
