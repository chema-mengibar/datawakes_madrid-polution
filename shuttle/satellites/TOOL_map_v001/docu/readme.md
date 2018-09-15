# T00_map_v001

El objetivo del script es crear un mapa 2d a partir de las cordenadas de una region.
La gran cantidad de coordenadas, y el proceso de conversion y x,y hace que el renderizado del mapa se ralentize.
Por ello, se ha anyadido un filtro que reduce los puntos de los poligonos.


## Librerias
### visvalingamwyatt
https://github.com/fitnr/visvalingamwyatt
Mediante la libreria ***visvalingamwyatt*** es posible reducir el numero de puntos de un poligono manteniendo la forma.
El metodo de simplificacion utiliza un ratio ( 0.0 -> 1.0 ) como parametro que marca la intensisdad de la reducción, siendo 1 = nula.

El problema reside en aplicar el mismo ratio a formas con diferentes numeros de puntos. Si una poligono tiene 100 puntos, aplicandole 0.1 obtendriamos 10 puntos.
Aplicando el mismo ratio a un poligono con 1000 puntos obtenemos 100. por lo que la reducción no es realmente igual, si no proporcional.

Para poder opbtener un mapa en el que los poligono poseen el mismo grado de simplificación es necesario aplicar un ratio diferente a cada poligono segun el numero de puntos.
Por ello se llevan a cabo una serie de condiciones en el metodo 2 de la clase *MapService*.
