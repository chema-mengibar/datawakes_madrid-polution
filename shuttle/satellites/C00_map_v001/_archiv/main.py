import sys
import os
from os import listdir
from os.path import isfile, join

currentFullRoute = os.path.abspath(os.path.join(os.path.dirname(__file__),"./"))
currentDir = os.path.basename(os.getcwd())
currentFileName = os.path.basename(__file__)

libDir = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append( libDir )
print libDir

from lib.router import Router
router = Router( )
ROUTES =  router.getRoutes()

from lib.loader import Loader
loader = Loader( currentFullRoute, ROUTES  )

from lib.helper import Helper
helper = Helper( )

from lib.filewriter import FileWriter
filewriter = FileWriter( )

from lib.reporter import Reporter
reporter = Reporter(  ROUTES  )

# return to current path

sys.path.append( currentFullRoute )

#_______________________________________________________________________________ CUSTOM LIBS

from MapService import *
from math import *

# from graphviz import Digraph
# #https://pythonhosted.org/svgwrite/
# import svgwrite
# from svglib.svglib import svg2rlg
# from svglib.svglib import SvgRenderer
# from reportlab.graphics import renderPM

#_______________________________________________________________________________ MAIN

if __name__ == '__main__':

    # params = loader.parseArgs( sys.argv[1:] )
    inputs = loader.getInputs()

    inputFile =  inputs[0]["path"][ 0 ]
    df_madrid = filewriter.jsonToObj( inputFile )

    geometryListPoints = []
    for idr, region in  enumerate( df_madrid["features"] ):
        if region["geometry"]["type"] == 'MultiPolygon':
            for pol in  region["geometry"]["coordinates"][0]:
                regionData = {
                    "coordinates": pol,
                    "properties": {
                        "postalcode": region["properties"]["COD_POSTAL"],
                        "region":"madrid"
                    }
                }
                geometryListPoints.append( regionData )
        else:
            regionData = {
                "coordinates": region["geometry"]["coordinates"][0],
                "properties": {
                    "postalcode": region["properties"]["COD_POSTAL"],
                    "region":"madrid"
                }
            }
            geometryListPoints.append( regionData )

    #___________________________________________________________________________

    SVG_PATH = loader.getOutputPath( )["path"] + 'separate.svg'
    PNG_PATH = loader.getOutputPath( )["path"] + 'separate.png'
    mapservice = MapService( SVG_PATH, PNG_PATH, 800, 800, geometryListPoints )
    # mapservice.run()

    stationsFile =  inputs[1]["path"][ 0 ]
    df_stations = filewriter.csvToDF( stationsFile )
    idStation = 15
    _lon =  df_stations["lon"][ idStation ]
    _lat =  df_stations["lat"][ idStation ]


    xyStacion = ( 1,1 ) # mapservice.mapCoorToXY( ( _lon, _lat ) )

    print mapservice.isPointInPolygon( xyStacion, [( 450,450 ),( 460, 450 ),( 470 ,450   )]   )
    # print mapservice.getPostalcodeByCoors( xyStacion)


    # _dwg = mapservice.getDwg()


    # # from coordinates to xy
    # _xy = mapservice.mapCoorToXY( [ _lon, _lat ]  )
    # CIRCLE = _dwg.circle(center= _xy , r=20, fill="#ffcc00", stroke="none", opacity=0.7 )
    # _dwg.add( CIRCLE )
    #
    # print mapservice.xyPoligons[1]
    # # print mapservice.countyBoundaries[0][0].x
    #
    # polygon = mapservice.xyPoligons[1]
    # tab = [3.5, 1.5 ]
    # print mapservice.isPointInPolygon( tab, polygon  )
    #
    #
    # mapservice.saveDwg()
