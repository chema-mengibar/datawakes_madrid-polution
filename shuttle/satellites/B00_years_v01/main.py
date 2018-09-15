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



# ---------------------------------------------------------------------- MAIN

if __name__ == '__main__':

    params = loader.parseArgs( sys.argv[1:] )

    inputs = loader.getInputs()

    # inputFile =  inputs[0]["path"][ 17 ]
    # df_2001 = filewriter.csvToDF( inputFile )
    # print df_2001

    inputFileStations =  inputs[1]["path"][ 0 ]
    df_stations = filewriter.csvToDF( _inputFullPathFile=inputFileStations  )
    print df_stations

    # loader.getOutputPath( )["path"]
    # loader.saveMetas();
