# Datawakes | Madrid polution.

EL datawake se centra en el juego de datos de la polución de Madrid.

## Set up

1. Download the datasets from the repositories

2. Install the requirements

3. Change the projects routes to your local paths
`[ROOT]/shuttle/satellites/lib/router.py`  

4. Run manually in the terminal the satellites sequences described in the  
 `[ROOT]/shuttle/satellites/sequences.xml`


## Throwing a satellite
*Draft: Terminal and Shuttle*

Before to throw a satellite be sure the **metascript.json** in each folder has the right values:  
* name of satellites
* input files
* output target
* parameters (if necessary)
* description
* etc...



#### Throwing a satellite in terminal
Then open the satellite-directory in the terminal a throw the script.

Python example:
 ```
cd [ROOT]/shuttle/satellites/A00_extract-zip_v01
python main.py
 ```
or
 ```
cd [ROOT]/shuttle/satellites/A00_extract-zip_v01
.\main
 ```

#### Throwing a satellite with Shuttle

---

## Datasets

> ### Air quality Madrid
**url:** https://www.kaggle.com/decide-soluciones/air-quality-madrid  
**folder-name:** air-quality-madrid  
**datawake-folder:** universe/stage

> ###   Spain postal-codes and geo-polygons
**url:** https://github.com/inigoflores/ds-codigos-postales   
**folder-name:** ds-codigos-postales-master  
**datawake-folder:** universe/master

---

## Requeriments

#### Python
* ast
* base64
* copy
* collections
* csv
* datetime
* decimal
* graphviz
* itertools
* json
* math
* matplotlib.pyplot
* matplotlib.patches
* numpy
* pandas
* pandas.compat * StringIO
* reportlab.graphics
* simplejson
* string
* svglib.svglib
* svgwrite
* sys
* time
* urllib
* urllib2
* zipfile
* shapely   
  - https://pypi.org/project/Shapely/#downloads
  - https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely

---

## Links

> #### Centro Nacional de Información Geográfica (CNIG)
**url:** http://centrodedescargas.cnig.es/CentroDescargas/buscadorCatalogo.do?codFamilia=02122    

> #### Shapely: python module
http://toblerity.org/shapely/manual.html  
http://toblerity.org/shapely/project.html
