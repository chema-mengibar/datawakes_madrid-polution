from math import *
from decimal import Decimal
from graphviz import Digraph
#https://pythonhosted.org/svgwrite/
import svgwrite
from svglib.svglib import svg2rlg
from svglib.svglib import SvgRenderer
from reportlab.graphics import renderPM

#https://github.com/fitnr/visvalingamwyatt
import visvalingamwyatt as vw

class Vector( ):
    def __init__( self, _x, _y ):
        self.x = _x
        self.y = _y

class MapService( ):

    def __init__( self, IMAGE_FILE_PATH, IMAGE_FILE_PATH_PNG , IMAGE_WIDTH_IN_PX, IMAGE_HEIGHT_IN_PX, GEOMETRIES ):

        MINIMUM_IMAGE_PADDING_IN_PX = 50
        QUARTERPI = pi / 4.0

        dwg = svgwrite.Drawing( IMAGE_FILE_PATH , profile='tiny', size = ( IMAGE_WIDTH_IN_PX , IMAGE_HEIGHT_IN_PX ) )

        minXY = Vector( -1, -1 );
        maxXY = Vector( -1, -1 );

        countyBoundaries = []
        IDS = []
        CLASSES = []

        for idg, ZONE_BOUNDARIES in enumerate( GEOMETRIES ):

            lonLat = []
            print 'Geometries '+ str( idg )

            coordinates = ZONE_BOUNDARIES["coordinates"]
            IDS.append( ZONE_BOUNDARIES["properties"]["postalcode"] )

            className = "region__" + ZONE_BOUNDARIES["properties"]["region"] + "--" + str( idg )
            CLASSES.append( className )

            ##------------------------------------------------------------------ Reduce Method 1
            # numPoints = len( ZONE_BOUNDARIES )
            # if numPoints <= 20:
            #     jump = 1
            # elif  numPoints > 20 and numPoints <= 50:
            #     jump = 4
            # elif  numPoints > 50 and numPoints <= 100:
            #     jump = 8
            # elif  numPoints > 100 and numPoints <= 250:
            #     jump = 12
            # elif  numPoints > 250 and numPoints <= 500:
            #     jump = 20
            # elif  numPoints > 500 and numPoints <= 750:
            #     jump = 75
            # elif  numPoints > 750 and numPoints <= 1200:
            #     jump = 90
            # else:
            #     jump = 110
            #ZONE_BOUNDARIES_REDUCED = [ ZONE_BOUNDARIES[e] for e in range( 0, numPoints, jump )]
            # print( numPoints, jump, len( ZONE_BOUNDARIES_REDUCED ) )

            ##------------------------------------------------------------------ Reduce Method 2
            if len( coordinates ) < 50:
                _ratio =  0.15

            elif len( coordinates ) >= 50 and len( coordinates ) < 200:
                _ratio =  0.05

            elif len( coordinates ) >= 200 and len( coordinates ) < 1000:
                _ratio =  round( Decimal( float( len( coordinates ) / 2 ) / float( 10000 ) ) , 4 ) # (714, 0.0714, 51) -> (714, 0.014, x)

            else:
                _ratio =  round( Decimal( float( len( coordinates ) ) / float( 100000 ) ) , 4 )

            ZONE_BOUNDARIES_REDUCED = vw.simplify( coordinates, ratio= _ratio ) # 0.10
            print( len( coordinates ), _ratio, len( ZONE_BOUNDARIES_REDUCED ) )


            # -----------------------------------------------------------------------------------  Start Calculate Map
            for idc, countyBoundary in enumerate( ZONE_BOUNDARIES_REDUCED ):

                longitude = countyBoundary[0] * pi / 180;
                latitude = countyBoundary[1] * pi / 180;

                xy = Vector( 0, 0 )
                xy.x = longitude;
                xy.y = log( tan(QUARTERPI + 0.5 * latitude) );

                minXY.x = xy.x if (minXY.x == -1) else min(minXY.x, xy.x)
                minXY.y = xy.y if (minXY.y == -1) else min(minXY.y, xy.y)

                lonLat.append( xy );

            countyBoundaries.append(lonLat);

        for lonLatList in countyBoundaries:
            for point in lonLatList:
                point.x = point.x - minXY.x;
                point.y = point.y - minXY.y;

                maxXY.x = point.x if (maxXY.x == -1) else max( maxXY.x, point.x);
                maxXY.y = point.y if (maxXY.y == -1) else max( maxXY.y, point.y);


        paddingBothSides = MINIMUM_IMAGE_PADDING_IN_PX * 2;

        mapWidth = IMAGE_WIDTH_IN_PX - paddingBothSides;
        mapHeight = IMAGE_HEIGHT_IN_PX - paddingBothSides;

        mapWidthRatio = mapWidth / maxXY.x;
        mapHeightRatio = mapHeight / maxXY.y;

        globalRatio = min(mapWidthRatio, mapHeightRatio);
        heightPadding = (IMAGE_HEIGHT_IN_PX - (globalRatio * maxXY.y)) / 2;
        widthPadding = (IMAGE_WIDTH_IN_PX - (globalRatio * maxXY.x)) / 2;

        def drawShape( pointsList, polygonConfig ):
            print ' Drawing shape'
            pathStr = "M " + str( int( pointsList[0][0] ) ) + ',' + str( int( pointsList[0][1] ) ) + " "
            for idx, coor in enumerate( pointsList ):
                if idx == 0:
                    continue
                pathStr += "L "
                pathStr += str( int( coor[0] ) ) + ',' + str( int( coor[1] ) ) + " "
            pathStr += "Z"

            objPath = dwg.path( d = pathStr, fill='#ffffff', stroke= '#000000', stroke_width=1, id= polygonConfig["id"], class_= polygonConfig["class"] )
            #objPath.stroke(  opacity=0.4 )
            return objPath

        #DOCU: https://svgwrite.readthedocs.io/en/latest/classes/base.html
        for idl, lonLatList in enumerate( countyBoundaries ):
            polygonPoints = []
            polygonConfig = {
                "id":"region_" + str( IDS[ idl ] ),
                "class": CLASSES[ idl ]
            }
            for point in lonLatList:
                adjustedX = int( widthPadding + (point.x * globalRatio) )
                adjustedY = int(IMAGE_HEIGHT_IN_PX - heightPadding - (point.y * globalRatio));
                polygonPoints.append( [ adjustedX, adjustedY ] )
            shape = drawShape( polygonPoints, polygonConfig )
            dwg.add( shape )

        dwg.save()
        # drawing = svg2rlg( IMAGE_FILE_PATH )
        # renderPM.drawToFile( drawing , IMAGE_FILE_PATH_PNG )
