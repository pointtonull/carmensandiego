#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from decoradores import Verbose
from logging import debug
from math import sin, cos, radians, asin, sqrt, atan2
import re
import sys
import time
import topocoding
import urllib2

VERBOSE = 4

class clase_estacion:
    def __init__(self, nombre, latitud, longitud, altitud=0, temp_normal=20,
        id=None, id_tipo="smn"):

        self.nombre = nombre
        self.coordenadas = (latitud, longitud, altitud)
        self.latitud = latitud
        self.longitud = longitud
        self.altitud = altitud
        self._id = id
        self._id_tipo = id_tipo
        self.temperatura = temp_normal
        self._tiempo_temperatura = None

    def __repr__(self, *args):
        return "%s: (%f, %f, %d)" % (self.nombre, self.latitud, self.longitud,
            self.altitud)

    def __getitem__(self, *args):
        return self.coordenadas.__getitem__(*args)

    def calcular_distancia(self, estacion):
        return calcular_distancia(self.latitud, self.longitud, 
            estacion.latitud, estacion.longitud)


    def obtener_temperatura(self):
        if (self._tiempo_temperatura and (time.time()
            - self._tiempo_temperatura < 180)):
            return float(self.temperatura)

        elif self._id:
            if self._id_tipo == "smn":
                url = """http://www.smn.gov.ar/?mod=dpd&id=21&e=""" + self._id

                try:
                    pagina = urllib2.urlopen(url)
                    html = "".join(pagina.readlines())

                except urllib2.URLError:
                    debug("No se pudo descargar la página")
                    self._tiempo_temperatura = time.time()
                    return float(self.temperatura)

                else:
                    filtro = r"""TEMPERATURA.*?>(?P<temp>[\d.]*?)[ Cc]"""

                    try:
                        self.temperatura = float(re.search(filtro, html,
                            re.MULTILINE|re.UNICODE).group('temp'))

                    except AttributeError:
                        print(url)
                        raise

                    self._tiempo_temperatura = time.time()

                    return float(self.temperatura)
            else:
                debug("Obteniendo de otra fuente")
    
        else:
            return calcular_temperatura(self.latitud, self.longitud,
                self.altitud)


def calcular_temperatura(latitud, longitud, altitud=None):
    """Calcula la temperatura de la estación sin mediciones propias a partir de
la distancia cubica y la diferencia de altitudes con respecto a referencias 
medidas.

    latitud, longitud, altitud » ºC"""

    debug("Calculando la temperatura en función de mediciones proximas y"
        "variaciones de altitud")

    if not altitud:
        altitud = topocoding.get_elevations(((latitud, longitud),))[0]
            
    # Calcúlo la distancia a las estaciones conocidas
    distancias = []
    for estacion in estaciones:
        if estaciones[estacion]._id:
            distancias.append(
            (
                calcular_distancia(
                    latitud, longitud,
                    estaciones[estacion].latitud, estaciones[estacion].longitud
                    ),
                estaciones[estacion]
            ))

    cercanas = [(cercana[0], cercana[1]) for cercana in sorted(distancias)
        if cercana[0] != 0][:3]

    distancias = [cercana[0] for cercana in cercanas]
    altitudes = [cercana[1].altitud for cercana in cercanas]
    temperaturas = [cercana[1].obtener_temperatura() for cercana in cercanas]

    # Diferencias de altitud a referencia
    da1 = altitudes[1] - altitudes[0]
    da2 = altitudes[2] - altitudes[0]
    # Diferencias de temperatura a referencia
    dt1 = temperaturas[1] - temperaturas[0]
    dt2 = temperaturas[2] - temperaturas[0]
# Pendiente y ordenadas al origen
    pendiente = (dt1 / da1 + dt2 / da2) / 2
    tnm = [0, 0, 0]
    tnm[0] = temperaturas[0] - pendiente * altitudes[0]
    tnm[1] = temperaturas[1] - pendiente * altitudes[1]
    tnm[2] = temperaturas[2] - pendiente * altitudes[2]

# Distancia promedio (para diferencia cubica)
    dp = sum((cercana[0] for cercana in cercanas)) / 3.
