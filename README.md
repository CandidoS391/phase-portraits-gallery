# Phase Portraits Gallery 

## Overview
This is a Python/Manim project that not only explores the mathematics, but also the art and beauty of Phase Portraits that arise from differential equations.

This project combines the  mathematical concepts of differential equations and dynamical systems, the numerical techniques of solving these systems such as the RK4 (Runge-Kutta) Method, and the creative capabilities of Python and Manim to create a visually pleasing collection of art that will be shown here.

To view the animation, [here's the link](https://drive.google.com/file/d/1ta7rnpXjM69F5B1s-VTPhQ58pqybgBPN/view?usp=sharing)

### What is a Phase Portrait? 
A phase portrait is a visual and geometric representation of a dynamical system governed by differential equations. Using vector fields and solution curves, it shows how a system evolves over time to reveal the qualitative behavior of a system. 

Rather than focusing on exact solutions, phase portraits emphasize the the overall structure of a system's behavior. In many cases, especially for nonlinear systems, closed-form solutions are difficult or even possible to find; so phase portraits provide a powerful alternative by offering a qualitative understanding of how trajectories move through the phase space. 

For more information on Phase Portraits, see the [Wikipedia article on phase portraits](https://en.wikipedia.org/wiki/Phase_portrait)


## The Gallery
Now for each portrait that you will see throughout the video, each of them are governed by a specific differential equation and set of conditions. This section will provide a mathematical explanation of each differential equation that sets up the phase portrait, as well as the qualitiative features observed in phase portraits. 

### Spiral Sink

The spiral sink is a phase portrait that arises from a linear system of differential equations of the form

$$
\dot{\vec{x}} = A\vec{x}, \quad \text{where } \vec{x} = \begin{bmatrix} x \\ y \end{bmatrix}
$$

and the matrix \( A \) has complex eigenvalues with negative real parts.

In this case, a representative system is given by

$$
A = \begin{bmatrix}
-1 & -2 \\
2 & -1
\end{bmatrix}
$$

which produces eigenvalues of the form

$$
\lambda = -1 \pm 2i
$$

Because the real part of the eigenvalues is negative, all trajectories decay toward the origin over time. The imaginary component introduces rotation, causing the trajectories to spiral rather than move directly inward.

As a result, the origin acts as a **stable equilibrium point**, often referred to as a *sink*, since all nearby trajectories are attracted to it.

In the phase portrait, this behavior appears as inward spiraling curves, with each trajectory gradually losing amplitude as it approaches the center. The vector field reflects this by pointing both inward and rotationally, combining contraction and rotation at every point in the plane.

This system highlights how eigenvalues directly determine the qualitative behavior of solutions, with the real part controlling stability and the imaginary part controlling oscillation.

### Center 

The center phase portrait arises from a linear system of differential equations of the form

$$
\dot{\vec{x}} = A\vec{x}, \quad \text{where } \vec{x} = \begin{bmatrix} x \\ y \end{bmatrix}
$$

A representative system is given by

$$
A = \begin{bmatrix}
0 & -1 \\
1 & 0
\end{bmatrix}
$$

The eigenvalues of this system are

$$
\lambda = \pm i
$$

Because the eigenvalues of this matrix are purely imaginary (meaning the real Eigenvalues is zero), there is no exponential growth nor decay within the phase portrait. 

As a result, the origin acts as a **neutral equilibrium point** or *center* since trajectories neither converge nor diverge from the origin, but instead remain at a constant distance from it. 

Meanwhile the imaginary component of the eigenvalues introduces rotation, similar to the sink portrait. However due of the absence of any growth or decay, this portrait is purely rotational, resulting in closed trajectories around the origin.

This is seen in the visual as the vector field and the trajectories form circular and elliptical movements around the origin, and don't converge nor diverge (unlike the sink).

This behavior reflects a system that conserves an energy-like quantity, where motion continues indefinitely without damping.

### Saddle Point 

The saddle point phase portrait arises from a linear system of differential equations of the form

$$
\dot{\vec{x}} = A\vec{x}, \quad \text{where } \vec{x} = \begin{bmatrix} x \\ y \end{bmatrix}
$$

A representative system is given by

$$
A = \begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
$$

The eigenvalues of this system are

$$
\lambda_1 = 1, \quad \lambda_2 = -1
$$

As this system has one positive and one negative eigenvalue, this causes solutions to the system to either move toward the origin along the path of one of the eigenvectors, or move away from the origin along the path of the other eigenvector. 

Because of this, that means one direction is experiencing exponential growth and the other experiencing decay, resulting in the two directions diverging away from the origin, and making the origin itself unstable. 

That's why this system is known as a *saddle* portrait as within this portrait, the trajectories are approaching the origin before diverging, showcasing how a mixed set of eigenvalues produces instability at the origin. 

### Defective Node

The defective node phase portrait arises from a linear system of differential equations of the form

$$
\dot{\vec{x}} = A\vec{x}, \quad \text{where } \vec{x} = \begin{bmatrix} x \\ y \end{bmatrix}
$$

A representative system is given by

$$
A = \begin{bmatrix}
-1 & 1 \\
0 & -1
\end{bmatrix}
$$

The eigenvalues of this system are

$$
\lambda = -1
$$

with only one linearly independent eigenvector.

### Rotated Defective System 

The rotated defective system is a variation of a defective node, obtained by applying a transformation to the system matrix.

A representative system is given by

$$
A = \begin{bmatrix}
2 & 1 \\
-1 & 4
\end{bmatrix}
$$

The eigenvalues of this system are

$$
\lambda = 3
$$

with only one linearly independent eigenvector.

### Damped Pendulum

The damped pendulum is governed by a nonlinear differential equation written as:

$$
\dot{\theta} = \omega, \qquad \dot{\omega} = -\sin(\theta) - c\omega
$$

where:
$$
\theta = \text{angular position}, \quad \omega = \text{angular velocity}, \quad c > 0
$$


## Technical Notes

This project combines numerical methods, dynamical systems, and visualization techniques to construct each phase portrait.

### Numerical Integration

Trajectories are generated using the fourth-order Runge–Kutta (RK4) method. This allows for accurate approximation of solutions to both linear and nonlinear differential equations without requiring closed-form solutions.

### Forward and Backward Integration

To produce complete trajectories, each solution curve is generated by integrating both forward and backward in time. These paths are then combined to create smooth, continuous curves across the phase plane.

### Vector Fields

Each phase portrait is built on top of an `ArrowVectorField`, where vectors represent the local direction of the system at each point. The length and direction of each arrow are scaled to maintain visual clarity.

### Trajectory Construction

Solution curves are constructed as smooth parametric paths using Manim’s `VMobject`. Care is taken to:
- clean and format trajectory points
- maintain continuity
- avoid numerical instability near boundaries

### Nonlinear Systems

For nonlinear systems such as the damped pendulum, behavior is determined numerically rather than analytically. This allows the visualization of more complex phenomena such as:
- spiraling trajectories due to damping
- separatrices dividing different motion regimes
- transitions between oscillation and rotation

### Design Choices

The visual style is carefully chosen to emphasize clarity and aesthetics:
- vector fields are colored based on position or energy
- trajectories are uniformly styled for readability
- highlighted solution curves are used to illustrate specific behaviors

Overall, the project aims to balance mathematical accuracy with visual presentation, treating each phase portrait as both a computational result and a piece of mathematical art.

 