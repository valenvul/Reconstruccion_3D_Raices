[[Reunion 4]]

---



> [!NOTE] Matriz intrínseca
> Toma puntos 3D en el sistema de coordenadas de la cámara y los proyecta al plano de la imagen, a coordenadas dadas en pixel.
> $K=\begin{bmatrix}f_{x}&0&c_{x}\\0&f_{y}&c_{y}\\0&0&1\end{bmatrix}$

> [!NOTE] Matriz extrínseca
> Transforma de un sistema de coordenadas a otro, por ejemplo del del mundo al de la cámara
> $P_{c} = R\times P_{w}+t$
> La matriz se define como $[R|t]$
> 

> [!NOTE] Matriz Esencial
> Describe la relación entre puntos en coordenadas normalizadas para dos cámaras calibradas.
> Cumple la ecuación $x_{2}^{T}Ex_{1}=0$ y se define como $E=T_\times R$ donde $T_\times$  es la matriz antisimétrica asociada a $t$.
> Otra forma de calcular $E$ es mediante la cuenta $E=K'^{T}FK$ donde $F$ es la matriz fundamental y $K$ y $K'$ son las matrices intrínsecas de las cámaras.

> [!NOTE] Matriz Fundamental
> Es la matriz que describe la relación entre puntos de la imagen dados en coordenadas de pixel y no requiere que las cámaras estén calibradas.
> Su ecuación principal es $p_{2}^{T}Fp_{1}=0$ y se define como
> $F = K_{2}^{-T}EK_{1}^{-1}$ donde $K_{1}$ y $K_{2}$ son las matrices intrínsecas de la cámaras


# Modelo de cámara
En un modelo de cámara pinhole sin distorsión la siguiente transformación proyectiva define la relación entre un pixel en la imagen y un punto definido según las coordenadas del mundo$$p=A[R|t]P_{w}$$
- $P_{w}$ es el punto 3D expresado en coordenadas del mundo
- $p$ es una pixel de la imagen expresado en 2D
- $A$ es la matriz intrínseca de la cámara
- $R$ es la matriz de rotación
- $t$ es el vector de traslación

$R$ y $t$ describen el cambio de coordenadas del sistema de coordenadas de la cámara a coordenadas del mundo.

La matriz intrínseca de la cámara proyecta puntos 3D dados en las coordenadas de la cámara a coordenadas de pixel. $p=AP_{c}$. Esta matriz se compone de focal length, expresado en unidades de pixel, y el centro de la cámara $$A=\begin{bmatrix}f_{x}&0&c_{x}\\0&f_{y}&c_{y}\\0&0&1\end{bmatrix}$$ y  por ende la ecuación de antes queda como
$$\begin{bmatrix}u\\v\\1\end{bmatrix}=\begin{bmatrix}f_{x}&0&c_{x}\\0&f_{y}&c_{y}\\0&0&1\end{bmatrix}\begin{bmatrix}X_{c}\\Y_{c}\\Z_{c}\end{bmatrix}$$

La matriz de rotación traslación es la matriz producto de la transformación proyectiva y la transformación homogénea. La matriz de transformación proyectiva lleva los puntos en 3D representados en las coordenadas de la cámara a puntos 2D en el plano de la imagen representados en las coordenadas de la cámara normalizadas. $x´=X_{c}/Z_{c}$ y $y'=Y_{c}/ Z_{c}$
$$Z_{c}\begin{bmatrix}x'\\y'\\1\end{bmatrix}=\begin{bmatrix}1&0&0&0\\0&1&0&0\\0&0&1&0\end{bmatrix}\begin{bmatrix}X_{c}\\Y_{c}\\Z_{c}\\1\end{bmatrix}$$
La matriz de transformación homogénea está compuesta por los parámetros extrínsecos en $R$ y $t$ representa el cambio de base de coordenadas del sistema de mundo a coordenadas de sistema de la cámara. Dadas las coordenadas de un punto en el mundo, obtenemos sus coordenadas en la cámara con la ecuación $$P_{c}=\begin{bmatrix}R & t\\0&1\end{bmatrix}P_{w}$$Combinando las matriz de transformación proyectiva con la homogénea  conseguimos la transformación que mapea los puntos 3D del mundo a puntos 2D en el plano de la imagen u coordenadas del sistema de la cámara normalizadas.