# Temperatura a nivel del mar por distribución cubica
    tnmc  = (tnm[0] * (dp / distancias[0]) ** 3 
        + tnm[1] * (dp / distancias[1]) ** 3 
        + tnm[2] * (dp / distancias[2]) ** 3 ) / ((dp / distancias[0]) ** 3 
        + (dp / distancias[1]) ** 3 + (dp / distancias[2]) ** 3 )

    return tnmc + altitud * pendiente
            

def g2r(grados, minutos=0, segundos=0):
    """grados a radianes"""
    return radians(grados + (minutos / 60.) + (segundos / 3600.))


def g2d(grados, minutos=0, segundos=0):
    """grados a decimal"""
    return grados + (minutos / 60.) + (segundos / 3600.)


def velocidad_del_sonido(temperatura=20):
    """Devuelve la velocidad del sonido dependiendo de la temperatura en
celsius según la ecuación de Laplace.

    ºC » m/s"""

    return 331300 * (1 + temperatura / 273.15) ** 0.2

estaciones = {
    "ttg" : clase_estacion("Tartagal",
        -g2d(22, 33, 02), -g2d(63, 48, 35), 506, 26, "87022"),
    "sal" : clase_estacion("Salta",
        -g2d(24, 47, 34), -g2d(65, 24, 29), 1181, 21, "87047"),
    "lqc" : clase_estacion("La Quiaca",
        -22.116754, -65.599923, 3467, 15, "87047"),
    "rvd" : clase_estacion("Rivadavia",
        -24.183576, -62.886453, 211, 23, "87065"),
    "ora" : clase_estacion("San Ramón de la Nueva Orán",
        -g2d(23, 9), -g2d(64, 19), 355, 27, "87016"),
    "juj" : clase_estacion("San Salvador Jujuy",
        -g2d(24, 14), -g2d(65, 16), 1239, 21, "87046"),
    "sde" : clase_estacion("Santiago del Estero",
        -g2d(27, 46), -g2d(64, 17), 194, 23, "87129"),
    "res" : clase_estacion("Resistencia", 
        -27.440878, -58.99581, 54, 26, "87155"),
    "prq" : clase_estacion("Roque Saenz Peña",
        -26.783324, -60.45002, 93, 24, "87148"),
    "spd" : clase_estacion("San Pedro",
        -24.227615, -64.870024, 593),
    "cmd" : clase_estacion("Coronel Modes",
        -25.2816, -65.4668, 1106, 27),
    }

# bjo*, tarija, yacuiba, nueva asuncion, boqueron, 


def calcular_tardanza_sonido(lat1, lon1, alt1, lat2, lon2, alt2):
    """Calcula la tardanza del sonido entre dos puntos geodesicos teniendo en
cuenta la temperatura del aire y la altitud

coordenadas + altitudes » s"""

    distancia = calcular_distancia(lat1, lon1, lat2, lon2)
    n = int(distancia / 10000.)

    nodos = [(
        lat1 + ((lat2 - lat1) / n) * nodo,
        lon1 + ((lon2 - lon1) / n) * nodo,
        alt1 + ((alt2 - alt1) / n) * nodo,
        )
        for nodo in xrange(1, n + 1)]

    tmp_nodos = sum((calcular_temperatura(nodo[0], nodo[1], nodo[2])
        for nodo in nodos)) / len(nodos)

# Obtiene la distancia real a partir de Pitagoras

    distancia = sqrt(distancia ** 2 + (alt1 - alt2) ** 2)

    return distancia / velocidad_del_sonido(tmp_nodos)


@Verbose(VERBOSE)
def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Devuelve la distancia, en metros, entre los puntos especificados por
sus coordenadas geodesicas con una precición increible.

    latitud, longitud » m
    """

    lat1, lon1 = radians(lat1), radians(lon1)
    lat2, lon2 = radians(lat2), radians(lon2)

#   Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    sin2lat = sin(dlat / 2) ** 2
    sin2lon = sin(dlon / 2) ** 2

    a = sin2lat + cos(lat1) * cos(lat2) * sin2lon
    c = 2 * asin(min(1, sqrt(a)))

#    Calculo del radio tendiendo en cuenta la excentricidad de la tierra
    radio = 6378140
    e = .01671

    radio *= (1 - e ** 2) / (1 - e ** 2 * sin((lat1 + lat2) / 2.) ** 2) ** 1.5

    return radio * c


def main():
    pass


if __name__ == "__main__":
    exit(main())
