
# SfM
Structure from Motion. Utiliza el movimiento entre las imágenes para calcular la estructura tridimensional de la escena
- _Multiple View Geometry in Computer Vision_ de Richard Hartley y Andrew Zisserman
- _An Invitation to 3D Vision_ de Yasutaka Furukawa y Carlos Hernández
https://mi.eng.cam.ac.uk/~cipolla/publications/contributionToEditedBook/2008-SFM-chapters.pdf


## Metodos Secuenciales
Incorporan una vista sucesiva a la vez. Por cada vista se hace una reconstrucción parcial 
# MVS
Multi-view stereo. Usa las imágenes tomadas desde distintos puntos de vista para crear reconstrucciones densas.
- "Towards a taxonomy and benchmark for dense multi-view stereo" por Y. Furukawa y J. Ponce (2007).
- _Computer Vision: Algorithms and Applications_ de Richard Szeliski.
# Shape from Shading
Se basa en analizar cómo cambia la intensidad de la liz debido a la geometría de la superficie para reconstruir la forma 3D
- "Determining shape from shading" de B.K.P. Horn (1970).
- _Computer Vision: A Modern Approach_ de David Forsyth y Jean Ponce.
# Photometric Stereo
Utiliza multiples imágenes del mismo objeto tomadas bajo diferentes condiciones de iluminación para deducir su forma tridimensionalidad
- “Photometric method for determining surface orientation from multiple images” (1980).
- Zisserman y Szeliski
# ==Shape from Silhouette==
Análisis de siluetas de un objeto desde diferentes pintos de vista para reconstruir su forma tridimesional
- "Reconstructing a 3D object from its silhouettes in multiple views" de K. N. Kutulakos y S. M. Seitz (1998).
# Stereo Matching
Reconstruir profundidad y estructura 3D a partir de pares de imágenes
- “A Taxonomy and Evaluation of Dense Two-Frame Stereo Correspondence Algorithms” por Scharstein y Szeliski.
- _Multiple View Geometry in Computer Vision_.
# ==Visual hull==
Usando siluetas de un objeto desde múltiples vistas para crear una aproximación tridimensional del objeto. Este método no recupera los detalles cóncavos ta que solo reconstruye el casco.
- "Generalized cones and the interpretation of visual hulls" por **Aaron S. A. H. Horry y K. A. Ikeuchi** (1992)
- _Multiple View Geometry in Computer Vision_ de Richard Hartley y Andrew Zisserman.
- _An Invitation to 3D Vision: From Images to Geometric Models_ de Yasutaka Furukawa y Carlos Hernández
- _An Invitation to 3D Vision: From Images to Geometric Models_ de Yasutaka Furukawa y Carlos Hernández
# ==Space carving==
Refina el modelo 3D de un objeto eliminando parte del espacio que no pueden pertenecer al objeto basandose en restricciones fotométricas. Space carrving es capaz de reconstruir tanto regiones concavas convexas.

- "A Theory of Shape by Space Carving" por **S. M. Seitz y C. R. Dyer** (1999).
- _Computer Vision: Algorithms and Applications_ de Richard Szeliski.
- _Multiple View Geometry in Computer Vision_ de Hartley y Zisserman
- "Photo-consistency and Space Carving" por Kutulakos y Seitz (2000).

# Bibliografía general
- _Computer Vision: Models, Learning, and Inference_ de Simon J.D. Prince.
- _Vision Algorithms: Theory and Practice_ editado por Bill Triggs, Andrew Zisserman y Richard Szeliski.

---
### Comparación de los métodos:

| Método                       | Ventajas                               | Limitaciones                        | Aplicaciones                    |
|------------------------------|----------------------------------------|-------------------------------------|---------------------------------|
| SfM                          | No necesita calibración previa         | Nube de puntos dispersa             | Modelos 3D generales            |
| MVS                          | Alta densidad en la reconstrucción     | Computacionalmente costoso          | Escenas complejas               |
| Fotogrametría                | Alta precisión en grandes escenas      | Requiere buena calibración          | Arquitectura, arqueología       |
| Estereovisión                | Simple y rápido                        | No funciona bien en escenas complejas | Vehículos autónomos, robótica   |
| Nube de puntos               | Detalles precisos                      | Puede generar ruido                 | Modelos detallados              |
| Fotometría Estéreo           | Captura detalles finos                 | Requiere iluminación controlada     | Escaneo de objetos pequeños     |

### **Resumen Comparativo de Ventajas y Desventajas MVS:**

| **Ventajas**                                          | **Desventajas**                                           |
|-------------------------------------------------------|-----------------------------------------------------------|
| Alta densidad y precisión en la reconstrucción         | Computacionalmente costoso                                |
| Flexibilidad: se puede aplicar a objetos pequeños y grandes | Requiere imágenes con buena superposición                 |
| Uso eficiente de múltiples vistas                     | Sensible a texturas y características de la superficie     |
| Compatible con SfM para mejorar la reconstrucción      | Ruido en la reconstrucción, necesita postprocesamiento     |
| Buena para capturar geometría general                  | Problemas con oclusiones y superficies lisas              |


| **Criterio**              | **Multi-view Stereo (MVS)**              | **Visual Hull**                    |
|---------------------------|------------------------------------------|------------------------------------|
| **Nivel de detalle**       | Alto: Captura detalles finos y texturas  | Bajo: Solo captura la geometría general |
| **Computacionalmente**     | Costoso, requiere más tiempo             | Rápido y eficiente                 |
| **Dependencia de textura** | Requiere texturas o características      | No depende de textura, solo siluetas |
| **Escenas complejas**      | Maneja geometrías complejas              | Dificultad con objetos cóncavos    |
| **Condiciones de captura** | Necesita muchas imágenes con solapamiento | Necesita fondo uniforme para siluetas |
| **Ruido**                  | Posible si las condiciones no son óptimas | Menos ruido, pero menos detalle    |

### **Herramientas y Software Común para MVS**

- **COLMAP**: Una herramienta popular de código abierto para SfM y MVS que permite generar nubes de puntos densas y modelos 3D detallados.
- **OpenMVG + OpenMVS**: Una combinación que primero genera una nube de puntos dispersa con SfM y luego densifica usando MVS.
- **Agisoft Metashape**: Software comercial muy utilizado para fotogrametría que incluye MVS como parte de su flujo de trabajo.
- **Meshroom**: Otro software de código abierto que facilita todo el proceso de reconstrucción, desde SfM hasta MVS y texturización.