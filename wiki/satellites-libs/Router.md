# Module Router

>**Version**: 1.0.0

> **Description:**
Get the absolute routes from the project. The absolute routes are just used by the Reloader module, or in custom main functions, but the absolute paths will be not saved in the metada or metascript files. The enviroment use references to acces the absolute path, like stage, universe. <br>The absolute paths are in this module hard-definned.

**Import module**
``` py
from lib.router  import Router
router = Router( )

```
#
## Properties ( self )
| Property Name |  |  |
| ------ | ------ | ------ |
|  .root |  | # |
|  .universe |  | # |
|  .processed |  | # |
|  .stage |  | # |
|  .master |  | # |
|  .satellites |  | # |
|  .reports |  | # |
|  .mongo_host |  | # |
|  .mongo_port |  | # |


#

## Methods
| Getters | Desc | Return |
| ------ | ------ | ------ |
| .getUniverse( ) | # |
| .getProcessed( ) | # |
| .getStage( ) | # |
| .getMaster( ) | # |
| .getSatellites( ) | # |
| .getReports( ) | # |
| .getRoot( ) | # |
| .getMongo( ) | # |
| .getRoutes( ) | Return an object with properties | **Obj-properties:**  <br> .root <br> .universe <br> .processed <br> .stage <br> .master <br> .satellites <br> .reports <br> .mongo_host <br> .mongo_port |


#
## Usage 

**getRoutes()**
Get the absolute routes from the project.

```py
ROUTES =  router.getRoutes()

if __name__ == '__main__':
    print ROUTES.stage
```
