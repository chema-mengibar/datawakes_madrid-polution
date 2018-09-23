# Class Mapservice

> **Version**: 1.0.0

> **Description:**
Creates a svg/png map from list of geometries, and provide some methods-tools

**Import module**
```py
from MapService import *
```
#

## Steps

### Reduce geometry boundaries points
Para acelerar el proceso de calculo y dibujo de las geometrias es necesario reducir el numero de puntos. Esto se hace de manera proporcional segun el numero de elementos que posse la geometria de cada forma, intentando reducir cada forma a 10 puntos.

### Geometry list
Difference between POlygon and Multipolygon to get the coordinates element:
```
regionData = {
            "coordinates": region["geometry"]["coordinates"][0],
            "properties": {
                "postalcode": region["properties"]["COD_POSTAL"],
                "region":"madrid"
            }
        }
```
Extend the properties with custom attributes.
Append each regionData in a list, for example **"geometryListPoints"**

## Methods

|  Read Input-file|  |
| ------ | ------ |
| .csvToDF(  ) | # |

<br>

|  Save Output-file|  |
| ------ | ------ |
| .objToJson(  ) | # |




## Usage

**.methodName(** param1, param2 **)** <br>
```py
if __name__ == '__main__':
  geometryListPoints = [ ... ]
  SVG_PATH = loader.getOutputPath( )["path"] + 'separate.svg'
  PNG_PATH = loader.getOutputPath( )["path"] + 'separate.png'
  mapservice = MapService( SVG_PATH, PNG_PATH, 800, 800, geometryListPoints )
  mapservice.run()
  mapservice.draw()
  mapservice.saveDwg()
```

**Check if point touch polygon **
```py
  region = mapservice.xyPoligons[0]["data"]
  cursor = (277, 366 ) # mapservice.mapCoorToXY( ( _lon, _lat ) )
  print mapservice.isPointInPolygon( cursor, region )
```
