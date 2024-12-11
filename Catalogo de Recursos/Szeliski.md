# 12. Depth Estimation
*Stereo matching* es el proceso de, dadas dos o más imágenes, crear un modelo 3d de la escena encontrando los pixeles que matchean en las imágenes y convirtiendo sus posiciones 2d en profundidades.
((Leer [[Szeliski#11]] para entender el cálculo de las posiciones de cámaras y una reconstrucción poco densa de escenas)).

El término *disparidad* se refiere al movimiento horizontal que hay entre lo que observan los dos ojos o un par de imágenes stereo. Esta disparidad es inversamente proporcional a la distancia que tiene el observador del objeto. 

## Epipolar Geometry
Las fotografías stereo proveen información extra, como las posiciones y calibración de las cámaras que tomaron la imagen de la misma escena estática, que facilita la búsqueda de la correspondencia de pixeles entre imágenes.

Un pixel ($x_0$) en una imagen de un par stereo se proyecta a un segmento de una *linea epipolar* en la otra imagen del par. Este segmento está delimitado en una punta por la proyección del rayo de visión del pixel en la cámara 1 al infinito ($p_\infty$), y en la otra punta por la proyección del centro de la cámara original ($c_0$) al de la cámara de la otra imagen ($c_1$). Los puntos en los que estos centros se proyectan en la imagen opuetsa se llaman *epipolos* ($e_0$ y $e_1$).

Ahora, tomando un punto de esta linea epipolar de la segunda imagen y proyectandolo hacia la primera, se consigue una nueva linea epipolar que esta delimitada por la proyección de este rayo de visión al infinito y por el epipolo de la primera imágen. 

Este par de lineas epipolares indican la intersección de los planos de las imágenes con el *plano epipolar* que paso tanto por los centros de las cámaras como por el punto de interés ($p$).

![[epipolar geometry.jpg]]

### Rectification
La geometría epipolar queda implícita en la pose relativa y calibración de las cámaras. Dados las suficientes correspondencias de pixeles es fácil calcular dicha geometría. Una vez obtenida las lineas epipolares facilitan la búsqueda de nuevas correspondencias al limitar el campo de búsqueda para estas.

Se puede conseguir un algoritmo eficiente para calcular estas correspondencias si se rectifican las lineas epipolares, de manera que las lineas de escaneo horizontal se correspondan con las lineas epipolares. Es decir, que los segmentos epipolares en cada imagen se conviertan en segmentos de una misma linea.

### Plane sweep
Una alternativa a la rectificación

## Sparse Correspondance
Los algoritmos de matcheo originales usaban extracción de características. Primero se determinaban posibles puntos de interés donde alinear las imágenes, y luego se buscaban las posibles ubicaciones correspondientes en el resto de las imágenes usando busqueda por parches. Esto no solo se hacía por las limitaciones computacionales del momento sino que además de esta forma se limitaban las respuestas a las que tenían la mayor certeza. Esto producía correspondencias escasas que luego se interpolaban usando algoritmos de  ajuste de superficie.
Más recientemente estas características se usan como semillas para encontrar correspondencias adicionales.
## ...
## Multiview stereo


# Bibliografía interesante
1. Poggi, M., Tosi, F., Batsos, K., Mordohai, P., and Mattoccia, S. (2021). On the synergies between machine learning and binocular stereo for depth estimation from images: a survey. IEEE Trans- actions on Pattern Analysis and Machine Intelligence, (accepted)().
2. Geiger, A., Lenz, P., and Urtasun, R. (2012). Are we ready for autonomous driving? The KITTI vision benchmark suite. In IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR).