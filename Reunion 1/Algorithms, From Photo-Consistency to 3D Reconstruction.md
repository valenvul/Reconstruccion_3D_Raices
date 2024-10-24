Bibliografía: https://carlos-hernandez.org/papers/fnt_mvs_2015.pdf 2013

---

- [ ] 1.3 *3*
- [ ] 1.5 *3*
- [ ] 3
	- [x] 3.1 *18*
	- [ ] 3.2 *10*
	- [ ] 3.3 *12*
	- [ ] 3.4 *14*

Se enfoca en algoritmos de multi-view stereo

Las representaciones más populares que devuelven los algoritmos son:
- Depthmap
- Pointcloud
- volume scalar field. Es convencion tratarlo como una funcion de distancia a la superficie
- mesh

Level set solia ser popular ya que podia sopotar cambios topologicos. Peroo fue reemplazado por otros métodos. Inicializar los volumenes con visual hull tampoco es tan popular. 

De todas fromas existen algoritmos que automaticamente extraen la silueta de las imágenes.
- Neill D.F. Campbell, George Vogiatzis, Carlos Hernández, and Roberto Cipolla. Automatic 3D object segmentation in multiple views using volumetric graph-cuts. In British Machine Vision Conference, volume 1, pages 530–539, 2007.
- Neill D.F. Campbell, George Vogiatzis, Carlos Hernández, and Roberto Cipolla. Automatic 3D object segmentation in multiple views using volumetric graph-cuts. Image and Vision Computing, 28(1):14 – 25, January 2010.
- Neill D.F. Campbell, George Vogiatzis, Carlos Hernández, and Roberto Cipolla. Automatic object segmentation from calibrated images. In Visual Media Production (CVMP), 2011 Conference for, pages 126 – 137, Nov. 2011.

![[Reconstruction paths.jpg]]

# Representaciones 3D y sus aplicaciones
![[Scene representation evaluation.jpg]]

[165, 176] Evaluaciones de algoritmos
Modelos que son geométricamente exactos no siempre producen la mejor visualización.

# Algoritmos que producen DepthMaps
La representación en depthmaps es la más popular dado su flexibilidad y escalabilidad. Si uno tiene muchas imágenes y lo parámetros de la cámara, uno puede simplemente reconstruir un mapa de profundidad de cada imagen y, tratandolo como un arreglo de puntos 3D, multiples mapas pueden ser considerados como un point cloud ya de entrada.

Para algoritmos de stereo con multiples vistas, se traba bajo la asunción de que se tiene una baseline angosta. Se toman un conjunto de imágenes junto a los parámetros de la cámara y se decretiza el rango de profundidad válido a un rango acotado y finito, Luego se reconstruye, la geometría 3D para una  imagen de referencia. 

## Winner takes all
Una manera simple de reconstruir es, tomar una imagen, algunas imágenes vecinas y un rango de valores de profundidad que contienen a la escena. Una vez computado el depthmap, se puede evaluar los valores de *photo-consistency* de cada valor del rango de profundidad. Luego elegir el que tiene mayor consistencia para cada pixel independientemente. Una medida de consistencia pueda ser la correlación cruzada normalizada. ![[Depth Map estimation algorithm.jpg]]
Además se evalúa el nivel de confianza, para que los mapas de profundidad con menos confianza sean ignorados o pesen menos en la union de modelos que viene después.
![[Winner takes all depth map.jpg]]

### Función de consistencia
El algoritmo anterior funciona relativamente bien, pero no hay garantía de que la apariencia en la ventana seleccionada sea única en toda la superficie del objeto. Una ventana más grande haría que sea más único pero hace que la estimación de la profundidad sea menos precisa. Ademas no lidia bien con oclusiones o superficies no lambertianas.

Otro algoritmo propone, dada las curvas de consistencia en cada pixel, que son calculadas entre la imagen de referencia y cada una de sus imágenes vecinas, el algoritmo primero identifica los máximos locales para las curvas.
 Sea $d_{k}$ la profundidad y $\mathcal{C}_{k}$ el valor de consistencia para el $k$-ésimo máximo local. La función de robust photoconsistency se calcula como: $\mathcal{C}^{R}(d)=\sum_{k}\mathcal{C}_{k}W(d-d_{k})$. Donde $W$ es una función de kernel como por ejemplo la función gaussiana. Esta funcion permite mejorar mucho el ruido entre las funciones de consistencia y conseguir el mejor maximo.
 ![[Robust depth map consistency.jpg]]
