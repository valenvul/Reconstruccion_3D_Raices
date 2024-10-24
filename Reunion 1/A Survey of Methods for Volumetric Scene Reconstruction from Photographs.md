2001
https://www.researchgate.net/publication/221257818_A_Survey_of_Methods_for_Volumetric_Scene_Reconstruction_from_Photographs
---

El término volumétrico implica una representación que describe no solo la superficie de cierta región, sino que también el espacio que dicha región envuelve. En el campo de los gráficos computacionales volumétrico implica una representación sampleada, mientras que en el de visión computacional no implica dicho muestreo. En este paper volumétrico se refiere a representaciones sampleadas, como lo son los voxels.

Todos los métodos descritos necesitan un preprocesamineto previo. Se necesitan imágenes calibradas, y excepto los métodos descritos por Szeliski y De Bonet, se asume que todas las superficies son opacas. Las técnicas de visual hull requieren que se pueda segmentar la imagen en foreground y background. El resto asuneb que las superficies reflejan la luz igualmente en todas las direcciones (aproximadamente).
# Volumetric Visual Hull
También llamado volume intersection en la literatura. El visual hull de un objeto puede ser descrito como la forma maximal que resulta en la misma silueta que el objeto real para todas las vistas (outside the convex hull of the object?). 
La idea es usar un conjunto finito de vistas y computar el visual hull inferido. Se comienza con la proyección de un objeto a $N$ planos de imagen conocidos. Cada uno de estos planos tiene que ser segmentado en la imagen binaria, el foreground contiene las regiones a las que el objeto es proyectado y el background es el resto. Si se retropropaga estas regiones de foreground en el espacio 3D y se intersectan, el volumen resultante es el visual hull inferido de la imagen.
![[Visual hull.jpg]]

El visual hull es solo una aproximación del objeto pero te asegura que el objeto real va a estar dentro de este volumen. La calidad de la aproximación depende de la geometría del objeto y del rango de vistas usado. Cuantas más imágenes más chico el visual hull. De todas formas, puede ser que no todas las concavidades sean capturadas sin importar cuantas imágenes se usan.

- Martin 83
- Chien 84
- Chien 86
- Shneier 84
- Veenstra 86
- Massone 85
- Potmesil 87
- Szeliski 93
- Gortler 96
- Garcia 98
- Luong 96
- Shashua 95
- Saito 99
- Seitz 95 y Collins 96 no producen un modelo del volumen completo
- Fromherz 94 y 95 basado en luminancia
- Moezzi 96 y 97 visual hull de video de muchas cámaras
# Voxel Coloring
## Color Consistency
La idea es distinguir puntos de la superficie a partir de su consistencia de color. Dos cámaras cuya visión no esta ocluida por una superficie pueden ver más allá de esta y por ende ven colores inconsistentes en la dirección del punto. Un voxel es considerado parte de la superficie si la .edición de inconsistencia es menor a algún umbral.
![[Voxel Color Consistency.jpg]]

Las escenas de la vida real frecuentemente presentan superficies con cambio de color abrupto. Esto puede hacer que el método falle en la reconstrucción. Para mejorar la eficacia del método se puede agregar un umbral adaptativo que aumenta cuando los voxels parecen inconsistentes en una imagen.
## Restricted Camera Placements
El algoritmo de *Voxel Coloring* empieza con una reconstrucción de volumen de voxels, inicialmente opacos, que  encapsulan la escena a ser reconstruida. A lo largo de las iteraciones, los voxels son testeados por su consistencia de color, y aquellos inconsistentes son tallados (se vuelven transparentes). el algoritmo frena cuando todos los voxels restantes son cosistentes en color.

Mientras avanza el voxel coloring, va cambiando la oclusión generada por los voxels opacos del modelo. Para testear la consistencia de color es necesario definir antes la la visibilidad del voxel, es decir el conjunto de pixeles de imágenes que pueden verlo. Hay muchas formas en la que esto puede ser calculado, y su eficiencia es escencial ya que se hace reiteradas veces durante la ejecución del algoritmo.

