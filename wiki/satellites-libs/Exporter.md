# Module Exporter 

> **Version**: 1.0.0

> **Description:**
Contains the standard functions to work with files, and data objects like dataframes and json 

**Import module**
```py
from lib.exporter  import Exporter
exporter = Exporter( )
```
#


## Methods

|  Read Input-file|  |
| ------ | ------ |
| .csvToDF(  ) | # |
| .jsonToDf(  ) | # |

<br>

|  Save Output-file|  |
| ------ | ------ |
| .objToJson(  ) | # |
| .dfToCsv(  ) | # |

<br>

|  In-flow utils|  |
| ------ | ------ |
| .dfToJsonObj(  ) | # |





#
## Usage 

> ### **From input file** 

**.csvToDF(** DF, inputFullPathFile **)** <br>

```py
if __name__ == '__main__':

    inputs = reloader.getInputs()
    [...]
    #Get the fileItem 1 fromThe inputBlock 0
    myDF = exporter.csvToDF( inputs[0]["path"][1] )
```



**.jsonToDf(** inputFullPathFile **)** <br>
Get the content of a file and creates a pandas Dataframe.

```py
if __name__ == '__main__':

    inputs = reloader.getInputs()
    [...]
    dfYT = exporter.csvToDF( inputs[1]["path"][1] )
```

> ### **Save output file** 
**.objToJson(** jsonData, outputFullPathFile **)** <br>
Save a file .json ( the file-extension will be added in function) .

```py
if __name__ == '__main__':

    inputs = reloader.getInputs()
    myDF = [...]
    [...]
    outputParams =  reloader.getOutputPath( "my_suffix_filename" )
    exporter.objToJson( myDF, outputParams["path"] )
```

**.dfToCsv(** DF, outputFullPathFile **)** <br>
Save a file .csv ( the file-extension will be added in function) .

```py
if __name__ == '__main__':

    inputs = reloader.getInputs()
    myDF = [...]
    [...]
    outputParams =  reloader.getOutputPath( "my_suffix_filename" )
    exporter.dfToCsv( myDF, outputParams["path"] )
```


> ### **In-flow utils** 



**.dfToJsonObj(** DF **)** <br>
Creates a json object from a pandas Dataframe. <br>
The result json-object can be saved in a doc MongoDb or in a raw-file.
```py
if __name__ == '__main__':

    inputs = reloader.getInputs()
    [...]
    DFJson = exporter.dfToJsonObj( myDF )
```
