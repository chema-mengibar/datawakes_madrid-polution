from math import *
from decimal import Decimal

from shapely.geometry import Point, Polygon

# https://pypi.org/project/svgwrite/
# https://svgwrite.readthedocs.io/en/master/
import svgwrite
from svglib.svglib import svg2rlg
from svglib.svglib import SvgRenderer
from reportlab.graphics import renderPM

#https://github.com/fitnr/visvalingamwyatt
import visvalingamwyatt as vw

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Vector( ):
    def __init__( self, _x, _y ):
        self.x = _x
        self.y = _y

class MapService( ):

    def __init__( self, IMAGE_FILE_PATH, IMAGE_FILE_PATH_PNG , IMAGE_WIDTH_IN_PX, IMAGE_HEIGHT_IN_PX, ZONES ):
        # Globals
        self.ZONES = ZONES
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

        self.colors = {
            "background": 'rgb(8,18,41)',
            "basic": 'rgb(39,52,79)',
            "white": 'rgb(255,255,255)',
            "contrast":{
                "rosa":'rgb(255,4,189)',
                "blue":'rgb(47,255,199)',
                "orange":'rgb(255,76,22)',
                "green":'rgb(26, 204, 44)'
            },
            "gradation":[
                'rgb(255, 200, 107)',
                'rgb(255, 187, 73)',
                'rgb(252, 175, 45)',
                'rgb(211, 132, 0)'
            ]
        }


    def run( self ):
        self.step_processCoordinates( self.ZONES )
        self.step_calculateMax()
        self.step_calculateSizes()
        self.step_calculateXyPoligons()

    def draw( self ):
        self.dwg = svgwrite.Drawing( self.IMAGE_FILE_PATH , profile='tiny', size = ( self.IMAGE_WIDTH_IN_PX , self.IMAGE_HEIGHT_IN_PX ) )
        self.dwg.add( self.dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill= self.colors["background"] ))

        for idl, xyPoligon in enumerate( self.xyPoligons ):
            shape = self.drawShape( xyPoligon["data"], xyPoligon["config"] )
            self.dwg.add( shape )

    # ----------------------------------------------------------------------------------------------------------- GETTERS
    def getDwg( self ):
        return self.dwg

    def getColors( self ):
        #@todo: do this recursive
        colors = Struct(**self.colors)
        colors.contrast = Struct( **self.colors['contrast'] )
        #colors.gradation = Struct( **self.colors['gradation'] )
        return colors

    # ----------------------------------------------------------------------------------------------------------- STEPS
    def step_processCoordinates( self, _ZONES ):
        print( 'Processing coordinates...' )
        for idg, ZONE_BOUNDARIES in enumerate( _ZONES ):

            lonLat = []
            coordinates = ZONE_BOUNDARIES["coordinates"]
            self.IDS.append( ZONE_BOUNDARIES["properties"]["postalcode"] )

            className = "region__" + ZONE_BOUNDARIES["properties"]["region"] + "--" + str( idg )
            self.CLASSES.append( className )

            ##------------------------------------------------------------------ Reduce Method 2
            #print len( coordinates )
            if len( coordinates ) <= 70:
                _ratio =  0.25

            elif len( coordinates ) > 70 and len( coordinates ) < 150:
                _ratio =  0.15

            elif len( coordinates ) >= 150 and len( coordinates ) < 500:
                _ratio =  0.05

            elif len( coordinates ) >= 500 and len( coordinates ) < 1000:
                _ratio =  round( Decimal( float( len( coordinates ) / 2 ) / float( 10000 ) ) , 4 )

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
        print( 'Processing coordinates ready' )


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


    def step_calculateXyPoligons( self ):
        #DOCU: https://svgwrite.readthedocs.io/en/latest/classes/base.html
        for idl, lonLatList in enumerate( self.countyBoundaries ):
            polygon = {
                "meta":{
                    "postalcode": self.ZONES[ idl ]["properties"]["postalcode"]
                },
                "config":{
                    "id":"region_" + str( self.IDS[ idl ] ),
                    "class": self.CLASSES[ idl ],
                },
                "data": []
            }
            for point in lonLatList:
                xyList = self.mapPointToXY( point ) # [ adjustedX, adjustedY ]
                polygon["data"].append( xyList )

            self.xyPoligons.append( polygon )



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
        objPath = self.dwg.path( d = pathStr, fill= self.colors["basic"] , stroke= self.colors["background"], stroke_width=1, id= polygonConfig["id"], class_= polygonConfig["class"] )
        #objPath.stroke(  opacity=0.4 )
        return objPath


    def saveDwg( self ):
        self.dwg.save()
        # drawing = svg2rlg( selfIMAGE_FILE_PATH )
        # renderPM.drawToFile( drawing , self.IMAGE_FILE_PATH_PNG )

    # -------------------------------------------------------------------------------------------------------------- EXTENSION:TOUCH

    def isPointInPolygon( self, tap, polygon):
        _polygon = Polygon( polygon )
        # linearring = LinearRing(list(polygon.exterior.coords))
        point = Point( tap[0], tap[1])
        return _polygon.contains(point)


    def getPostalcodeByCoors( self, pointer ):
        for idr, region in enumerate( self.xyPoligons ):
            if len( region["data"]) > 2:
                if self.isPointInPolygon( pointer, region["data"] ):
                    return idr
        return -1
