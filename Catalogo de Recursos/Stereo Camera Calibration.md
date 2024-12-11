fuente: https://www.youtube.com/watch?v=hUVyDabn1Mg

---
Dada una imagen calibrada es imposible conocer las coordenadas 3D de un pixel de la imagen. Lo que si se sabe es que dicho punto debe encontrarse sobre el rayo que sale desde el plano de la imagen y pasa por dicho pixel. Los mapeos se calculan de la siguiente manera 
$$\underset{\text{(punto)}}{\text{3D a 2D: }}\,\,\begin{matrix}u=f_{x} \frac{x_{c}}{z_{c}}+o_{x}\\v=f_{y} \frac{y_{c}}{z_{c}}+o_{y}\end{matrix}$$
$$\underset{\text{(rayo)}}{\text{2D a 3D: }}\,\,\begin{matrix}x=\frac{z}{f_{x}}(u-o_{x})\\y=\frac{z}{f_{y}}(v-o_{y})\\z>0\end{matrix}$$
Teniendo una cámara que es exactamente igual a la original pero que captura la foto con cierto desplazamiento horizontal, se puede calculas la posición del punto 3D. Esto se llama un sistema de cámaras estereo. La distancia entre ambas cámaras en el eje $x$ se llama *baseline*.

Detectando el mismo pixel en la nueva imagen y calculando el rayo al que proyecta, se puede tomar la intersección de ambos rayos para conocer la posición del punto en el espacio. Esto se llama *triangulación*.

![[Screenshot 2024-12-11 at 12.46.47.jpg]]


Con este sistema, se pueden conseguir las coordenadas del punto $$\begin{matrix}x=\frac{b(u_{l}-0_{x})}{(u_{l}-u_{r})}&y=\frac{bf_{x}(v_{l}-o_{y})}{f_{y}(u_{l}-u_{r})}&z=\frac{bf_{x}}{(u_{l}-u_{r})}\end{matrix}$$
La diferencia entre las coordenadas $u$ de los puntos en las imágenes se llama *disparidad*. Como podemos ver por la ecuación para $z$, la disparidad es inversamente proporcional a la profundidad del punto. Además la disparidad es proporcional al baseline.

Como la diparidad solo ocurre en el eje $x$ para buscar puntos de correspondencia entre las imágenes solo es necesario escanear en lineas horizontales.
