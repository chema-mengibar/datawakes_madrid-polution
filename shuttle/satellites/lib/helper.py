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
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
os.chdir( os.path.dirname(__file__) )
from os.path import isfile, join



class Helper(object):

    def __init__(self):
        #init
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        #print 'walk, don`t run'


    def isCombinationInList(self, searchList, targetList ):
        uniqueSearchItemsList = set( searchList )
        uniqueTargetItemsList = set( targetList )
        res =  [ x for x in uniqueSearchItemsList if x in uniqueTargetItemsList ]
        if len( res ) == len( uniqueSearchItemsList ):
            if len( res ) == len( searchList ):
                if len( res ) == len( targetList ):
                    return 2
                else:
                    return 1
            else:
                return 0
        else:
            return -1

    def allCombinations( self, listNumbers, nunItems ):
        resultsTuples = itertools.combinations( listNumbers, nunItems )
        return [list(elem) for elem in resultsTuples]
        