Otro método sería ignorar los valores de cosnistencia que som menores a cierto umbral. Se descarta la estimación de profundidad de un pixel cuando el nivel de confianza de esta es menor a cierto umbral. Cuanto mayor sea va a haber menos ruido, pero más agujeros en la estimación.

Un dolo mapa puede  tener agujeros y ruido, pero al usar multiples para la reconstrucción, esta es más robusta. Se necesitan muchas imágenes para que el modelo esté completo y sin agujeros.

- [190]
- [80]

## MRF
El pico de la curva de la función previa puede no corresponderse con la profundidad real en casos difíciles. Si hay oclusiones severas puede no existir un pixel correspondiente en las otras imágenes. Una solución es obligar a que haya consistencia espacial, bajo la hipotesis de que los pixeles vecinos tienen profundidades similares. Para esto se usan MArkov Random Fields. Es una formulación de mapas de profundidad que puede ser vista como un problema de optimación combinatorio en el que un rango de profundidad de entrada es dicretizado a un rango finito. La idea es asignarle una etiqueta de profundidad $k_{p}$ de un conjunto de etiquetas a cada pixel $p$, minimizando la siguiente función de costo: $E(\{k_{p}\})=\sum_{p}\Phi(k_{p})+\sum_{(p,q)\in\mathcal{N}}\psi(k_{p},k_{q})$.
La primer suma es sobre todos los pixeles de la imagen mientras que la segunda es sobre todos los pares de pixels vecinos denotados $\mathcal{N}$. Estos se definen por vecindarios de a 4, en los que un pixel está conectado con los adyacentes horizontal y vertical mente, o vecindarios de 8, en los que además se toma en cuenta los pixels que se encuentran en diagonal.
$\Phi$ es la *unary potential* y $\Psi$ es la pairwise interaction potential.

==Potencial unario==
Refleja la información de foto consistencia, donde el costo debe ser inversamente proporcional a la cosistencia. La definición varía segun la medida de consistencia que se use.

==Potencial de interacción de a pares==
Este costo busca asegurar la regularización espacial y debe ser proporcional a la discrepancia de profundidad que hay entre pixels vecinos, para que los pixels vecinos tengan niveles de profundidad similares. Puede ser definida de muchas manera pero una es $\psi(k_{p}=d_{1},k_{q}=d_{2})=min(\tau_{p},|d_{1}=d_{2}|)$

Existen optimizaciones.

- [120]
### Multi hypothesis MRF Depthmaps
Para mejorar los resultados, en vez de usar un rango de profundidad discreto elegido de maneara aleatoria, el algoritmos extra los maximos locales de la consistencia de cada pixel, después se usa MRF para asignar la profundidad de uno de esos máximos a cada pixel. De esta forma, cada pixel tiene un conjunto de etiquetas distinto. También agregan una etiqueta que indica que no se puede estimar la profundidad correctamente u por ende no se debe evaluar ese pixel a la hora de reconstruir la superficie.

Primer hay una fase de extracción de etiquetas de profundidad. Consiste en encontrar las hipotesis de profundidad para cada pixel $p$ en referencia a una imagen de referencia $I_{ref}$. Se computa la curva de foto consistencia entre $I_{ref}$ y cada uno de sus vecinos. Los $K$ picos con el mayor valor de todas las curvas se almacenan. Se usa NCC para calcular dicha consistencia.

Después viene un etapa de optimización con MRF. Se asigna la etiqueta de profundidad con MRF. El costo unario busca minimizar las hipotesis con menor puntuaciones de consistencia. Además se agrega una penalización a la etiqueta de unknown. $$\begin{equation}\Phi(k_{p}=x)=\begin{cases}\text{exp}[-\beta\cdot\mathcal{C}(p,x)]& \text{if }x\in\{d_{i}(p)\}\\\Phi_{\mathcal{U}} & \text{if }x=\mathcal{U}\end{cases}\end{equation}$$
Despues la termino de pares obliga a que haya regularización espacial.  Se define en base a las combinaciones posibles de etiquetas, clasificandolas en etiquetas puras y la unknown
 $$\begin{equation}
 \Psi(k_{p}=x, k_{q}=y)=
 \begin{cases} 
