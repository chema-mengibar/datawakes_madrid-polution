from math import *
from decimal import Decimal

# https://pypi.org/project/svgwrite/
# https://svgwrite.readthedocs.io/en/master/
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
        # Params
        self.MINIMUM_IMAGE_PADDING_IN_PX = 50
        self.IMAGE_HEIGHT_IN_PX = IMAGE_HEIGHT_IN_PX
        self.IMAGE_WIDTH_IN_PX = IMAGE_WIDTH_IN_PX
        self.IMAGE_FILE_PATH = IMAGE_FILE_PATH
        self.IMAGE_FILE_PATH_PNG = IMAGE_FILE_PATH_PNG
        # Definition
        self.globalRatio = 0;
        self.heightPadding = 0;
        self.widthPadding = 0;
        self.minXY = Vector( -1, -1 );
        self.maxXY = Vector( -1, -1 );
        self.countyBoundaries = []
        self.xyPoligons = []
        self.IDS = []
        self.CLASSES = []
        self.QUARTERPI = pi / 4.0
        # Init steps
        self.dwg = svgwrite.Drawing( IMAGE_FILE_PATH , profile='tiny', size = ( IMAGE_WIDTH_IN_PX , IMAGE_HEIGHT_IN_PX ) )
        self.step_processCoordinates( GEOMETRIES )
        self.step_calculateMax()
        self.step_calculateSizes()
        self.step_drawPoints()

    # ----------------------------------------------------------------------------------------------------------- GETTERS
    def getDwg( self ):
        return self.dwg

    # ----------------------------------------------------------------------------------------------------------- STEPS
    def step_processCoordinates( self, _GEOMETRIES ):
        for idg, ZONE_BOUNDARIES in enumerate( _GEOMETRIES ):

            lonLat = []
            print 'Geometries '+ str( idg )

            coordinates = ZONE_BOUNDARIES["coordinates"]
            self.IDS.append( ZONE_BOUNDARIES["properties"]["postalcode"] )

            className = "region__" + ZONE_BOUNDARIES["properties"]["region"] + "--" + str( idg )
            self.CLASSES.append( className )

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

            # -----------------------------------------------------------------------------------  Start Calculate Map
            for idc, countyBoundary in enumerate( ZONE_BOUNDARIES_REDUCED ):
                xy = self.mapCoorToVector( countyBoundary )
                self.minXY.x = xy.x if ( self.minXY.x == -1) else min( self.minXY.x, xy.x)
                self.minXY.y = xy.y if ( self.minXY.y == -1) else min( self.minXY.y, xy.y)
                lonLat.append( xy );
            self.countyBoundaries.append(lonLat);


    def step_calculateMax( self ):
        for lonLatList in self.countyBoundaries:
            for point in lonLatList:
                point.x = point.x - self.minXY.x;
                point.y = point.y - self.minXY.y;
                self.maxXY.x = point.x if ( self.maxXY.x == -1) else max( self.maxXY.x, point.x);
                self.maxXY.y = point.y if ( self.maxXY.y == -1) else max( self.maxXY.y, point.y);


    def step_calculateSizes( self ):
        paddingBothSides = self.MINIMUM_IMAGE_PADDING_IN_PX * 2;
        mapWidth = self.IMAGE_WIDTH_IN_PX - paddingBothSides;
        mapHeight = self.IMAGE_HEIGHT_IN_PX - paddingBothSides;
        mapWidthRatio = mapWidth / self.maxXY.x;
        mapHeightRatio = mapHeight / self.maxXY.y;
        self.globalRatio = min( mapWidthRatio, mapHeightRatio );
        self.heightPadding = (self.IMAGE_HEIGHT_IN_PX - ( self.globalRatio * self.maxXY.y)) / 2;
        self.widthPadding = (self.IMAGE_WIDTH_IN_PX - ( self.globalRatio * self.maxXY.x)) / 2;


    def step_drawPoints( self ):
        #DOCU: https://svgwrite.readthedocs.io/en/latest/classes/base.html
        for idl, lonLatList in enumerate( self.countyBoundaries ):
            polygonPoints = []
            polygonConfig = {
                "id":"region_" + str( self.IDS[ idl ] ),
                "class": self.CLASSES[ idl ]
            }
            for point in lonLatList:
                polygonPoints.append( self.mapPointToXY( point ) ) # [ adjustedX, adjustedY ]

            self.xyPoligons.append( polygonPoints )
            shape = self.drawShape( polygonPoints, polygonConfig )
            self.dwg.add( shape )


    # ----------------------------------------------------------------------------------------------------------- POSITION TOOLS

    def mapCoorToVector( self, tuppleCoors ):
        longitude = tuppleCoors[0] * pi / 180;
        latitude = tuppleCoors[1] * pi / 180;
        pointerXY = Vector( 0, 0 )
        pointerXY.x = longitude;
        pointerXY.y = log( tan( self.QUARTERPI + 0.5 * latitude) );
        return pointerXY


    def mapCoorToXY( self, tuppleCoors ):
        _vector = self.mapCoorToVector( tuppleCoors )
        _vector.x = _vector.x - self.minXY.x;
        _vector.y = _vector.y - self.minXY.y;
        _xy = self.mapPointToXY( _vector )
        return _xy


    def mapPointToXY( self, point ):
        adjustedX = int( self.widthPadding + (point.x * self.globalRatio) )
        adjustedY = int( self.IMAGE_HEIGHT_IN_PX - self.heightPadding - (point.y * self.globalRatio));
        return [ adjustedX, adjustedY ]

    def findCenter( self, listPoints ):
        return []

    # ----------------------------------------------------------------------------------------------------------- SVG TOOLS

    def drawShape( self, pointsList, polygonConfig ):
        print ' Drawing shape'
        pathStr = "M " + str( int( pointsList[0][0] ) ) + ',' + str( int( pointsList[0][1] ) ) + " "
        for idx, coor in enumerate( pointsList ):
            if idx == 0:
                continue
            pathStr += "L "
            pathStr += str( int( coor[0] ) ) + ',' + str( int( coor[1] ) ) + " "
        pathStr += "Z"
        objPath = self.dwg.path( d = pathStr, fill='#ffffff', stroke= '#000000', stroke_width=1, id= polygonConfig["id"], class_= polygonConfig["class"] )
        #objPath.stroke(  opacity=0.4 )
        return objPath


    def saveDwg( self ):
        self.dwg.save()
        # drawing = svg2rlg( self.IMAGE_FILE_PATH )
        # renderPM.drawToFile( drawing , self.IMAGE_FILE_PATH_PNG )
