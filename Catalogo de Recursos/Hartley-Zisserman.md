# 4. Transformaciones proyectivas en 2D

# 7. Computation of the camera matrix
La matriz de la cámara no es más que una matriz de proyección de puntos en el espacio 3D a su correspondiente en la entidad de una imagen. Para que este mapeo sea lineal es necesario que la imagen no tenga distorsión radial, así como conocer los parámetros intrínsicos de la cámara.

La matriz $P$ es una transformación que, dado $X$ un punto en el mundo real y $x$ su correspondiente en la imagen,  $x=PX$. Para cada correspondencia conocida, se deriva la siguiente relación: $$\begin{bmatrix}0^{T} &-w_{i}X_{i}^{T}& y_{i}X_{i}^{T} \\ w_{i}X_{i}^{T}&0^{T}&-x_{i}X_{i}^{T}\\ -y_{i}X_{i}^{T}&x_{i}X_{i}^{T} & 0^{T}\end{bmatrix} \begin{pmatrix}P_{1}\\p_{2}\\ P_{3}\end{pmatrix} = 0$$

# 9.Epipolar geometry
La matriz fundamental es la representación algebraica de la geometría epipolar. Dado un par de imágenes, para cada punto en una, existe una linea epipolar que le corresponde en la otra imagen. En la segunda imagen, el punto de correspondencia debe yacer sobre dicha linea. La *matriz fundamental* es el mapeo proyectivo de puntos de una imagen a lineas en la otra.

Este mapeo se puede descomponer en dos pasos. Primero el punto $x$ se mapea a algún punto $x´$ en la linea epipolar correspondiente en la otra imagen. Dicho punto es un match potencial. En el segundo paso se consigue la linea epipolar se obtiene como la linea que une $x´$ con el peipolo en la misma imágen $e´$.

# 10. 3D Reconstruction of Cameras and Structure
## Outline of the reconstruction method
Dado una serie de correspondencias de puntos entre dos imágenes, sin ninguna información extra, se puede reconstruir una escena desde dos vistas de la siguiente manera:
1. Computar la matriz fundamental a partir de las correspondencias
2. Computar las matrices de la cámara a parir de la *matriz fundamental*
3. Para cada correspondencia, computar el punto en el espacio que proyecta a ambos puntos

Si las cámaras están calibradas se calcula la *matriz esencial* en vez de la fundamental. Se puede usar información adicional para refinar la reconstrucción. En el capitulo 11 y 12 se describen implementaciones de este método.

### 1. Computation of the fundamental matrix 
La matriz fundamental es aquella que, dado un conjunto de correspondencias $x'_{i}\leftrightarrow x_{i}$, cumple que $x'_{i}Fx_{i}=0$ para todo $i$. Cada punto de correspondencia genera una ecuación linear para obtener las entradas de $F$, es posible llegar a una solución linear con 8 puntos.

### 2. Computation of the camera matrices
Las matrices de las cámaras son necesarias para reconstruir la posición 3D de los puntos. Estas se calculan a partir de la matriz fundamental siguiendo los siguientes pasos:
1. Se obtiene la matriz esencial a partir de la fundamental mediante la ecuación $E=k_{2}^{T}FK$ o desde las correspondencias de puntos con la ecuación $x´^{T}Ex=0$ con $x$ y $x'$ coordenadas normalizadas en las imágenes-
2. La matriz de la primera cámara por convenio se fija como $P=[I|0]$. Esta cámara está en el origen del sistema de coordenadas.
3. La matriz de la segunda cámara se expresa como $P'=[R|t]$ donde $R$ es la matriz de rotación y $t$ el vector de traslación. Para obtener $R$ y $t$ se descompone a $E$ en valores singulares (SVD). Por propiedades de $E$ sus dos primeros valores singulares son iguales, y se escalan a 1, mientras que el tercero es 0 por lo que la descomposición queda $E=U\begin{bmatrix}1&0&0\\0&1&0\\0&0&0\end{bmatrix}V^{T}$. Luego, $E$ se puede escribir como $E=SR$ donde $S$ codifica a $t$ y $R$ es la matriz de rotación. $S=U\begin{bmatrix}0&-1&0\\1&0&0\\0&0&0\end{bmatrix}U^{t}$ y $R=U\begin{bmatrix}0&-1&0\\1&0&0\\0&0&1\end{bmatrix}V^{T}$ o $R=U\begin{bmatrix}0&-1&0\\1&0&0\\0&0&1\end{bmatrix}^{T}V^{T}$
	Hay una ambiguedad de soluciones ya que hay dos posibles rotaciones y la traslación tiene una ambiguedad de signo, ademas la escala de $t$ tampoco se puede determinar mediante $t$. Es necesario elegir la decomposición correcta.

### 3. Triangulation
Dadas las matrices de las cámaras 