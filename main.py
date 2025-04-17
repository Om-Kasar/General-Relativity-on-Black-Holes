import numpy as np
import plotly.graph_objects as go
import taichi as ti

# Change to ti.gpu or ti.opengl if needed
ti.init(arch=ti.cpu)

# ---- MODEL CONSTANTS ----

G = 1                               # Gravitational Constant
M = 1                               # Mass of Black Hole
c = 1                               # Speed of Light
dt = 0.01                           # Increment used for position
steps = 260                         # How far the trajectory covers
Z_CLAMP = 50                        # Z-axis limiter
schwarzschild_radius = 2*G*M/c**2   # Schwarzschild Radius

# ---- IMPLEMENT CURVATURE GRID ----

x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
Z = -2 * G * M / R**3
Z = np.clip(Z, -Z_CLAMP, 0)

# ---- USE TAICHI VECTOR FIELDS ----
pos = ti.Vector.field(2, dtype=ti.f32, shape=())
vel = ti.Vector.field(2, dtype=ti.f32, shape=())
trajectory = ti.Vector.field(3, dtype=ti.f32, shape=steps)

@ti.func
def gravity_force(position):
    r = position.norm()
    if r < 0.1:
        r = 0.1
    f_mag = -G * M / (r ** 3)
    return f_mag * position.normalized()

@ti.kernel
def init():
    pos[None] = ti.Vector([1.5, 0.0])
    vel[None] = ti.Vector([0.0, 0.35])

@ti.kernel
def update():
    for i in range(steps):
        force = gravity_force(pos[None])
        vel[None] += force * dt
        pos[None] += vel[None] * dt
        r = pos[None].norm()
        curvature = -2 * G * M / (r**3)
        curvature = max(curvature, -Z_CLAMP)
        trajectory[i] = ti.Vector([pos[None][0], pos[None][1], curvature])

# ---- RUN SIMULATION ----
init()
update()

# Convert trajectory to NumPy for plotting
trajectory_np = trajectory.to_numpy()

# ---- GENERATE ANIMATION FRAMES ----
frames = []
for i in range(steps):
    frames.append(go.Frame(
        data=[
            # Curvature surface
            go.Surface(
                z=Z, x=X, y=Y,
                colorscale='Viridis',
                opacity=0.8,
                showscale=False,
                name='Spacetime curvature'
            ),
            # Black hole entity
            go.Scatter3d(
                x=[0], y=[0], z=[0],
                mode='markers',
                marker=dict(size=6, color='black'),
                name='Black Hole'
            ),
            # Animated particle only
            go.Scatter3d(
                x=[trajectory_np[i, 0]],
                y=[trajectory_np[i, 1]],
                z=[trajectory_np[i, 2]],
                mode='markers',
                marker=dict(size=5, color='red'),
                name='Particle'
            )
        ],
        name=str(i)
    ))

# ---- IMPLEMENT CURVATURE & PARTICLE INTO A PLOTLY FIGURE ----
fig = go.Figure(
    data=[
        go.Surface(
            z=Z, x=X, y=Y,
            colorscale='Viridis',
            opacity=0.8,
            showscale=True,
            name='Spacetime curvature'
        ),
        go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(size=6, color='black'),
            name='Black Hole'
        ),
        go.Scatter3d(
            x=[trajectory_np[0, 0]],
            y=[trajectory_np[0, 1]],
            z=[trajectory_np[0, 2]],
            mode='markers',
            marker=dict(size=5, color='red'),
            name='Particle'
        )
    ],
    layout=go.Layout(
        title=dict(
            text='Particle Motion Around Black Hole of Mass M = 1',
            x=0.5
        ),
        scene=dict(
            zaxis=dict(range=[np.min(Z), 0]),
            aspectratio=dict(x=1, y=1, z=0.7)
        ),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None, {"frame": {"duration": 40, "redraw": True},
                                       "fromcurrent": True}]),
                     dict(label="Pause",
                          method="animate",
                          args=[[None], {"frame": {"duration": 0, "redraw": False},
                                         "mode": "immediate",
                                         "transition": {"duration": 0}}])])
        ]
    ),
    frames=frames
)

fig.show()