2\frac{|x-y|}{(x+y)} & \text{if } x\in\{d_{i}(p)\},& y\in\{d_{i}(p)\} \\
\Psi_{\mathcal{U}} & \text{if }  x=\mathcal{U},& y\in\{d_{i}(p)\}  \\
\Psi_{\mathcal{U}} & \text{if } x\in\{d_{i}(p)\}, &y=\mathcal{U}\\
0 & \text{if } x=\mathcal{U}, & y=\mathcal{U}
\end{cases}
 \end{equation}$$
 Cuando las dos etiquetas son valores de profundidad el costo se mide como la discrepancia normalizada entre ambos. En los dos del medio como uno es unknown se impone la penalización. En el ultimo como son iguales se pone 0 ya que esto favorece lal consistencia espacial.
![[MRF.jpg]]

Se consigue un modelo completo con menos depthmaps y solo se agregan profundidades con alta confianza.

### Real Time Plane Sweeping
La reconstrucción por mapas de profundidad no es computacionalmente barata ya que es necesario calcular la función de foto consistencia para cada pixel de cada imagen en cada profundidad hipotetizada. Se demostró que se puede hacer de manera lineal usando GPU.
Este algoritmo agarra una familia de planos paralelos en una escena, proyecta imágenes a un plano y despues evalua la foto consistencia en cada plano. Después se elige la profundidad de cada pixel con la técnica de winner takes all. 

Primero, el algoritmo recorre la escena en múltiples direcciones, que son extraídas de la escena tal que la dirección se alinie con la estructura de la escena a ser reconstruida. Esto ayuda a que las imágenes se proyecten correctamente sobre la orientación de la superficie y se logre una  mejor correlación entre las ventanas que son evaluadas para la foto consistencia en cada imagen. Cada dirección produce un mapa de profundidad y luego multiples de estos se mezclan para conseguir el modelo final.

Esta estrategia sirve más efectivamente para escenas en las que esxisten pocas direcciones dominantes, que pueden ser extraídas de un pointcloud reconstruido por SfM.

Se usa la GPU para reproyectar las imágenes y calcular la foto consistencia.

- [76] 
### Second order Smoothness
Se le agrega un prior de suavidad. Este actua en un par de pixels y trata de minimizar la diferencia de profundidad entre estos. En escenas de la vida real usar esto causaria artifactos ya que trataria de llevar todos los planos de la escena a ser paralelos a la imagen.

Se introdujo un algoritmo que usa MRF pero introduce una suavización de segundo orden de a tres pixels. Dados tres pixels adyacentes se penaliza un costo de suavidad, que es la aproximación de la segunda derivada, y se vuelve 0 cuando la de primer orden es constante.

![[Smoothness prior depth map reconstruction.jpg]]

- [196]

## Conclusiones
Los depth maps son buenos para muchas aplicaciones como analisis de escena y visualización, pero presentan problemas cuando se los busca mezclar en un solo modelo 3D global. La calidad de la reconstrucción es además inversamente proporsional a la distancia de la superficie. Las soluciones encontradas para enforzar consistencia geometrica entre los depthmaps hacen que el problema de optimación crezca mucho y se vuelva muy caro computacionalmente.
# Point cloud
Las representaciones de pointcloud reconstruyen un solo pointcloud 3D usando todas las imágenes de input, y además siguen pudiendo ser facilmente manipulables.

Los algoritmos de reconstrucción por pointcloud hacen uso de la propiedad asumida de consistencia espacial y expanden la point cloud en la superficie de la escena durante el proceso de reconstrucción en vez de concentrarse en un punto a la vez.

PatchMatch Stereo. Inicializa los valores de profundidad de manera aleatoria y las refina basandose propagación local y busqueda aleatoria.
 
PMVS  itera entre expandir el pointcloud y filtrarlo una vez que reconstrute una cantidad de patches iniciales medinate feature matching. El paso de filtrado analisa la consistencia de patches entre todas las vistas y remueve los que se reconstruyeron mal.

La salida es un conjunto de patches para la escena entera. Cada patch es una aproximación del plano tangente a la superficie. Cada patch se define segun la ubicacion de su centro y la direccion de su normal.


- [74] PMVS es open source (ahora CMVS)
https://www.di.ens.fr/cmvs/

- [132]
- [85]
- [40]
- [34]
# Volumetric
## Graph cuts
# Mesh refinement

# Bibliografia