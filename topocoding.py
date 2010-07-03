#!/usr/bin/env python
#-*- coding: UTF-8 -*-

r"""
    >>> get_elevations([("  1° 9'53.06\"S ", "  32°46'14.33\"E "), (" 45°14'55.42\"N ", "  21°45' 3.83\"E "), (" 45° 3'42.74\"N ", " 103° 3'37.64\"O "), (" 24°46'54.74\"S ", "  65°23'45.99\"O "), (" 27°26'27.24\"S ", "  58°59'44.88\"O "), ])
    [1134, 199, 826, 1424, 54]
"""

import re
import browser
import urllib

import debug as dmodule
debug = dmodule.debug
#dmodule.VERBOSE = 0
from decoradores import Verbose
from math import sqrt, floor

CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.!*()"
MAXCOORDINATES = 280
URL = """http://www.topocoding.com/api/altitude_v1.php?%s"""
REFERER = """http://www.topocoding.com/demo/google.html"""
KEY = "BGMCCPGOZNKXPZC"
ID = 1
VERBOSE = 4

#@Verbose(VERBOSE)
def parse_coordinate(value):
    r"""
    Recibe una coordenada, latitud o longitud, la normaliza y la devuelve como
    flotante.
    string > float

    >>> parse_coordinate("  1° 9'53.06\"S ") - (-1.1647) < 0.01
    True
    >>> parse_coordinate("  32°46'14.33\"E ") - (32.7706) < 0.01
    True

    """
    value = str(value).upper()
    regex = r"""([A-z]|[\+\-]|\d+\.?\d*)"""
    arr = re.findall(regex, value)
    divider = 1
    result = 0
    sign = 1
    for i in xrange(len(arr)):
        if arr[i] in "NE+":
            sign = 1
        elif arr[i] in "SWO-":
            sign = -1
        else:
            result += float(arr[i]) / divider
            divider *= 60
    return round(result * sign, 4)


#@Verbose(VERBOSE)
def encode_coordinates(coordinates):
    r"""
        Codifica las coordenadas para ofuscar la llamada (bleh).
        Recibe una lista lista con pares ordenados de coordenadas.
        Devuelve un string con las coordenadas codificadas.
        ((lat, lon), (lat2, lon2)...) > string


    >>> encode_coordinates([('  1° 9\'53.06"S ', '  32°46\'14.33"E ')])
    ')gMtnAx'
    >>> encode_coordinates([(' 27°26\'27.24"S ', '  58°59\'44.88"O ')])
    '65HVm1-'
    >>> encode_coordinates([(-25.281600000000001, -65.466800000000006)])
    '74vFun3'
    """

    result = ""
    for coordinate in coordinates:

        lat = parse_coordinate(coordinate[0])
        lon = parse_coordinate(coordinate[1])
        
        if lat < 0:
            lat += 180

        lat = lat / 180.
        lat = lat - floor(lat)

        if lon < 0:
            lon += 360

        lon = lon / 360.
        lon = lon - floor(lon)

        for i in xrange(3):
            lat = lat * len(CHARS)
            index = int(floor(lat))
            lat -= index
            result += CHARS[index]

            lon = lon * len(CHARS)
            index = int(floor(lon))
            lon -= index
            result += CHARS[index]

        isqrt = lambda x: int(sqrt(x))


        lat *= isqrt(len(CHARS))
        lon *= isqrt(len(CHARS))

        index = int(floor(lat) * isqrt(len(CHARS)) + floor(lon))
        try:
            result += CHARS[index]
        except IndexError:
            result += "-" #HACK: ??

    return result


#@Verbose(VERBOSE)
def get_elevations(coordinates, browser_instance=None):
    r"""
    >>> get_elevations([('  1° 9\'53.06"S ', '  32°46\'14.33"E ')])
    [1134]
    >>> get_elevations([(' 27°26\'27.24"S ', '  58°59\'44.88"O ')])
    [54]
    """
    b = browser_instance if browser_instance else browser.BROWSER()
    b._twillbrowser._browser.addheaders.append(("referer", REFERER))
    if type(coordinates) is not str:
        coordinates = encode_coordinates(coordinates)

    url = URL % urllib.urlencode({"l" : coordinates, "key" : KEY, "id" : ID})
    output = b.get_html(url, cache=60*60*24*30)

    regex = r"""[,\[](\d+)"""
    altitudes = [int(alt) for alt in re.findall(regex, output) if alt]

    return altitudes


if __name__ == "__main__":
    import doctest
    print("Modulo probado, %d tests fallaron, %d funcionaron debidamente"
        % doctest.testmod())
