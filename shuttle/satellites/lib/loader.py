#!/usr/local/bin/python
import sys
import os
import json
import urllib2, base64
import simplejson
import datetime as dtm
import pandas as pd
import copy
from pandas.compat import StringIO
from os import listdir
from os.path import isfile, join


class Loader( object ):

    def __init__(self, CURRENT_DIR, ROUTES ):
        self.dir_path = os.path.dirname( os.path.realpath( __file__ ) )
        self.dir_root =  ROUTES["root"]
        self.routes = {
            "master": ROUTES["master"],
            "processed": ROUTES["processed"],
            "stage": ROUTES["stage"],
            "reports": ROUTES["reports"]
        }
        self.params = {}
        self.metaScript = self.loadMeta( CURRENT_DIR )
        self.metaScriptOutput = self.metaScript["output"]
        outputDomain = self.metaScriptOutput["domain"]
        self.scriptName = self.getMetaInfo( "name" )
        self.fullOutputPath =  self.routes[ outputDomain ] + self.scriptName +  '\\'
        if outputDomain == 'reports':
            p_data_source = "mongo"
        else:
            p_data_source = self.metaScriptOutput["data_source"]
        self.metaData = {
            "date_creation": self.today(),
            "script_name": self.scriptName,
            "inputs": self.metaScript["inputs"],
            "output": {
                "data_source": p_data_source,
                "domain": outputDomain,
                "collection":"",
                "docs":[ ]
            },
            "extras":{},
            "params":{}
        }

    #---------------------------------------------------------------------- META-DATA

    def loadMeta( self, pCurrentDir ):
        modelFileReference= 'metascript.json'
        rawJsonModel = open(os.path.join( pCurrentDir, modelFileReference ), 'r')
        return json.load( rawJsonModel )


    def setMetaColumns( self, prop="", val="" ):
        if( prop in self.metaData ):
            self.metaData[ prop ] = val;
        else:
            self.metaData[ "extras" ][prop] = val


    def setMetaProp( self, prop="", val="" ):
        if( prop in self.metaData ):
            self.metaData[ prop ] = val;
        else:
            self.metaData[ "extras" ][prop] = val


    def setMetaReporterInfo( self, prop, val ):
        self.metaData[ "extras" ][prop] = val


    def saveMetas( self ):
        with open( self.fullOutputPath + 'metadata.json', 'w' ) as outfile:
            json.dump( self.metaData , outfile , indent=2, sort_keys=True )
        return self.metaData


    def getMetaInfo( self, prop ):
        return self.metaScript["info"][ prop ]


    def getMetadata( self ):
        return self.metaData


    def isMongoTarget( self ):
        if self.metaScript["output"][ "data_source" ] == "dir":
            return False
        else:
            return True


    def addMetaOutputDoc( self , docName ):
        self.metaData["output"]["docs"].append( str( docName ) )


    def setMetaOutputCollection( self , collectionName ):
        self.metaData["output"]["collection"] = collectionName


    #---------------------------------------------------------------------- UTILS

    def today(self, str_format = '%Y.%m.%d' , dif=0):
        #http://strftime.org/
        today = dtm.datetime.today() - dtm.timedelta( ( int(dif)*-1) )
        DATE_TODAY = dtm.datetime.strftime(today, str_format)
        return DATE_TODAY


    def createOutputDir(self, DIR  ):
        if not os.path.exists( DIR ):
            print 'folder created'
            os.makedirs( DIR )
        else:
            print "folder exist"


    def getInputs( self ):
        nInputs = []
        msInputs = copy.deepcopy( self.metaScript["inputs"])
        for input in msInputs:
            if input["data_source"] == "dir":
                paths = []
                for file in input["docs"]:
                    domain = input["domain"]
                    collection = input["collection"].replace("/", "") + "\\"
                    fullFileRoute = self.routes[ domain ] + collection + file
                    paths.append( fullFileRoute.replace("/", "\\") )
                input["path"] = paths
                nInputs.append( input )
            else:
                nInputs.append( input )
        return nInputs


    def getOutputPath( self, addon = "" ):
        metaOutput = self.metaScriptOutput
        domain = metaOutput["domain"]
        fullOutputPath =  self.fullOutputPath
        self.createOutputDir( fullOutputPath )
        addPathData = ""
        if(  addon != "" ):
            addPathData +=  '_' + addon.replace(" ", "_")
        if metaOutput["data_source"] == "dir": #and domain != "reports": #???
            self.setMetaOutputCollection( self.scriptName )
            return {
                "type":"dir",
                "path" : fullOutputPath ,
                "file_name": addPathData
            }
        else:
            if metaOutput["collection"] != "":
                collectionTarget = metaOutput["collection"]
            else:
                collectionTarget = addPathData

            self.setMetaOutputCollection( collectionTarget )
            return {
                "type":"mongo",
                "db":metaOutput["domain"],
                "collection": collectionTarget
            }


    def parseArgs( self, args ):
        params = { }
        metadataParams =  self.metaScript["params"]
        numRequiredParams = 0;
        numIntroducedRequiredParams = 0
        for paramKey, paramAttrs in metadataParams.iteritems():
            if paramAttrs["required"]:
                numRequiredParams +=1
        for arg in args:
            param = arg.split("=")
            argKey = param[0]
            if metadataParams[argKey]["type"] == "integer":
                argValue = int(param[1])
            elif metadataParams[argKey]["type"] == "float":
                argValue = float(param[1])
            else:
                argValue = param[1]
            params[ argKey ]= argValue
            # Check in arg is required
            if argKey in metadataParams:
                if metadataParams[ argKey ]["required"]:
                    numIntroducedRequiredParams += 1
                # To output metada add params with gived value
                metadataParams[ argKey ]["value"] = argValue
            else:
                print ">> ignored argument: ", argKey

        if numIntroducedRequiredParams < numRequiredParams:
            raise ValueError('Not all required parameters')
        self.setMetaProp("params", metadataParams )
        #print metadataParams
        return params
