# Module Reloader 

> **Version**: 1.0.0

> **Description:**
Constains the tools to allow the Scripts acces their metadata, 
acces the datasets in the diferents repositories,
and the methods to create and read the metadata of the datasets.

**Import module**
``` py
from lib.router  import Router
from lib.reloader  import Reloader
router = Router( )
ROUTES =  router.getRoutes()
reloader = Reloader( currentFullRoute, ROUTES  )
```
#
## Properties ( self )
| Property Name |  |  |
| ------ | ------ | ------ |
|  .dir_path |  | # |
| .dir_root |  | # |
| .routes |   | # |
|  |  master | # |
|  |  processed | # |
|  |  stage | # |
|  |  reports | # |
| .mongo_host |  | # |
| .mongo_port |  | # |
| .params |  | # |
| .metaScript |  | # |
| .metaScriptOutput |  | # |
|  .scriptName |  | # |
| .fullOutputPath |  | # |
|  .metaData |  | # |
|   |  .date_creation | # |
|   |  .script_name | # |
|   |  .inputs | # |
|   |  .output | # |
|   |  .params | # |

#

## Methods
| Getters, Setters |  |
| ------ | ------ |
| .loadMeta( pCurrentDir ) | # |
| .setMetaColumns( prop, val ) | # |
| .setMetaProp( prop, val ) | # |
| .saveMetas() | # |
| .getMetaInfo( prop ) | # |
| .getMetadata( docName ) | # |
| .setMetaOutputCollection( collectionName ) | # |
| .getInputs() | # |

| Utils |  |
| ------ | ------ |
| .isMongoTarget() | # |
|  .addMetaOutputDoc() | # |
| .today() | # |
| .parseArgs( args ) | # |

| Flow |  |
| ------ | ------ |
| .createOutputDir( DIR ) | # |
| .getOutputPath() | # |

#
## Usage 

**Catch Terminal arguments** <br>
Get the gived arguments in command. Not necessary after main block. <br>
If arguments ar required, trhow and exception

```py
if __name__ == '__main__':
    params = reloader.parseArgs( sys.argv[1:] )
```

**Inputs file references** <br>
Get from metascrip the input objects
```py
if __name__ == '__main__':
    inputs = reloader.getInputs()
    postalCodesFile =  inputs[1]["path"][0]
```

**Output file propertires** <br>
Generate the full path to save the script files (  with add file suffix )
```py
if __name__ == '__main__':
    [...]
    outputParams =  reloader.getOutputPath( "test-005" )
```


**Difference output Target source ( Mongo or Directory )** <br>
Create the metada.json file in the data-ouput folder 
```py

    [...]
    if not reloader.isMongoTarget() :

        reloader.addMetaOutputDoc( outputParams["file_name"] )
        exporter.dfToCsv( dfRYt, outputParams["path"] )

    else:
        print outputParams
        db = client[ outputParams["db"] ]
        
        DFJson = exporter.dfToJsonObj( dfRYt )
    
        collection = db[ outputParams["collection"] ]
        insertId = collection.insert( DFJson )



        reloader.addMetaOutputDoc( str( insertId ) )
```

**Generate metada output file**
Create the metada.json file in the data-ouput folder 
```py
if __name__ == '__main__':
    [...]
    outputParams = reloader.getOutputPath( "my_suffix" )
    reloader.saveMetas()
```



