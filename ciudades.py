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
