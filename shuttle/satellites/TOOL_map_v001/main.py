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

# ---------------------------------------------------------------------- CUSTOM LIBS

from MapService import *
from math import *

# from graphviz import Digraph
# #https://pythonhosted.org/svgwrite/
# import svgwrite
# from svglib.svglib import svg2rlg
# from svglib.svglib import SvgRenderer
# from reportlab.graphics import renderPM

# ---------------------------------------------------------------------- MAIN

if __name__ == '__main__':

    # params = loader.parseArgs( sys.argv[1:] )
    inputs = loader.getInputs()

    inputFile =  inputs[0]["path"][ 0 ]
    df_madrid = filewriter.jsonToObj( inputFile )


    # postalCode =  df_madrid["features"][ itemCursor ]["properties"]["COD_POSTAL"]
    # formType =  df_madrid["features"][ itemCursor ]["geometry"]["type"] # Polygon

    geometryListPoints = []

    # itemCursor = 150
    # regionData = {
    #     "coordinates": df_madrid["features"][ itemCursor ]["geometry"]["coordinates"][0],
    #     "properties": {
    #         "postalcode": df_madrid["features"][ itemCursor ]["properties"]["COD_POSTAL"]
    #     }
    # }
    # geometryListPoints.append( regionData )


    # limit = 150
    for idr, region in  enumerate( df_madrid["features"] ):
        # if idr == limit:
        #     break
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


    SVG_PATH = loader.getOutputPath( )["path"] + 'testIds.svg'
    PNG_PATH = loader.getOutputPath( )["path"] + 'testIds.png'

    MapService( SVG_PATH, PNG_PATH, 800, 800, geometryListPoints )
