# 4. Transformaciones proyectivas en 2D

# 7. Computation of the camera matrix
La matriz de la cámara no es más que una matriz de proyección de puntos en el espacio 3D a su correspondiente en la entidad de una imagen. Para que este mapeo sea lineal es necesario que la imagen no tenga distorsión radial, así como conocer los parámetros intrínsicos de la cámara.

La matriz $P$ es una transformación que, dado $X$ un punto en el mundo real y $x$ su correspondiente en la imagen,  $x=PX$. Para cada correspondencia conocida, se deriva la siguiente relación: $$\begin{bmatrix}0^{T} &-w_{i}X_{i}^{T}& y_{i}X_{i}^{T} \\ w_{i}X_{i}^{T}&0^{T}&-x_{i}X_{i}^{T}\\ -y_{i}X_{i}^{T}&x_{i}X_{i}^{T} & 0^{T}\end{bmatrix} \begin{pmatrix}P_{1}\\p_{2}\\ P_{3}\end{pmatrix} = 0$$

# 14. Affine Epipolar Geometry
