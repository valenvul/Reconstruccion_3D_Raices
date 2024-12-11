"Computer Vision: Algorithms and Applications" - Szeliski
Cap 12 y13.
[[Reunion 1]]

---
Pagina 754, tabla con datasets de imágenes stereo para usar
# Stereo Matching
Stereo matching is the process of takin two or more images and building a 3D model of the scene by finding matching pixels and converting the 2D positions into 3D depths. 

## Epipolar geometry
A pixel in one image $x_{0}$ projects to an epipolar line segment on the other image. This segment in bounded by the projection of the original viewing ray to infinity $p_{\infty}$ and by the projection of the original camera center $c_0$ to the other camera. This second projection is known as the epipole $e_{1}$. 
If we do the same process from the second camera to the first, we get another line, bounded by the other epipole, $e_{0}$, and by the projection of the pixel in the other image $x_{1}$. These lines define the intersection of the two image planes with the epipolar plane that passes through both camera centers and the point of interest.
![[epipolar geometry.jpg]]

The epipolar geometry of a pair of cameras is implicit in the relative pose and calibrations of the cameras and can easily be computed by  using the fundamental matrix.

Once the epipolar geometry is computed we want to finde the corresponding pixel in one image to the other. This can be done by first rectifying the input images so that the corresponding horizontal scanlines are epipolar lines (for cameras that are next to each other).