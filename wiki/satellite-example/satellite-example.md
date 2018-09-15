# Script example

>**Version**: 1.0.0




> **Description:**

#### Table of Contents
1. [Basic script blocks](#basic-script-blocks)
    1.1. [Header-script](#header-script)
    1.2. [Custom libs](#custom-libs)
    1.3. [Init block](#init-block)

2. [Notes](#notes)
    2.1 [Comand arguments](#comand-arguments)

3. [Notes](#examples)
    3.1 [Simple File Access](#simple-file-access)
    3.2 [Mongo Save](#mongo-save)

---
##Basic script blocks

###Header-script
````python
 # --------------------------------------------------- COMMON LIBS 
import sys
import os
from os import listdir
from os.path import isfile, join

currentFullRoute = os.path.abspath(os.path.join(os.path.dirname(__file__),"./"))
currentDir = os.path.basename(os.getcwd()) 
currentFileName = os.path.basename(__file__)

libDir = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
sys.path.append( libDir )

from lib.router import Router
router = Router( )
ROUTES =  router.getRoutes()

from lib.reloader import Reloader
reloader = Reloader( currentFullRoute, ROUTES  )

from lib.helper_01 import Helper
helper = Helper( )

from lib.exporter import Exporter
exporter = Exporter( )

 # Optional module 1
from lib.social import Social
social = Social( )

 # Optional module 2
from lib.reporter import Reporter
reporter = Reporter(  ROUTES  )

#......................
sys.path.append( currentFullRoute )
#os.chdir( os.path.dirname(__file__) )
 
````


###Custom libs
```` py
# --------------------------------------------------- CUSTOM LIBS
import json
import pymongo
from pymongo import MongoClient
````


###Init block
With argument-parser ( optional )
```` py
if __name__ == '__main__':

    params = loader.parseArgs( sys.argv[1:] )

    print 'init'

````

---

##Notes

###Comand-arguments
Return an object with the arguments keys=value, with required validation
```` py
params = reloader.parseArgs( sys.argv[1:] )
````

---

##Examples

###Simple File access

```` py
if __name__ == '__main__':

    #Get the script inputs paths
    inputs = reloader.getInputs()

    #Load the files content in dataframes
    myDF0 = exporter.csvToDF( inputs[0]["path"][0] )
    myDF1 = exporter.csvToDF( inputs[0]["path"][1] )

    #Do something with the data

    #Get the full output-path with suffix, and save the file
    outputParams =  reloader.getOutputPath( "test-suffix" )

    if not reloader.isMongoTarget(): #optional check
        'register output-file-reference in output-metadata
        reloader.addMetaOutputDoc( outputParams["file_name"] )

        exporter.dfToCsv( myDF1 , outputParams["path"] )

    reloader.saveMetas() 

````

###Mongo Save

```` py
if __name__ == '__main__':

    client = MongoClient( ROUTES["mongo_host"], ROUTES["mongo_port"] )


    # Get inputs data and do something with the data
    inputs = reloader.getInputs()
    myDF0 = exporter.csvToDF( inputs[0]["path"][0] )


    # Get the full output-path with suffix
    # If mongo is the output target, it will be usec the db and collection reference.
    # The gived suffix will be the doc name
    outputParams =  reloader.getOutputPath( "test-suffix" )
    
    # Check if output-target is MongoDB before save doc
    if reloader.isMongoTarget():

        db = client[ outputParams["db"] ]

        DFJson = exporter.dfToJsonObj( myDF0 )

        collection = db[ outputParams["collection"] ]
        insertId = collection.insert( DFJson )
        reloader.addMetaOutputDoc( insertId )

    reloader.saveMetas()

````
