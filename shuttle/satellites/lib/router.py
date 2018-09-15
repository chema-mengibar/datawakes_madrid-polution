#!/usr/local/bin/python
import sys

import os
os.chdir( os.path.dirname(__file__) )
from os.path import isfile, join

class Router(object):

    def __init__( self ):
        #init
        #self.data_captures = os.path.dirname(os.path.realpath(__file__))

        self.rootFolder = 'datawakes_madrid-polution'
        self.root = '[ABSOLUTE_LOCAL_PATH_TO_PROJECT_FOLDER]' + self.rootFolder +  '\\'

        self.universe =  self.root + 'universe\\'
        self.processed =  self.root + 'universe\\PROCESSED\\'
        self.stage =  self.root + 'universe\\STAGE\\'
        self.master =  self.root + 'universe\\MASTER\\'
        self.reports =  self.root + 'universe\\REPORTS\\'

        self.satellites =  self.root + 'shuttle\satellites\\'

        self.mongo_remote = False

        if self.mongo_remote:
            self.mongo_host = 'abc-ynqo4.mongodb.net'
        else:
            self.mongo_host = 'localhost'

        self.mongo_port = 27017
        self.mongo_pass = 'dev'
        self.mongo_user = 'dev'
        self.mongo_role = 'admin'


    def getUniverse( self ):
        return self.universe

    def getProcessed( self ):
        return self.processed

    def getStage( self ):
        return self.stage

    def getMaster( self ):
        return self.master

    def getSatellites( self ):
        return self.satellites

    def getReports( self ):
        return self.reports

    def getRoot( self ):
        return self.root


    def getRoutes( self ):
        return {
            "root": self.root,
            "universe": self.universe,
            "processed": self.processed,
            "stage": self.stage,
            "master": self.master,
            "satellites": self.satellites,
            "reports": self.reports,
            "mongo_config":{
                "mongo_host": self.mongo_host,
                "mongo_port": self.mongo_port,
                "mongo_pass": self.mongo_pass,
                "mongo_user": self.mongo_user,
                "mongo_remote": self.mongo_remote,
                "mongo_role": self.mongo_role
            }
        }
