import numpy as np
import plotly.graph_objects as go

# TODO: Use taichi backend + integration with simulation
# ---- Constants ----
G = 1  
M = 0.5
c = 1
schwarzschild_radius = 2 * G * M / c ** 2
Z_CLAMP = 50

# Grid for spacetime curvature
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2 + 0.01)
Z = -2 * G * M / R**3
Z = np.clip(Z, -Z_CLAMP, 0)

# Create figure
fig = go.Figure()

# Add curvature surface
fig.add_trace(go.Surface(
    z=Z, x=X, y=Y,
    colorscale='Viridis',
    opacity=0.8,
    showscale=True,
    name='Spacetime curvature'
))

# TODO: Create Black Hole Sphere
'''u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
x_sphere = schwarzschild_radius * np.cos(u) * np.sin(v)
y_sphere = schwarzschild_radius * np.sin(u) * np.sin(v)
z_sphere = schwarzschild_radius * np.cos(v)

# Position sphere slightly above the lowest point of the surface
z_offset = np.min(Z) + 0.2  # Shift upward slightly
fig.add_trace(go.Surface(
    z=z_sphere + z_offset,
    x=x_sphere,
    y=y_sphere,
    surfacecolor=np.zeros_like(z_sphere),
    colorscale=[[0, 'black'], [1, 'black']],
    showscale=False,
    name='Black hole'
))'''

# Layout
fig.update_layout(
    title=dict(
        text='Spacetime Warping of Black Hole w/ Mass M = 0.5',
        x=0.5,
        xanchor='center'
    ),
    scene=dict(
        zaxis=dict(range=[np.min(Z), 0]),
        aspectratio=dict(x=1, y=1, z=1)
    )
)

fig.show()
