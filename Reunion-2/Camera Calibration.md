[[Reunion 2]]
fuente: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html

---

## Distorsiones
Algunas cámaras introducen distorsiones significantes en las imágenes. Hay dos tipos de distorsiones principales:
- *Radial:* Causa que las lineas rectas aparezcan curvas. Se vuelve peor cuanto más lejos se encuentran estas del centro de la imagen. $$\begin{matrix}x_{\text{distorted}}=x(1+k_{1}r^{2}+k_{2}r^{4}+k_{3}r^{6})\\y_{\text{distorted}}=y(1+k_{1}r^{2}+k_{2}r^{4}+k_{3}r^{6}) \end{matrix}$$
- *Tangencial:* Ocurre cuando el lente que saca la imagen no esta alineado perfectamente paralelo al plano de la imagen por lo que algunas áreas de la imagen pueden aparecer más cerca de lo que realmente están. $$\begin{matrix}x_{\text{distorted}}=x+[2p_{1}xy+p_{2}(r^{2}+2x^{2})]\\y_{\text{distorted}}=y+[p_{1}(r^{2}+2y^{2})+2p_{2}xy] \end{matrix}$$
Para definir la distorsión tenemos que encontrar los 5 parámetros que aparecen en las ecuaciones, $(k_{1},k_{2},p_{1},p_{2},k_{3})$
## Parámetros de la cámara
Los parámetros *intrínsicos* de la cámara son aquellos específicos de la cámara, es decir el foco ($f_x,f_y$) y el centro óptico ($c_x,c_y$). Con estos se crea una matriz de la cámara, que puse usarse para remover la distorsión generada por el lente particular de la cámara. Una vez calculada esta matrix puede ser reusada para todas las imágenes sacadas por la cámara. $$\begin{bmatrix}f_{x} & 0 & c_{x}\\0& f
_{y}&c_{y}\\0&0&1\end{bmatrix}$$
Los parámetros *extrínsicos* corresponen a los vectores de rotación y traslación que indican las coordenadas del sistema.

# Calibración
Previo a analizar imágenes stereo es necesario lidiar con estas distorsiones. Para esto es necesario sacar algunas imágenes de un patron definido como puede ser un tablero de ajedrez. Tomamos alguna parte de la que sepamos la posición relativa, como por ejemplo las esquinas que sabemos que deben estar perpendiculares. Sabiendo las posiciones de estos en el mundo real y sus coordinadas en la imagen se puede resolver para encontrar los coeficientes de distorsión. 
Para los mejores resultados se necesitan al menos 10 patrones de test.
Imágenes de prueba en openCV (samples/data/left01.jpg-left14.jpg)

## Código
El input importante que necesitamos es el conjunto de puntos 3D del mundo real que le corresponden a los puntos 2D de interés en la imagen. Para conocer los puntos podemos decir que el patrón se mantuvo siempre quieto en un plano y se movió la cámara. Ahora simplemente se pueden mandar valores que representan los puntos de la imagen. Para tenerlos a escala real es necesario saber la distancia entre los puntos.
Por ejemplo en el tablero de ajedrez, si tomamos los puntos como los lugares en los que se tocan dos cuadrados negros, y sabemos que el tamaño de cada cuadrado es de 30mm, en vez de pasar$(1,0),(2,0),...$ pasamos $(30,0),(60,0),...$ y conseguimos los resultados en mm.

Para encontrar el patron en la tabla de ajedrez se usa la función `cv.findChessboadCorners()`. Además hay que pasarle que tipo de patrón se está usando, es decir, una grilla de 5x5, 8x8, etc. La función devuelve los puntos de las esquinas y `retval=true` si se consiguió el patron. Los puntos se encuentran de izquierda a derecha y de arriba a abajo.

Si se quiere usar otro patrón se puede usar una grilla circular con la función `cv.findCirclesGrid()`. Con este patron se necesitan menos imágenes para una calibración exitosa.

``` Python
import numpy as np
import cv2 as cv
import glob

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('*.jpg')

for fname in images:
	img = cv.imread(fname)
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	# Find the chess board corners
	ret, corners = cv.findChessboardCorners(gray, (7,6), None)

	# If found, add object points, image points (after refining them)
	if ret == True:
		objpoints.append(objp)
		
		corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
		imgpoints.append(corners2)

		# Draw and display the corners
		cv.drawChessboardCorners(img, (7,6), corners2, ret)
		cv.imshow('img', img)
		cv.waitKey(500)

cv.destroyAllWindows()
```

Este código encuentra todos los puntos de la imagen. Con esto, se puede empezar la calibración. Para esto se puede usar la función `cv.calibrateCamera()` que devuelve la matriz de la cámara, los coeficientes de distorsión, los vectores de rotación y traslación, etc.

Una vez calculados los parámetros se puede agarrar una imagen y sacarle la distorsión. Primero hay que refinar la matriz de la cámara basando es un parámetro de crecimiento libre usando `cv,getOptimalNewCameraMatrix()`. Si el parámetro es 0 devuelve la imagen sin distorsión y con la cantidad minima de pixels no deseados, por lo que puede reducen algunos pixels en las esquinas de las imágenes. Si el parámetro es 1, se retienen todos los pixeles de la imagen.

Para sacar la distorsión openCV provee dos funciones `cv.undistort()`, que es la más simple y usa el ROI resultante de la función anterior o usando `cv.initUndistortRectifyMap()` y `cv.remap()`. Esta forma es más difícil, primero encuentra una función de mapeo de la imagen distorsionada a la no distorsionada y después usa una función de remapeo.

Luego se puede almacenar la matriz de la cámara y los coeficientes de distorsión para usos futuros.

## Error de reproyección
Esta medida de error da una estimación de que tan exactos son los parámetros encontrados. Cuanto más cercano a 0 más exactos fueron los parámetros encontrados. Para encontrarlo se usa el siguiente código:
```Python
mean_error = 0

for i in range(len(objpoints)):

imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)

error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)

mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )
```