Para simplificar este cálculo Seitz y Dyer impusieron una restricción en lo que ellos llaman *ordinal visibility* de las posiciones de las cámaras. Es necesario que estas estén localizadas de manera que todos los voxels puedan ser visitados en un solo escaneo en orden de cerca a lejos relativo a la cámara. Esto se puede lograr poniendo todas las cámaras en un solo lado de la escena y escaneando en planos que son cada vez más lejanos a las cámaras. De esta forma, la transparencia de los voxels que pueden ocluir a cierto voxel es determinada antes de que el voxel sea evaluado para consistencia de color. Es decir, se aseguran que la visibilidad de cierto voxel deje de cambiar previo a que este sea computado. Esto es importante ya que cada voxel se evalúa una única vez. Para tomar en cuenta estas oclusiones se calcula un bitmap con un bit por pixel en la cámara de entrada. Inicialmente todas las oclusiones están apagadas.

El tiempo de cómputo esta relacionado al número de voxels de la representación.
![[Voxel Coloring occlusion map.jpg]]

- Fromherz 95 Hace un test de superficie basado en consistencia pero observando solo la luminosidad y la intersección de volumen
- Seitz 97 probo que una escena lo suficintemente colorida puede ser reconstruida usando solo consistencia de color, sin necesidad de la intersección de volúmenes. Este algoritmo es llamado Voxel Coloring
- Prock 98 Usa multiples resoluciones para agilizar el proceso de cómputo.
## Arbitrary Camera Placements
La restricción presentada por la ordinal visibility es significante, ya que al tener todas las cámaras de un lado de la escena, ciertas superficies no van a ser visibles en ninguna imagen y no podrán ser reconstruidas. Es por esto que se desarrollaron multiples variaciones de Voxel Coloring. Estos cambios implican testear cada voxel reiteradas veces ya que no se tiene certeza que la visibilidad del voxel era la correcta en la primera pasada.

El loop interno del siguiente código encuentra la visibilidad de los voxels, su consistencia en medida y si este es inconsistente se lo excluye del modelo. Cuando se excluye un voxel puede cambiar la visibilidad de los otros, por lo que el loop externo repite el chequeo de consistencia hasta que no se excluyan más voxels en el loop interno.
![[Voxel Coloring.jpg]]

- Kutulakos 98 muestra que el algoritmo no falla por eliminar voxels muy temprano, siempre que se use una medida de consistencia razonable. Esta medida debe ser monótona, si encuentra que un conjunto de pixeles es consistente el superconjunto al que este pertenece también debe ser inconsistente. Los pixeles que pueden ver a un voxel en un determinado momento son un subconjunto de aquellos que lo pueden ver más adelante. El algoritmo encuentra el modelo único consistente en color que es el superconjunto de cualquier otro modelo consistente. Lo llaman photo hull.
### Space Carving
Es una implementación del código previo.
Evalúa planos de voxels, midiendo la consistencia de color.
Hace muchas pasadas a lo largo de las direcciones positivas y negativas de cada eje. Obliga que los escaneos sean de cerca a lejos relativo a las cámaras, usando solo las imágenes cuyas cámaras ya pasaron por el plano en movimiento. De esta forma, cuando un voxel es evaluado, la transparencia de otros voxels pueden ocluirlo de la cámara que esta siendo observada, ya es sabida.

Space Carving nunca excluye voxels que no debería, pero es posible que incluya voxels inconsistentes en color. esto es porque durante los escaneos las cámaras que están por delante del plano en movimiento, no son usados para chequear la consistencia, hasta cuando los voxels siendo evaluados son visibles desde esa cámara.

Hay otro método llamado el space carving aproximado que lidia con las fallas que puede haber por el desconocimiento de la calibración de la cámara. Cuando se evalúa un voxel, el método, considera un disco de radio $r$ en cada imagen, centrada en la proyección del centro del voxel. Si hay un color de pixel que aparece es todos los discos se dice que el voxel es $r$-consistente y se queda en el volumen calculado.

- Kutulakos 98, 00a, 00b
### Generalized Voxel Coloring
Es otra implementación del código de la figura 4, también llamada GVC. computa la visibilidad de manera exacta y por ende, genera un modelo consiste al color. 

Existen variantes llamadas GVC-IB y GVC-LDI, que usan diferentes estructuras de datos, llamadas item buffers y  layered depth images, para computar la visibilidad de los voxels.
Un item buffer graba, para cada pixel en una imagen, el voxel de superficie que es visible desde la imagen. Un LDI guarda, por cada pixel en una imagen,  una lista ordenada por profundidad de todos los voxel de superficie que proyectan a ese pixel. La información almacenada en la LDI es un superconjunto de la almacenada en el item buffer y suele consumir bastante más memoria.
![[GVC.jpg]]

