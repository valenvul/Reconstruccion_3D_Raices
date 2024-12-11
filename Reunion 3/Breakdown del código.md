[[Reunion 3]]

---

# Reconstrucción 3d (stereo)
## 1. Calibración de cámaras
La calibración de cámaras consiste en encontrar los parámetros que definen tanto la distorsión como las características intrínsicas y extrínsicas de la cámara. Para esto, se utilizan imágenes de un patrón ya conocido (tablero de ajedrez) de manera que se saben sus posiciones relativas en el espacio 3D. De esta forma se conocen la posición del mismo punto en cada imagen obteniendo un mapeo de los puntos en el mundo real a sus coordenadas en cada imagen, a partir del cual se pueden calcular dichos parámetros.

## 2. Rectificación de las imágenes
Una vez calculada la calibración, se puede realizar un remapeo de las imágenes para sacarles la distorsión y que los planos epipolares de cada par de imágenes estén alineados.

## 3. Calcular la disparidad
Para este paso nuevamente se necesita un patron conocido (tablero de ajedrez o april tags), que se fotografía junto con el objeto a reconstruir, de esta forma se puede calcular la disparidad entre las fotografías stereo.
Una vez detectado este objeto conocido, se pueden calcular tanto la rotación como la traslación de las cámaras en el espacio con respecto a dicho objeto. Luego, con estos puntos, se calcula la *matriz de transformación homogénea*, que permite pasar del sistema de coordenadas de la cámara al sistema del objeto y viceversa.
Por último, se calcula la disparidad en vase a las imágenes rectificadas.

## 4. Reproyección a 3D
Usando la disparidad y la *matriz de la cámara*, se reproyectan los puntos a 3D.

---
# Posición de las cámaras
La posición de las cámaras queda almacenada en la matriz de transformación homogénea. En el código hay dos matrices:
- La matriz `c_T_o` es la transformación que toma puntos expresados en el sistema de coordenadas del mundo y los lleva al sistema de coordenadas de la cámara. $$c\_T\_{o}= \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix}$$donde $R$ es la matriz de rotación ($3\times 3$) y $t$ es el vector de traslación ($3\times1$).
- La matriz `o_T_c` es la inversa de la matriz anterior, y representa la transformación que lleva los puntos expresados en coordenadas de la cámara al sistema de coordenadas del mundo.

Hay una de cada una de estas matrices por cámara en el dataset, y cada `c_T_o` se almacenan en la lista `all_camera_extrinsics`.

Como se explicó antes, la posición de la cámara se almacena en la ultima columna de la matriz `c_T_o` y para acceder a esta basta con la cuenta $-R^{T}\times t$.


---
# Filtrado de la nube de puntos
Dado que las imágenes de las raíces a reconstruir tienen siempre el mismo formato  (el april tag arriba y un tanque de tamaño fijo) el filtro se puede definir segun la distancia en el eje z a estas. 
En los datasets de prueba este formato no se respeta por lo que hay que implementar filtros manuales a ojo o definir otro tipo de filtrado.

### Algoritmos de filtrado de nubes de puntos:
- Clustering de DBSCAN
	Detecta agrupaciones densas en la nube de puntos permitiendo la identificación del objeto si es la parte mas densa de la nube.
- Distancia al centro de la escena
- Segmentación basada en planos
	Si el fondo es plano se puede usar una segmentación basada en RANSAC para eliminar el plano y quedarse con el objeto
- Bounding Box    c 
	
# Visualización
- py vista
- mesh io para almacenar nubes de puntos. (conectividad 0)