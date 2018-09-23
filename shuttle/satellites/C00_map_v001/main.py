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

#_______________________________________________________________________________ dataweaks libs

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

#_______________________________________________________________________________ current-script libs

from MapService import *
from math import *
from sklearn import preprocessing

# from graphviz import Digraph
# #https://pythonhosted.org/svgwrite/
# import svgwrite
# from svglib.svglib import svg2rlg
# from svglib.svglib import SvgRenderer
# from reportlab.graphics import renderPM

#_______________________________________________________________________________ main

if __name__ == '__main__':

    # params = loader.parseArgs( sys.argv[1:] )

    #COM: Load input-files
    inputs = loader.getInputs()

    inputFile =  inputs[0]["path"][ 0 ]
    df_madrid = filewriter.jsonToObj( inputFile )

    stationsFile =  inputs[1]["path"][ 0 ]
    df_stations = filewriter.csvToDF( stationsFile )

    yearFile =  inputs[2]["path"][ 17 ]
    df_year2018 = filewriter.csvToDF( yearFile )

    # .......................................................................... block: Load and map geometries and metadata from geo-data

    geometryListPoints = []
    # limit = 1
    # exact = 47
    for idr, region in  enumerate( df_madrid["features"] ):
        # if idr == limit:
        #     break
        # if idr != exact:
        #     continue
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

    # .......................................................................... block: Translate coordinates to pixels

    SVG_PATH = loader.getOutputPath( )["path"] + 'all.svg'
    PNG_PATH = loader.getOutputPath( )["path"] + 'all.png'
    mapservice = MapService( SVG_PATH, PNG_PATH, 800, 800, geometryListPoints )
    mapservice.run()

    #Get colors pallete
    _colors = mapservice.getColors()

    # .......................................................................... block: Locate sensor values

    #com: Get a column with normalized values
    CO_min =  df_year2018['CO'].min()
    CO_max =  df_year2018['CO'].max()
    CO_norm = (df_year2018['CO'] - CO_min) / ( CO_max - CO_min)
    df_year2018['CO_norm'] = CO_norm

    #com: Get normalized min,max to change the domain-range of values for the map
    CO_norm_min =  df_year2018['CO_norm'].min()
    CO_norm_max =  df_year2018['CO_norm'].max()

    ranged_min = 0
    ranged_max = 200

    #com: to collect data from one stations
    def getStationData( _stationId, _datum ):
        #com: Select sensor data row
        #rowSensor = df_year2018.loc[ (df_year2018['date'] == _datum ) & (df_year2018['station'] == _stationId), ['CO', 'CO_norm', 'station'] ]
        #rowSensor_coNorm = rowSensor.iloc[0]['CO_norm']

        rowSensor = df_year2018.loc[ (df_year2018['station'] == _stationId), ['CO', 'CO_norm', 'station'] ]
        rowSensor_coNorm = rowSensor['CO_norm'].mean()

        #com: Convert the norm value for the map representation
        #com@opacity: the new range defines the opacity
        normMeditionRanged =  round( helper.domainRange( (CO_norm_min, CO_norm_max), (0,200), rowSensor_coNorm ) , 2)
        if( isnan( normMeditionRanged ) ) :
            normMeditionRanged = 0
        #com: Get the station coordinates
        rowStation = df_stations.loc[ df_stations['id'] == _stationId ]
        stationLon = rowStation.iloc[0]['lon']
        stationLat = rowStation.iloc[0]['lat']
        #help: print( _stationId, 'report: ', CO_min, CO_max, rowSensor_coNorm, normMeditionRanged )
        return { "id": _stationId, "lon": stationLon, "lat": stationLat, "data": normMeditionRanged }


    #com: collect data from all stations
    stationData_collection = []
    for idx, station in df_stations.iterrows():
        stationData = getStationData( station["id"], '2018-03-01 01:00:00' )
        if( stationData["data"] is not None  ):
            stationData_collection.append( stationData )

    # .......................................................................... block: Locate station in map

    #com: Create svg
    mapservice.draw()
    _dwg = mapservice.getDwg()

    #com: draw data from all stations, adding forms for each station
    for idx, station in enumerate( stationData_collection ):
        stationXY = mapservice.mapCoorToXY( [ station["lon"], station["lat"] ]  )
        #help: print station["data"]
        #com: look at #com@opacity

        sep = float( ranged_max/3 )
        if (station["data"] == 0):
            colorValue = _colors.white
        elif( station["data"] >= 1 and station["data"] < sep ):
            colorValue = _colors.contrast.blue
        elif( station["data"] >= sep and  station["data"] < sep*2 ):
            colorValue = _colors.contrast.orange
        elif( station["data"] >= sep*2 and  station["data"] < 200 ):
            colorValue = _colors.contrast.rosa
        CIRCLE = _dwg.circle(center= stationXY , r='5', fill= colorValue , stroke="none", opacity='0.8' )
        _dwg.add( CIRCLE )

    # .......................................................................... block: Labels
    #https://stackoverflow.com/questions/17127083/python-svgwrite-and-font-styles-sizes
    _dwg.add(_dwg.rect( (10,10), (7,50), fill= _colors.contrast.rosa ))
    #_dwg.add(_dwg.text( str(200), insert= (20, 20), fill= _colors.white,font_size="10px" ))

    _dwg.add(_dwg.rect( (10,60), (7,50), fill= _colors.contrast.orange ))
    #_dwg.add(_dwg.text( str(sep*2), insert= (20, 60), fill= _colors.white,font_size="10px" ))
    #_dwg.add(_dwg.text( str(sep), insert= (20, 110), fill= _colors.white, font_size="10px" ))

    _dwg.add(_dwg.rect( (10,110), (7,50), fill= _colors.contrast.blue ))
    # _dwg.add(_dwg.text( str(1), insert= (20, 160), fill= _colors.white, font_size="10px" ))

    _dwg.add(_dwg.rect( (10,160), (7,10), fill= _colors.white))
    #_dwg.add(_dwg.text( str(0), insert= (20, 170), fill= _colors.white, font_size="10px" ))



    # .......................................................................... block: Save
    #com: save svg file
    mapservice.saveDwg()