Cuando GVC-IB corre, el item buffer para cada input puede ser calculado rendereando el conjunto de voxels de superficie actual al la vista de la imagen, usando Z-buffering. En vez de renderear los colores como se suele hace con Z-buffering, se le agregan voxel IDs en el item buffer.

LDIs se computan similarmente pero en vez de usar Z-buffering para encontrar el voxel más cercano a cada pixel, todos los voxels de la superficie que proyectan al pixel se agregan a la lista en orden.

Para encontrar los pixels visibles a los que se proyecta un voxel en una imagen el voxel se scan-converted para encontrar los pixels en la proyección de la imagen. En el caso de IB, el voxel es visible desde el subconjunto de pixeles cuyos valores en el item buffer matchean con el identificador del voxel. Para LDI se compara con el primer voxel en la lista correspondiente.

Cada vez que se elimina un voxel el IB queda inválido. Recalcular el IB cada vez que esto ocurre es muy costoso por lo que se puede seguir operando on IBs no actualizados y actualizarlos menos frecuentemente. Esto es por que la eliminación de voxels es conservadora por lo que no se van a eliminar voxels que sean necesarios. En la última iteración los IBs quedan válidos para que el conjunto de voxels final sea consistente. Es conveniente actualizar los IBs despues de la linea 3 en el código.

Lo mismo ocurre con los LDI, pero estos pueden ser actualizados incrementalmente con un costo computacional mínimo. Los voxels se agregan o eliminan de un LDI primero encontrando los pixels en la proyección del voxel y despues agregando o eliminando el voxel de la LDI para esos pixels. Por esto los LDIs son actualizados inmediatamente después de eliminar el voxel. La ventaja principal que tienen los LDIs por sobre los IBs, es que es posible chequear qué voxels cambiaron visibilidad cunado un voxel es eliminado. Esto permite volver a chequear la consistencia solo de los voxels que cambian su visibilidad. En cambio con IBs todos los voxels deben volver a ser chequeados en cada iteración.

- Culbertson 99 Presenta resultados experimentales que muestran que la visibilidad exacta, en comparación con la aproximada de space carving, resulta en reconstrucciones que se ven mejor y son numéricamente más consistentes con las imágenes de entrada.
- Weghorst 84 IB
- Max 96 y Shade 98 LDI
### Multi Hypothesis voxel coloring
Se propuso una técnica de voxel coloring que de muchas hipótesis. Una hipostesis es un posible color para el voxel. Primero se pasa por una etapa de asignación de hipótesis para cada voxel. Después el algoritmo achica la cantidad de las posibilidades en la etapa de eliminación de hipótesis. En esta se eliminan los voxels inconsistente. Los voxels restantes son la reconstrucción final.

La asignación de hipótesis empieza determinando el color del pixel al que se proyecta el centro del voxel en cada imagen. Los colores de cada par de imágenes son comparados, y si al menos dos cámaras ven un color consistente para el voxel se le asigna dicho color como hipótesis al voxel. La consistencia la definen como un umbral a la distancia en el espacio RGB. Este proceso se repite para cada voxel. En esta etapa todavia no hay ninguna geometría reconstruida por lo que no hay ninguna información de oclusión posible. Por esto las hipotesis asignadad pueden no corresponderse con la superficie que se está reconstruyendo.

El siguiente paso, de eliminación de hipótesis, es el que toma en cuenta las oclusiones. Para una vista dada, el espacio de voxel es recorrido en una dirección compatible con la oclusión. Un voxel visible es proyectado a la imagen y el pixel correspondiente al centro del voxel es comparado a la hipótesis. Las hipótesis no consistentes son eliminadas y se repite el proceso para el resto de las vistas. Si no queda ninguna hipótesis, entonces el voxel es considerado inconsistente y se lo elimina. Luego se procesa los pixeles a los que esto le cambió la visibilidad. Se sigue iterando hasta que ya no se puedan eliminar hipótesis.

Es muy parecido a los métodos observados antes. La diferencia recae en que en este método la decisión de sacar un voxel se hace evaluando una imagen a la vez, en cambio en los otros se evalúan todas juntas. Esto simplifica la determinación de la visibilidad. Durante la etapa de eliminación de hipótesis se puede escanear el espacio de voxel de cerca a lejos en relación a una cámara a la vez. En consecuencia, siempre se puede usar los bitmaps para determinar la oclusion.

