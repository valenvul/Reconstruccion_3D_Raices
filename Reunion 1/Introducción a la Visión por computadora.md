[[Szeliski]] Caps 1 y 2
[[Reunion 1]]

---
# Geometric Primitives and Transformations
Geometric primitives are the basic building blocks for 3D shapes.
## 2D
### Points
2D points can be represented as pairs $(x,y)\in\mathbb{R}^{2}$ or *homogeneous coordinates* $\tilde x = (\tilde x, \tilde y,\tilde w)\in \mathcal{P}^{2}$ where vectors that only differ by scale are considered to be equivalent. The space $\mathcal{P}^{2}=\mathbb{R}^{3}-(0,0,0)$ and it's called the 2D *projective space*. 
To go from a homogeneous vector to an inhomogeneous vector you only need to divide it by the $\tilde w$ component. $\tilde x = \tilde w\bar x = \tilde w (x,y,1)$. $\bar x$ is called the *augmented vector*.
When $\tilde w$ equals $0$ the points are calles *ideal points* and they model infinity. They do not have an inhomogeneous representation.
### Lines
Extending these concepts to 2D lines, they can also be represented by homogeneous coordinates $\tilde l = (a,b,c)$. And it's corresponding line equation is $\hat x \cdot \tilde l = ax+by+c=0$.

The line equation can be normalized and described by  it's *normal vector* that's perpendicular to the line and of size $||\hat n||=1$ and by it's distance to the origin. $l=(\hat n_{x},\hat n_{y},d)$.
The l*ine at infinity* $\tilde l=(0,0,1)$ can't be normalized.

$\hat n$ can also be expressed as a function of rotation angle $\theta$ $\hat n = (\hat n_{x}, \hat n_{y})=(\text{cos } \theta, \text{sin }\theta)$. The coordinates $(\theta, d)$ are known as the line's *polar coordinates.*

The intersection of two lines can be computed as $\tilde x = \tilde l_{1}\times \tilde l_2$ where $\times$ is the cross product. Similarly the line joining two points can be written as $\tilde l = \tilde x_{1}\times \tilde x_{2}$.

![[Screenshot 2024-09-03 at 16.14.27.jpg]]
### Conics
*Conic sections* are the intersection between a plane and a 3D cone. They can be expressed by homogeneous equation using a *quadric* equation $\tilde x^{T} Q \tilde x=0$.

## 3D
### Planes
They can be represented as homogeneous coordinates $\tilde m = (a,b,c,d)$ with a corresponding plane equation $\hat x \cdot \tilde m = ax + by + cz+ d = 0$.
This, again, can be expressed in a normalized manner $m = (\hat n_{x}, \hat n_{y}, \hat n_{z}, d)$. In this case, the normal vector is perpendicular to the plane and $d$ is the distance of the plane to the origin. The *plane at infinity* $\tilde m = (0,0,0,1)$ contains all the points at infinity and cannot be normalized.
![[Screenshot 2024-09-03 at 16.14.17.jpg]]

$\hat n$ can once again be expressed as a function of angles, using *spherical coordinates* $\hat n = (\text{cos }\theta\text{ cos }\phi, \text{ sin }\theta\text{ cos }\phi,\text{ sin }\phi)$. They are not as widely used and do not sample the space of possible normal vectors uniformly.

## Lines
One way to express lines in 3D is using two points belonging to it. Any other point on the line can be expressed as a linear combination of those points $r = (1-\lambda)p+\lambda q$. If we limit $\lambda$ to only take values between $0$ and $1$, we get the segment joining both points.
![[Screenshot 2024-09-03 at 16.21.44.jpg]]

Using homogeneous coordinates lines can be expressed as $\tilde r = \mu \tilde p + \lambda \tilde q$. When the second point is infinity ($\tilde q =(\hat d_{x},\hat d_{y},\hat d_{z},0)=(\hat d,0)$), we can still use the direction of the line $\hat d$ and rewrite the inhomogeneous 3D line equation as $r=p+\lambda \hat d$.

We can use plane parametrization to reduce the amount of degrees of freedom given by this representation. By fixing two planes (for example z=0 and z=1) we only have four degrees to worry about.

