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

#libDir = os.path.abspath(os.path.join(os.path.dirname(__file__),"./reporters"))
#sys.path.append( libDir )
#from MultiLayerTimeSerie import MultiLayerTimeSerie


import pymongo
from pymongo import MongoClient


class mDate( object ):
    d = 0
    m = 0
    y = 0

class mLayer( object ):
    name = ""
    data = []
    color = 0

# class mLayerData( object ):
#     a=0,
#     b=0,
#     c=0


class Reporter( object  ): #MultiLayerTimeSerie


    def __init__(self, ROUTES ):
        self.routes = ROUTES

    def dfToJsonObj( self, DF ):
        df_as_json = DF.to_dict(orient='split')
        return df_as_json



    def mongoClient( self ):
        pHost =  self.routes["mongo_config"]["mongo_host"]
        pPort =  self.routes["mongo_config"]["mongo_port"]
        pPass =  self.routes["mongo_config"]["mongo_pass"]
        pUser =  self.routes["mongo_config"]["mongo_user"]
        pRole =  self.routes["mongo_config"]["mongo_role"]
        pRemote =  self.routes["mongo_config"]["mongo_remote"]

        if pRemote:
            client = pymongo.MongoClient( 'mongodb+srv://' + pUser +':' + pPass + '@' + pHost + '/' + pRole )
            #client = pymongo.MongoClient("mongodb+srv://dev:dev@tfm-ynqo4.mongodb.net/admin")
        else:
           client = MongoClient( pHost, pPort )

        return client


    def dfToReport( self, pCollection, pDf, pDatasetFields ):

        client = self.mongoClient()

        db = client[ 'reports' ]
        DFJson = self.dfToJsonObj( pDf )
        collection = db[ pCollection ]
        insertId = collection.insert( { "doc" : DFJson, "metadata":pDatasetFields }  )
        # db.collection.update({'_id' : insertId},
        #              {'$set' : {'metadata' : pDatasetFields }})
        return insertId



    def jsonToReport( self, pCollection, objJson ):

        client = self.mongoClient()
        db = client[ 'reports' ]
        collection = db[ pCollection ]

        #insertId = collection.insert( { "doc" : objJson, "metadata":pDatasetFields }  )
        insertId = collection.insert( objJson )

        # db.collection.update({'_id' : insertId}, {'$set' : {'metadata' : pDatasetFields }})
        return insertId


    def addMetadataToDoc( self, insertId, pCollection, objJson  ):

        client = self.mongoClient()

        db = client[ 'reports' ]
        collection = db[ pCollection ]

        collection.update({'_id' : insertId}, {'$set' : {'metascript' : objJson } })
