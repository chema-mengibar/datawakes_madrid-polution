#!/usr/local/bin/python
import sys
import urllib, json
import numpy as np
import pandas as pd
import math
import itertools
import string
import copy
import collections
import time
import datetime as dt
from ast import literal_eval
import csv
import os
os.chdir( os.path.dirname(__file__) )
from os.path import isfile, join



class FileWriter( object ):

    def __init__(self):
        print 'walk, don`t run'


    def objToJson( self, jsonData, outputFullPathFile ):
        with open( outputFullPathFile  + '.json' , 'w') as outfile:
            json.dump( jsonData , outfile , indent=2)

    def jsonToObj( self, inputFullPathFile ):
        with open( inputFullPathFile ) as train_file:
            return json.load(train_file)

    def jsonToDf( self, inputFullPathFile ):
        with open( inputFullPathFile ) as train_file:
            dictTrain = json.load(train_file)

        # converting json dataset from dictionary to dataframe
        dfN = pd.DataFrame.from_dict(dictTrain, orient='index')
        dfN.reset_index(level=0, inplace=True)
        return dfN

    def dfToJsonObj( self, DF ):
        df_as_json = DF.to_dict(orient='split')
        return df_as_json
        # return DF.to_json( orient='index' )

    def dfToCsv( self, DF, outputFullPathFile ):
        DF.to_csv( path_or_buf = outputFullPathFile + '.csv' , sep=",", quoting=None, index=False )


    def csvToDF( self, _inputFullPathFile='', _sep= ',', _quotechar='', _quoting= 0 ):
        #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
        return pd.read_csv( filepath_or_buffer=_inputFullPathFile, sep= _sep, quoting= _quoting ) #,encoding="utf-8-sig"
