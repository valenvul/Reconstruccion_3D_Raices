Paper: [[Detailed_reconstruction_of_3D_plant_root_shape.pdf]]

---
Images are $1.600 \times 1.200$ and they take about $40$ images.

1. model the background of each image as a harmonic function, which facilitates the extraction of the silhouette by adaptive thresholding
2. Visual hull. Adding a restriction to satisfy one particular image. This helps to reconstruct delicate structures.
3. *Persistent Homology* [1] to guarantee the connectedness of the 3D reconstruction.

Visual hull or volumetric carving finds the largest shape consistent with the input silhouettes or colors images, but thin features of the shape are likely to be lost.

Imaging using coplanar shadowgrams [2]

[1] H. Edelsbrunner, D. Letscher, and A. Zomorodian. Topological persistence and simpliﬁcation. Discrete & Computational Geometry, 28(4):511–533, 2002

[2] S. Yamazaki, S. G. Narasimhan, S. Baker, and T. Kanade. Coplanar shadowgrams for acquiring visual hulls of intricate objects. In ICCV, pages 1–8, 2007

## Harmonic background subtraction
The image is modeled as a function of intensities $J:\Omega\rightarrow[0,255]$, where $\Omega$ is the image grid. The root is interpreted as the foreground and the rest as the background. Then it is normalized
$I: \Omega\rightarrow[0,1]$ defined as:$$I(x,y)=\frac{\sum_{i=0}^{J(x,y)}h[i]}{\sum_{i=0}^{255}h[i]}$$
where $h[i]$ is the number of pixels with intensity $i$.
This normalized intensity will be the input to the algorithm.
The background is then approximated by a harmonic function $B:\Omega\rightarrow[0,1]$. The borders of the image are set to the actual intensity $B(x,y)=I(x,y)$ on the boundary and for the interior of the image they enforce $\Delta B=\frac{\partial^{2}B}{\partial x^{2}}+\frac{\partial^{2}B}{\partial y^{2}}=0$.
This can be done because the background values vary smoothly and there are no local extrema.

To construct the foreground they use the difference between the intensity of the image and the harmonic background. The foreground is therefore enhanced and hysteresis thresholding [3] can be applied with greater results.

[3] J. Canny. A computational approach to edge detection. IEEE Trans. Pattern Anal. Mach. Intell., 8(6):679C698, 1986

## Regularized Visual Hull
Let $I_{k}$ be the $k$-th image of a plant root. For a set $V$ of voxels in 3D, let $\pi_{k}(V)\subseteq\Omega_{k}$ be it's projection to a set of pixels in the $k$-th image. We write $\mathcal{F}_{k}\subseteq\Omega_{k}$ for the foreground, noting that $\pi_{k}^{-1}(\mathcal{F_{k}})$ is the maximal set of voxels with projection $\mathcal{F}_{k}$.
The visual hull is the maximal set of voxels whose projections are contained in all foregrounds $$V=\bigcap^{N}_{k=1}\pi_{k}^{-1}(\mathcal{F}_{k})$$
We can also define it as an optimization problem, the consistency of a voxel $v$ with the $k$-th image is defined as $$\begin{equation}cons_{k}(v)=\begin{cases}1 &\text{if } v \in\pi_{k}^{-1}(\mathcal{F}_{k}) \\
-N & \text{otherwise}\end{cases}\end{equation}$$
and its total consistency can be defined as $cons(v)=\sum\limits_{k=1}^{N}cons_{k}(v)$. Then the visual hull is the set of voxels that maximize the total consistency:
$$V= \text{arg} \underset{S}{\operatorname{max}}\sum\limits_{v\in S}cons(v)$$
Tiny distortions can cause inconsistencies using the normal visual hull algorithm, and in the end the reconstruction doesn't match any of the input images. To improve this they use one of the images as a regularization term.
Given a set of images, a distinguished image $I_{j}$ and a regularization parameter $\lambda$, the regularized visual hull is the set of voxels $V_{\lambda}$ such that $$V_{\lambda}=\text{arg}\underset{S}{\operatorname{max}}\{\sum\limits_{v\in S}cons(v)+\lambda \cdot |\pi_{j}(S)\cap\mathcal{F}_{k}|\}$$
Only one image is used since jittering can cause different images to contradict each other. Since roots cause only a tiny amount of occlusion using only one image is not a problem. The regularized visual hull is always the same or bigger than the regular visual hull, it never excludes voxels from the model.

The computation of the regularized visual hull goes as follows:
	The regularized visual hull is initialized as the visual hull $V_\lambda=V$ 
	Visiting each pixel $u$ in $\mathcal{F}_{j}$, if $u$ is not covered, look for a voxel with maximal consistency measure in the set $\pi_{j}^{-1}(u)$: $$v = \text{arg}\underset{v\in \pi_{j}^{-1}(u)}{\operatorname{max}}cons(v)$$
	 $cons(v)$ is negative, otherwise it would already be covered.
	 Then the regularized measure is computed $cons(v)+\lambda$, and $v$ is added to $V_\lambda$ if the measure is positive.

## Repairing Connectivity
The regularized visual hull can consist of ore than one connected component. To assure connectedness, they restrict themselves to add voxels to the reconstruction instead of removing from it. They add those voxels with low inconsistency with 2D images and with small distance to the regularized visual hull. For each voxel $v$ $$\begin{matrix}\text{incons}(v)& = & \text{max}\{-\text{cons}(v),0\}\\ \\ \text{dist}(v)& = & \underset{w\in V_{\lambda}}{\operatorname{min}}||v-w||\end{matrix}$$
Based on this an optimization problem is defined. They want to find a connected set of voxels $U$, with $V_{\lambda}\subseteq U$, that minimizes the following two measures in sequence:
1. The maximum distance to $V_\lambda$
2. The minimum inconsistency with the 2D images.

They use the Euclidean distance between the centers of two voxels to measure their distance, two voxels are neighbors when they share a 2-dimensional face. A path is a sequence of voxels in which any two contiguos voxels are neighbors, and $U$ is connected if any two of its voxels have a connecting path within $U$.

Let $d\geq 0$ be the smallest threshold such that the set of voxels $S=S_d$ with distance at most $d$ from $V_\lambda$ is connected. They optimize the first criterion computing $S$ with breadth first search, and limiting $U$ to be a subset of $S$. If $v\in V_\lambda$, $\text{incons}(v)=0$ by definition, and by construction $\text{incons}(v)>0$ if $v\in S-V_\lambda$ . $S$ can be expressed as a graph in which the voxels are nodes and edges are pairs of neighboring voxels. The weight of any edge is the larger inconsistency of its two nodes.

They compute the minimum spanning tree of this graph. Any voxel $v\in S-V_\lambda$ separates if it lies on a minimum cost path and connects two voxels in $V_\lambda$. The desired solution then is the set $U$ that consists of all voxels in $V_\lambda$ plus all separating voxels in the minimum spanning tree. They compute $U$ by repeatedly removing the leafs nodes in the spanning tree if they do not belong to $V_\lambda$.
![[Reparacion de topologia detailed root reconstruction.jpg]]

## Experiments
Forty plant roots, forty images each taken in a circle around the plant. Grown in gel. Plants placed in a turntable, programmed to alternate between a small rotation an a stop, long enough for a single image to be acquired. The root moves in the gel which accounts for some inaccuracies during data acquisition. 