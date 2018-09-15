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

from math import *
from graphviz import Digraph

#https://pythonhosted.org/svgwrite/
import svgwrite
from svglib.svglib import svg2rlg
from svglib.svglib import SvgRenderer
from reportlab.graphics import renderPM


# ---------------------------------------------------------------------- MAIN

if __name__ == '__main__':

    params = loader.parseArgs( sys.argv[1:] )

    inputs = loader.getInputs()

    inputFile =  inputs[0]["path"][ 0 ]
    df_madrid = filewriter.jsonToObj( inputFile )

    itemCursor = 0
    postalCode =  df_madrid["features"][ itemCursor ]["properties"]["COD_POSTAL"]
    formType =  df_madrid["features"][ itemCursor ]["geometry"]["type"] # Polygon
    geometryListPoints =  df_madrid["features"][ itemCursor ]["geometry"]["coordinates"][0]




    SVG_PATH1 = loader.getOutputPath( )["path"] + 'radar.svg'
    PNG_PATH1 = loader.getOutputPath( )["path"] + 'radar.png'

    imageWidth = 800
    imageHeight = 800
    imagePadding = 200
    limitSize = 200



    dwg = svgwrite.Drawing( SVG_PATH1 , profile='tiny', size = ( imageWidth , imageHeight ) )

    # CIRCLE = dwg.circle( [400, 400 ] , 50 , fill="none", stroke="#000")
    # dwg.add( CIRCLE )
    #dwg.add(dwg.text( itemText , insert= topPos , fill='black'))

    # shape = [[100,300],[300,300],[200,50]]

    def drawShape( pointsList ):

        def drawLine( M0, M1, L0, L1 ):
            pathStr = "M " + str( int( M0 ) ) + ',' + str( int( M1 ) ) + " "
            pathStr += "L "
            pathStr += str( int( L0 ) ) + ',' + str( int( L1 ) ) + " "
            #pathStr += "Z"
            return pathStr

        origin = pointsList[0]

        farbe = '#ffcc00'
        lenPoints = len( pointsList )
        for idx, coor in enumerate( pointsList ):
            if idx == lenPoints-1:
                next = pointsList[ 0 ]
            else:
                next = pointsList[ idx + 1 ]

            objPath = dwg.path( d =  drawLine( coor[0], coor[1], next[0], next[1] ),  stroke=farbe, stroke_width=3  )
            objPath.stroke(  opacity=0.4 )
            dwg.add( objPath )


    # def correction( coors ):
    #     lat = coors[1]
    #     lon = coors[0]
    #     x = ( 480 + lon ) * ( 600 / 360 )
    #     y = ( 90 - lat ) * ( 600 / 180 )
    #     return [ x, y]

    def rangeScale( point ):
        minA = 1
        maxA = 2
        minB = 100
        maxB = 500
        if minA < 0:
            maxA = maxA - minA
            point = point - minA
            if point == 0:
                return minB
        pos = maxA / point
        return ( ( maxB - minB ) / pos ) + minB

    # correctionPoints = [ correction(xs)  for xs in geometryListPoints]
    # scaledPoints = [[ rangeScale(s) for s in xs] for xs in correctionPoints]
    # #
    # print geometryListPoints
    # print correctionPoints
    # print scaledPoints

    correctionPoints = [ [1,1], [1,2], [2,2] , [2,1] ]
    scaledPoints = [[ rangeScale(s) for s in xs] for xs in correctionPoints]
    drawShape( scaledPoints )


    dwg.save()
    drawing = svg2rlg( SVG_PATH1 )
    renderPM.drawToFile( drawing , PNG_PATH1 )


    # loader.getOutputPath( )["path"]
    # loader.saveMetas();
