Autor Szeliski. El paper lo saque de su libro que recomendo gaston. Es de 2006. Puede haber metodologias más novedosas. Aunque las tecnicas esten desactualizadas sirven los datasets.

https://vision.middlebury.edu/mview/seitz_mview_cvpr06.pdf
---
# Mediciones
- ==Scene Representation==. Miden la representación que se tiene del modelo 3D. Esta puede ser:
	- 3D grid (voxels, level-sets). Simple, uniforme y capaz de aproximar cualquier superficie
	- Polygon Meshes. Eficientes para almacenar y render. Sirven para la computaciones de visibilidades.
	- Depth Maps. Permite evitar samplear reiteradas veces la geometría 3D. Sirve para data sets pequeños.
- ==Photo-consistency==. Mide la compatibilidad visual de una reconstrucción con un conjunto de imágenes de entrada.
- ==Visibility model==. Especifican que vistas considerar cuando se evalua la photo-consistency. Ayudan a lidiar con la oclusion y los cambios de visibilidad entre imagenes del dataset.
- ==Shape prior==. Se usan para mejorar la geometría. No son tan importantes en multi-view stereo.
- ==Algoritmo de reconstruccion==. 
	Hay cuatro "clases":
	- Computar una función de pérdida en un volumen 3D e ir sacandole superficie.
	- Iterativamente ir cambiando una superficie para minimizar la función de pérdida. (Space carving)
	- Computan los depth maps. Enfuerzan restricciones de consistencia entre los diferentes mapas o los mezclan en una escena 3D en post procesamiento.
	- Primero se calculan los feature points y despues le calculan una superficie que se amolde a dichos puntos.
- ==Requqerimientos de inicialización.== El procesamiento necesario para pasar de imagen original a la entrada del algoritmos

# Algoritmos
## Furukawa et al. 
Y. Furukawa and J. Ponce. High-fidelity image-based mod- eling. Technical Report 2006-02, UIUC, 2006.

Usan stereo matching para encontrar las coordenadas de los feature points. Después van achicandp un modelo de visual hull para que los puntos queden en su superficie. Por último refinan el resultado usando minimización de energía.
## Goesel et al.
M. Goesele, B. Curless, and S. Seitz. Multi-view stereo re- visited. In CVPR, 2006.

Computan un depth map para cada viewpoint y mezclan los resultados usando VRIP.
## Hernandez and Schmitt
 C. Hernandez and F. Schmitt. Silhouette and stereo fusion for 3D object modeling. CVIU, 96(3):367–392, 2004.
 
Computan el depth map de cada viewpoint y los mezclan en un volumen de costo. Despues iterativamente deforman un mesh que es inicializado como el vosual hull, para encontrar la superficie de minimo costo en el volumen calculado. También incluyen términos para adecuarse a las siluetas.
## Kolmogorov and Zabih
V. Kolmogorov and R. Zabih. Multi-camera scene recon- struction via graph cuts. In ECCV, vol. III, pp. 82–96, 2002.

Computan un conjunti de depth maps usando multi-baseline stereo con graph cuts. Después mezclan los resultados en voxel volume computando la interseccion de los volumenes ocluidos de cada viewpoint.
## Pons, Keriven and Faugeras
 J.-P. Pons, R. Keriven, and O. Faugeras. Modelling dynamic scenes by registering multi-view image sequences. In CVPR, vol. II, pp. 822–827, 2005.
Computan la superficie de minimo costo evolucionando una superficie en un level set framework usando una medición de predicción de error.
## Vogiatzis, Torr and Cipolla
G. Vogiatzis, P. Torr, and R. Cipolla. Multi-view stereo via volumetric graph-cuts. In CVPR, pp. 391–398, 2005.

Computan la correlación costo volumen cerca del visual hull. Computan la superficie de minimo costo usando min-cut volumétrico.

# Resultados
![[Comparación de algoritmos de reconstrucción.jpg]]

# Bibliografia
1. C. Dyer. Volumetric scene reconstruction from multiple views. In L. S. Davis, editor, Foundations of Image Understanding, pp. 469–489. Kluwer, 2001.
2.  G. Slabaugh, B. Culbertson, T. Malzbender, and R. Shafer. A survey of methods for volumetric scene reconstruction from photographs. In Intl. WS on Volume Graphics, 2001.
3. R. Szeliski and P. Golland. Stereo matching with transparency and matting. IJCV, 32(1):45–61, 1999.
4. S. Seitz and C. Dyer. Photorealistic scene reconstruction by voxel coloring. IJCV, 35(2):151–173, 1999.
5. P. Eisert, E. Steinbach, and B. Girod. Multi-hypothesis, volumetric reconstruction of 3-D objects from multiple calibrated camera views. In ICASSP 99, pp. 3509–3512, 1999.
6. K. Kutulakos and S. Seitz. A theory of shape by space carvng. IJCV, 38(3):199–218, 2000.
7. T.BonfortandP.Sturm.Voxel carving fors pecular surfaces. In ICCV, pp. 591–596, 2003.
8. G. Slabaugh, B. Culbertson, T. Malzbender, and M. Stevens. Methods for volumetric reconstruction of visual scenes. IJCV, 57(3):179–199, 2004. 
9.  H. Jin, S. Soatto, and A. Yezzi. Multi-view stereo reconstruction of dense shape and complex appearance. IJCV, 63(3):175–189, 2005.
10.  A. Rockwood and J. Winget. Three-dimensional object reconstruction from two-dimensional images. ComputerAided Design, 29(4):279–285, 1997.
11. J.Isidoro and S.Sclaroff. Stochastic refinement of the visual hull to satisfy photometric and silhouette consistency con- straints. In ICCV, pp. 1335–1342, 2003.
12. R. Szeliski. A multi-view approach to motion and stereo. In CVPR, vol. 1, pp. 157–163, 1999.
13. S. Savarese, H. Rushmeier, F. Bernardini, and P. Perona. Shadow carving. In ICCV, pp. 190–197, 2001.
14. A. Laurentini. The visual hull concept for silhouette-based image understanding. TPAMI, 16(2):150–162, 1994.
15. S. Sinha and M. Pollefeys. Multi-view reconstruction using photo-consistency and exact silhouette constraints: A maximum-flow formulation. In ICCV, pp. 349–356, 2005.
16. H. Saito and T. Kanade. Shape reconstruction in projective grid space from large number of images. In CVPR, vol. 2, pp. 49–54, 1999.
17. G. Slabaugh, T. Malzbender, B. Culbertson, and R. Schafer. Improved voxel coloring via volumetric optimization. TR 3, Center for Signal and Image Processing, 2000.
18. J.-Y. Bouguet. Camera calibration toolbox for Matlab. https://data.caltech.edu/records/jx9cx-fdh55