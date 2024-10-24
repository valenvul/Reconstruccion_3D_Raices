[[Reconstrucción 3D de raíces]]
Fecha de Reunion: 17/09/24

---
## Objetivo:
Presentar una overview de los mecanismos de reconstrucción existentes

## Notas
- [[Algoritmos de reconstruccion]]
- [[A Comparison and Evaluation of Multi-View Stereo Reconstruction Algorithms]]
- [[A Survey of Methods for Volumetric Scene Reconstruction from Photographs]]
- [[Algorithms, From Photo-Consistency to 3D Reconstruction]]

Resumen: [[Métodos de reconstrucción volumétrica de escena]]

Evaluar algoritmos para cámaras monoculares y cámaras Stereo. Hacer breve resumen de cada metodología con sus pros y contras (fidelidad a la geometria simplicidad etc.)

### Proyectos de reconstruccion
- [Colmap](https://colmap.github.io)
- [CMVS](https://www.di.ens.fr/cmvs/)
- https://prs.igp.ethz.ch/research/projects/gipuma.html
- [Open MVS](https://github.com/cdcseacave/openMVS?tab=readme-ov-file)
- [Open MVG](https://github.com/openMVG/openMVG)
### Bibliografia
- [Visual Hull](http://cs.harvard.edu/~sjg/papers/623.pdf)
- https://www.researchgate.net/publication/339009396_A_Review_on_3D_Reconstruction_Techniques_from_2D_Images
- https://carlos-hernandez.org/papers/fnt_mvs_2015.pdf

## TO DO
- [x] Completar resumen del paper en notion
- [ ] Hacer un buen resumen de los algoritmos en base a el survey y el libro de hernandez

---
# Devoluciones
Se decidió usar un tanque cuadrado. Vamos a probar con cámaras monoculares y stereo y decidir cual es conveniente. También hay que hacer pruebas para determinar si es suficiente reconstruir en base a las triangulaciones de pointclouds o es necesario usar siluetas.

Para la próxima reunión Implementar una calibración y detección de la posición de las cámaras en vase al siguiente repo.
[https://github.com/nburrus/stereodemo](https://github.com/nburrus/stereodemo)