Sin embargi, requiere un mayor tiempo de procesamiento ya que las hipotesis se le asignan a todos los voxels de la reconstrucción y no solo a los de la superficie. En los otros en cambio, los voxels que nunca son visibles nunca son procesados.

- Eisert 99
- Steinbach 00a, 00b
## Volumetric Optimization
### Opaque Voxels
Si se asume que las superficies reflejan la luz igual para todos lados aproximadamente, que no hay cambios de color abruptos, y que las cámaras están correctamente calibradas se puede usar un umbral pequeño para la consistencia de color. Sino se tieme que aumentar el umbral para tener una reconstrucción.
En general no hay un solo umbral que sea ideal para toda superficie, por lo que si se define uno global necesita ser mas grande ya que uno chico puede resultas en que algunas superficies presenten agujeros.

Se presenta un método de optimización volumétrica que bsuca refinar la reconstrucción y minimizar el error de reproyección, es decir La suma de las diferencias entre una imagen generada por la proyección del modelo a una vista y la imagen real sacada desde ese plano, para todas la imágenes.
Esto resulta en un umbral de consistencia que varía espacialmenete, lo que resulta en un areconstrucción que es generalmente más adecuada a la geometría real de la escena. 

Esta optimización puede sacar voxels, asi como agregar nuevos is nota que es más favorable para la reconstrucción de superficie.

- Slabaugh 00b
### Non-opaque Voxels
Es una optimización para mejorar los problemas generados por los pixels que se encuentran en el límite entre el foreground y background y por ende tienen una mezcla de colores. Para esto, usa una opacidad parcial en los voxels.

- Szeliski 98
## Alternate Voxel Spaces
### Projective Grid Space
Optimizaciones que ayudan a lidiar con la calibración de la cámara. La idea es proyectar sobre un  espacio de voxels no uniforme que se basa en la geometría epipolar entre las vistas.
### Volumetric Wrapping
### Two linked Voxel Space
# Volumetric Pair Wise Feature Matching
## Image Space
Una forma de reconstruir una escena 3D es alinear las características entre pares de imágenes. Se puede usar una representación volumétrica para asistir en esta tarea, tipicamente usando las coordenadas de la imagen para dos ejes y la dipsaridad siendo el tercero.

Los métodos de análisis de a pares estan limitados, se necesita que la baselune sea chica por una correlación efectiva, tiene problemas con la oclusión y es como máximo una reconstucción en 2 y medio D.

Para resolver esto las técnicas empezaron a encarar el problema en 3D.

- Marr 76
- Yang 93
- Intille 94
- Chen 99
## Object Space
La teoría de level set se desarrolló para podelar imterfaces que se propagan. Para la evolución de una superficie 3D, se empieza con una superficie inicial que se mueve con velocidad $F$ por su normal. La idea es seguir la evolución de la superficie en el tiempo.

Opera sobre una grilla 3D discreta como los voxels. En cualquier momento la superficie puede ser extraída de la grilla usando el 0 level set, usando matching cubes.

La idea es que la supericie inicial encapsule la escena. Luego esta evoluciona moviendo se por su normal que apunta para adentro, hacia los objetos de la escena. Avanza cada vez mas lento cuando se acerca a los objetos. 

La función de velocidad esta basada en la correlación cruzada de colores entre pares de imágenes. Cuando esta es mala, la velocidad es alta. La vellocidad del zero level set se caomputa pata cada vista, para que solo las que no tienen la vsta ocluida aporten al cálculo de la correlación.

Se basa en el calculo analitico de derivadas, por lo que provee información geometrica como los normales y la curvatura, ademas de la representación volumetrica en voxels.

- Osher 88
- Lorenson 87
- Faugeras 98

# Conclusiones
El Visual Hull usa intersecciones geometrica por lo que puede facilmente reconstruir superficies no lambertianas. El voxel coloring, se basa en la consistencia de color. Este segundo método produce una reconstrucción más ajustada al objeto real, y no requiere el preprocesamiento de separar el foreground del backgorund en cada imagen. Pero tiene dificultades a la hora de reconstruir superficies no lambertianas.