De esta forma podemos escribir la ecuación del comienzo como $$\begin{bmatrix}u\\v\\1\end{bmatrix}=\begin{bmatrix}f_{x}&0&c_{x}\\0&f_{y}&c_{y}\\0&0&1\end{bmatrix}[R|t]\begin{bmatrix}X_{w}\\Y_{w}\\Z_{w}\end{bmatrix}$$![[Screenshot 2024-12-05 at 16.00.34.jpg]]



https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html

# Calibración
Los lentes de verdad suelen tener distorsión por lo que se extiende el modelo. La distorsión radial queda definida por 6 coeficientes y la tangencial por 2. La distancia focal es multiplicada por una combinación de estos parámetros. Este es el modelo que se usa para calibrar la cámara

La función de calibración estima la matriz intrínseca para cada cámara, los coeficientes de distorsión, la matriz de rotación y de traslación entre las cámaras, la matriz esencial y la matriz fundamental.

Cada cámara se calibra primero de manera independiente para obtener sus parámetros intrínsecos y de distorsión. Para esto se usa un patron conocido, el cual se detecta en una cantidad de imágenes para obtener asi correspondencias de puntos. Se estiman los parametros mediante metodos lineales y luego se usa una oprimizacion  usando minimos cuadradis para minimizar el error reproyectivo.

Después se calcula la relación estéreo. La rotación y la traslación se estiman minimizando el error reproyectivo. 
Error reproyectivo=$\sum_{i=1}^{N}||p_{1}-\hat p_{1}||^{2}+||p_{2}-\hat p_{2}||^{2}$
donde $p_1$ y $p_2$ son las coordenadas reales en las imágenes y $\hat p_{1}$ y $\hat p_2$ las reproyectados com los parámetros del momento.

También se calcula la matriz esencial, y fundamental:
- La matriz esencial define la relación entre puntos en coordenadas normalizadas de cámaras calibradas. Su ecuación principal es $x_{2}^{T}Ex_{1}=0$ donde:
	- $x_{1}$, $x_{2}$ son puntos normalizados es decir, sin los efectos de los parámetros intrínsecos de la cámara
	- $E$ es la matriz esencial de $3\times3$
	La matriz esencial se calcula como $E=T\times R$ siendo $R$ la matriz de rotación entre las cámaras y $T_{\times}$ la matriz antisimétrica asociada al vector de traslación definida como: $T_{\times}=\begin{bmatrix}0&-t_{z}&t_{y}\\t_{z}&0&-t_{x}\\-t_{y}&t_{x}&0\end{bmatrix}$

- La matriz fundamental describe la relación entre puntos de la imagen dados en coordenadas de pixel y no requiere que las cámaras estén calibradas.
	Su ecuación principal es $p_{2}^{T}Fp_{1}=0$.
	Si las cámaras ya están calibradas se calcula a partir de la matriz esencial y las matrices intrínsecas de las cámaras con la ecuación $F=k_{2}^{T}EK_{1}^{-1}$.
	Si no, se calcula usando correspondencias de puntos entre las imágenes.

https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html

# Rectificación
Una vez que tienes RR y TT, las imágenes se "rectifican", es decir, se transforman para que los epipolos queden alineados horizontalmente. Esto simplifica el cálculo de la disparidad y permite generar la nube de puntos 3D.

`cv2.stereoRectify` usa las matrices intrinsecas y extrinsecas de las c'amaras para calcular las trandformaciones necesarias para alinear las imagenes estereo. Tambien calcula Q, la matriz de reproyección 3d.
$p_{1}= K_1[I|0]$(por convencion) $p_2=K_2[R|T]$
# Calculo de pose
En la calibración inicial se calcula la relación entre la cámara izquierda y la derecha. En este proceso se obtiene la rotación y traslación relativa que tienen las cámaras del par estereo entre si.

