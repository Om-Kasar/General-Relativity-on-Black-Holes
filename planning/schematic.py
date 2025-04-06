import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define grid size
size = 50
x = np.linspace(-2, 2, size)
y = np.linspace(-2, 2, size)
X, Y = np.meshgrid(x, y)

# Define mass (M) and compute radial coordinate
M = 1
G = 1
R = np.sqrt(X**2 + Y**2) + 0.1  # Avoid division by zero

# Approximate Ricci Tensor component (Simplified for visualization)
R_00 = 2 * M * G / R**3  # Simplified Schwarzschild-like component

# Define deformation: Use Ricci tensor as height map
Z = -R_00  # Inverse for visualization

# Create 3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot spacetime fabric (deformed grid)
ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='k', alpha=0.7)

# Labels and aesthetics
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Ricci Curvature")
ax.set_title("Ricci Tensor on Spacetime Fabric")

plt.show()
