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
exporter = FileWriter( )

 # Optional module 1
# from lib.social import Social
# social = Social( )

from lib.reporter import Reporter
reporter = Reporter(  ROUTES  )

#Extend the Reporter with the desired Report-Class
# from lib.reporters.MultiLayerTimeSerie import MultiLayerTimeSerie
# multilayer = MultiLayerTimeSerie()
# reporter.builder = multilayer.builder

#......................
sys.path.append( currentFullRoute )

# --------------------------------------------------- CUSTOM LIBS

import zipfile

# ---------------------------------------------------------------------- MAIN

if __name__ == '__main__':

    params = loader.parseArgs( sys.argv[1:] )

    inputs = loader.getInputs()
    inputFile =  inputs[0]["path"][0]

    zip_ref = zipfile.ZipFile( inputFile, 'r')

    zip_ref.extractall( loader.getOutputPath( )["path"] )
    zip_ref.close()

    loader.saveMetas();