Luego, para cada par de imágenes se calcula la posición global de la cámara que las tomó. Dado que tenemos un patrón conocido en todas las imágenes, podemos definir su posición en el mundo y así tener una correlación en cada imagen entre la posición en el mundo (3D) y la posición en la imagen (su proyección 2D). Esto se hace resolviendo la ecuación $$p_{i}= K[R|T]X_{i}$$
donde:
- $X_{i}=[X,Y,Z,1]^T$ son las coordenadas homogéneas de un punto en en las coordenadas del mundo. (conocido)
- $p_i=[u,v,1]^T$ Son las coordenadas homogéneas de la proyección del punto en la imagen. (en píxeles) (conocido)
- $K$ es la matriz intrínseca de la cámara: $\begin{bmatrix}f_{x}&0&c_{x}\\0&f_{y}&1\end{bmatrix}$ (calculado en la calibración)
- $R$ es un matriz de $3\times 3$ de rotación que orienta el sistema de coordenadas global al sistema de coordenadas de la cámara.
- $T$ es el vector de traslación de $3\times 1$ que representa el desplazamiento del origen global al origen de la cámara

La idea de la ecuación es proyectar el punto 3D ($X_i$) al plano de la imagen mediante dos transformaciones:
1. Una extrínseca mediante la matriz $[R|T]$ que cambia pasa las coordenadas globales del punto a las coordenadas de la cámara mediante la ecuación $X_{i}^{cam}= R\cdot X_{i}+T$.
2. Una intrínseca mediante la matriz $K$ que convierte las coordenadas de la cámara (en 3D) $[X',Y',Z']^{T}$ a coordenadas de la imagen (en 2D) $[u,v]^{T}$
---
El calculo de la pose se hace con `cv2.solvePnP`. busca estimar la posición y orientación de un objeto con respecto a la cámara. 
$X_i=[X,Y,Z,1]^T$ y su proyección en la imagen es $x_{i}=[u,v,1]^T$. $x_{i}=K[R|t]X_{i}$. 
`solvePnP` busca minimizar el error reproyectado. en el codigo se usa el metodo iterativo para mejorar dicha estimación.

`cv2.Rodrigues` convierte el vector de rotación que devuelve `solvePnP` en una matriz de rotación. el vector de rotación represente un eje de rotación y un ángulo de rotación.

Luego se construye la matriz de transformación homogenea que convierte los puntos expresados en coordenadas del mundo al sistema de coordenadas de la cámara. Luego calcula su matriz inversa que permite transformar los puntos expresados en sistemas de coordenadas de la cámara al sistema de coordenadas del objeto.
# Calculo de disparidad
La disparidad mide la diferencia en la posición horizontal de la proyección de un punto a la cámara izquierda y derecha de un par stereo. La disparidad esta inversamente relacionada con la profundidad del punto en 3D con la ecuación $Z=\frac{f\cdot b}{\text{disparidad}}$ donde f es la distancia focal de la cámara en pixeles y b la baseline de las cámaras.
Una vez calculada la profundidad se obtienen las coordenadas 3D del sostema de referencia de la cámara mediante las ecuaciones $X= \frac{(x−c_{x})\cdot Z}{f},Y=\frac{(y−c_{y})\cdot Z}{f}$ 

CREStereo es un algoritmo de deep learning para calcular la disparidad en escenarios estereo. Busca las correspondencias entre pixeles de las imágenes del par y luego las optimiza para garantizar consistencia y precision, Devuelve un mapa que indica la disparidad en cada pixel.

Las coordenadas X e Y en el espacio 3D en base al mapa de disparidad se cualculan como $X=\frac{(u-c_{x})\cdot Z}{f}$ e $Y=\frac{(v-c_{y})\cdot Z}{f}$.
La matriz Q (que se calcula en el proceso de rectificación de las imágenes) permite convertir los puntos del espacio imagen al espacio 3D. $\begin{bmatrix}X\\Y\\Z\\W\end{bmatrix}=Q\begin{bmatrix}u\\v\\d\\1\end{bmatrix}$. Esta matriz se construye en base a los parámetros intrínsecos, la baseline y las características geométricas del sistema estereo.
# Generación de nube de puntos
