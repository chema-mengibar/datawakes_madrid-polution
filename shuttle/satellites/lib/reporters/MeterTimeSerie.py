
class RegPlatform( object ):
    top = 0
    value = 0
    name = ""

class Frame( object ):
    def __init__(self):
        self.unique = ""
        self.blocks = []

class Serie( object ):
    def __init__(self):
        self.attr = {}
        self.data = []

#float(rowData.iloc[0][ dataCols[0] ]),

class MeterTimeSerie( object ):

    def __init__( self ):
        self.name = "MeterTimeSerie"
    
    def builder( self, pSourceDfs, pMeterKeys, pRowKey, blockKey ):

        builderData =  {}
        numDfs = len( pSourceDfs )
        for blockId, blockItem in  enumerate( pSourceDfs ):
              
            #Barcelona
            serie = Serie()
            blockUniqueName  = blockItem.iloc[0][ blockKey ] #pSourceDfs[0]
            
            serie.attr[ blockKey ] = blockUniqueName
            for index, row in blockItem.iterrows():
                        
                frameData = Frame()
                frameData.unique = row[pRowKey]
               
                for mkId , mkItem in enumerate( pMeterKeys ):
                    
                    regPlatform = RegPlatform( )
                    regPlatform.top = row[ mkItem["top"] ]
                    regPlatform.value = row[ mkItem["value"] ]
                    regPlatform.name = mkItem["name"]
                    frameData.blocks.append( vars( regPlatform ) )
                
                serie.data.append( vars( frameData ) )
        
            builderData[ blockUniqueName ] =  vars( serie ) 
        
        return builderData

