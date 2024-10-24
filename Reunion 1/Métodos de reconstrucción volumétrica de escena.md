# Métodos de reconstrucción volumétrica de escenas a partir de fotografías

***Bibliografía principal:***

https://www.researchgate.net/publication/221257818_A_Survey_of_Methods_for_Volumetric_Scene_Reconstruction_from_Photographs

Tener en cuenta que es un paper del 2001. Deben existir mejoras para los algoritmos presentados, pero sirve como explicación conceptual de los algoritmos más usados.

[https://carlos-hernandez.org/papers/fnt_mvs_2015.pdf](https://carlos-hernandez.org/papers/fnt_mvs_2015.pdf) cap.3

El libro es del 2013 por lo que los algoritmos presentados son un poco más actuales. Solo trata algoritmos para sistemas stereo con múltiples vistas.

---
# Visual Hull

El *visual hull* de un objeto puede ser descrito como la forma maximal que resulta en la misma silueta que el objeto real para todas las vistas que se encuentran por fuera de su casco. La idea es usar un conjunto finito de vistas y computar el visual hull inferido.

Se comienza con la proyección de un objeto a $N$ planos de imagen conocidos, es decir imágenes del objeto con sus cordenadas conocidas. Cada una de estas imágenes tiene que ser segmentada en una imagen binaria que distingue entre el foreground, que contiene las regiones a las que el objeto es proyectado, y el background, es el resto. Retropropagando estas regiones de foreground en el espacio 3D, se puede conseguir la intersección entre el foreground de todas las imágenes. El volumes resultante es el visual hull buscado.

Esta representación es solo una aproximación del objeto, pero que asegura que el objeto real va a estar dentro de las fronteras calculadas.


> [!warning] Desventajas
> La calidad de la aproximación depende de la geometría del objeto y del rango de vistas usado, cuantas más imágenes del objeto se tengan mas chico será el visual hull. De todas formas, puede ser que no todas las concavidades sean capturadas sin importar cuantas imágenes se usan.


![[Visual hull.jpg]]

---

# Voxel Coloring

***Color Consistency***

![[Voxel Color Consistency.jpg]]

La idea de los métodos de Voxel Coloring se basa en distinguir cuáles son los puntos 3D que pertenecen a la superficie del objeto, a partir de su consistencia de color. Dado un punto en una superficie opaca, si dos cámaras lo observan desde distintos lugares, van a observar el mismo color. En cambio, si pueden ver más allá de la intersección de las vistas van a estar observando superficies más lejanas que son inconsistentes en términos de color.


> [!warning] Desventajas
> Esta medición tiene ciertos problemas. Las escenas en la vida real suelen presentan superficies con cambios de color abrupto, y esto puede hacer que el método falle en la reconstrucción. Para mejorar la eficacia se puede agregar un umbral adaptativo que aumenta cuando los voxels parecen inconsistentes en una imagen.


***Algoritmo de Voxel Coloring***

El algoritmo de *Voxel Coloring* empieza con un volumen de voxels opacos que encapsulan el objeto a ser reconstruido. Luego se itera sobre este, midiendo la consistencia de color de los voxels en este volumen. Es decir, si entre las proyecciones del voxel a las imágenes de entrada el color de los pixeles es consistente. Aquellos voxels considerados inconsistentes son tallados del volumen. El algoritmo termina cuando todos los voxels se determinan consistentes

En cada iteración, el volumen resultante va cambiando, por lo que la oclusión generada por ciertos voxels a ciertas vistas también lo hace. Cuando se elimina un voxel, este permite que ciertas vistas vean al voxel que se encontraba debajo y antes no veían. Entonces, para medir la consistencia de un voxel es necesario definir antes la visibilidad de este, el conjunto de pixeles de imágenes que lo ven. Es necesario calcular esto para cada voxel del modelo por lo que es esencial su eficiencia.

## Restricted Camera placement

Para simplificar el cálculo de la visibilidad la primera versión del algoritmo buscaba limitar los cambios en oclusiones que podían ser generados, y así calcular la consistencia de cada voxel una única vez. 

Para esto, se restringe la llamada *ordinal visibility* de las posiciones de las cámaras. Estas deben estar ubicadas de tal manera que se pueda hacer un único pase por el volumen, en orden de más cercano a más alejado de la cámara. Para lograr esto, se ponen todas las cámaras en un solo lado de la escena y se evalúan los voxels en planos que son cada vez más lejanos a las cámaras. De esta forma, la transparencia de los voxels que pueden ocluir a cierto voxel de interés es determinada antes de que la consistencia de color del voxel sea evaluada. 

Para tomar en cuenta estas oclusiones se calcula un bitmap con un bit por pixel en la cámara de entrada. Inicialmente todas las oclusiones están apagadas. Al evaluar las proyecciones del voxel, si en el bitmap de oclusiones de la cámara esos pixeles están prendidos, no son tomados en cuenta para el cálculo de la consistencia.

![[Voxel Coloring occlusion map.jpg]]


> [!warning] Desventajas
> La restricción presentada por la ordinal visibility es significante. Al tener todas las cámaras de un lado de la escena, ciertas superficies no van a ser visibles en ninguna imagen y no podrán ser reconstruidas. 


## Arbitrary Camera Placement

Para conseguir una reconstrucción robusta desde todos los ángulos, se desarrollaron variaciones al algoritmo de voxel coloring original. Estos nuevos algoritmos se basan en evaluar cada voxel reiteradas veces hasta que la visibilidad de estos se estabilice.

Todos los métodos se basan en el mismo pseudo código. Un loop interno encuentra la visibilidad de los voxels, se mide su consistencia y si este es inconsistente se lo excluye del modelo. Este cambio en el volumen puede implicar un cambio la visibilidad de algunos voxels, por lo que el loop externo repite el chequeo de consistencia hasta que no se excluyan más voxels en el loop interno.

![[Voxel Coloring.jpg]]

Se comprobó que el algoritmo no falla por eliminar voxels muy temprano, siempre que se use una medida de consistencia razonable. Esta medida debe ser monótona, es decir, si encuentra que un conjunto de pixeles es inconsistente, el superconjunto al que este pertenece también debe ser inconsistente. Como solo se eliminan voxels del modelo pero no se agregan nuevos, los pixeles que pueden ver a un voxel en un determinado momento son un subconjunto de aquellos que lo pueden ver más adelante. De esta forma, el algoritmo encuentra el modelo único consistente en color que es el superconjunto de cualquier otro modelo consistente. 

### Space Carving

### Generalized Voxel Coloring

*GVC* es una implementación del voxel coloring con las cámaras posicionadas de manera arbitraria. Tiene dos variantes, llamadas *GVC-IB* y *GVC-LDI,* que se diferencias por las estructuras de datos que usan para los cálculos de la voibilidad de los voxels.

![[GVC.jpg]]

*GVC-IB*, como su nombre lo indica, basa su cálculo en el item buffer. Este almacena, para cada pixel de cada imagen, el voxel de superficie que es visible desde dicho pixel. Por otro lado, *GVC-LDI* almacena los datos en una layered depth image. Esta guarda, por cada pixel de cada imagen, una lista de todos los voxels de superficie que proyectan a ese pixel, en orden de profundidad.


> [!warning] Desventajas
> La información almacenada en el item buffer es un subconjunto de la almacenada en la LDI, por lo que este último consume mucho más memoria.


***GVC-IB***

Para inicializar item buffer, cada input puede ser calculado rendereando el conjunto de voxels de superficie actual a la vista de la imagen, usando *Z-buffering* (un método de gráficos de computadora [https://es.wikipedia.org/wiki/Z-buffer](https://es.wikipedia.org/wiki/Z-buffer)). Este método suele calcular el color correspondiente al voxel, pero en vez de eso, este algoritmo almacena un ID único para el voxel correspondiente en el buffer.

Para encontrar los pixels visibles a los que se proyecta un voxel en una imagen el voxel se scan-converted para encontrar los pixels en la proyección de la imagen. En el caso de IB, el voxel es visible desde el subconjunto de pixeles cuyos valores en el item buffer matchean con el identificador del voxel.

Cada vez que se elimina un voxel el IB queda inválido. Recalcular el IB cada vez que esto ocurre es muy costoso por lo que se puede seguir operando on IBs no actualizados y actualizarlos menos frecuentemente. Esto es por que la eliminación de voxels es conservadora por lo que no se van a eliminar voxels que sean necesarios. En la última iteración los IBs quedan válidos para que el conjunto de voxels final sea consistente. Es conveniente actualizar los IBs despues de la linea 3 en el código.

***GVC-LDI***

### Multi-Hypothesis Voxel Coloring

## Optimizaciones

## Alternate Voxel Space

---

# Feature Matching

## Image Space

## Object Space

---

# Conlcusiones

Los algoritmos de voxel coloring y sus variaciones generan reconstrucciones más ajustadas a la geometría real, pero fallan cuando tienen que lidiar con superficies no lambertianas, es decir, cuando la superficie no tiene la misma luminancia desde todos los puntos de vista.

En cambio, los algoritmos de visual hull soportan este tipo de superficies, pero pueden perderse detalles en la concavidad de la superficie. De todas formas en papers como el de *Detailed reconstruction of 3D plant root shape,* se presentan mejoras que pueden solucionar estos problemas.