import numpy as np
from mayavi import mlab

# Create a 3D sphere
phi, theta = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

# Create the figure
mlab.figure(size=(800, 800), bgcolor=(0, 0, 0))

# Function to update the Sun's surface
def update_surface(t):
    global sphere
    r = 1 + 0.1 * np.sin(10 * (phi - t))
    sphere.mlab_source.set(x=r*np.sin(theta) * np.cos(phi),
                           y=r*np.sin(theta) * np.sin(phi),
                           z=r*np.cos(theta))

# Create the initial surface
sphere = mlab.mesh(x, y, z, color=(1, 1, 0))

# Animate the surface
@mlab.animate(delay=50)
def animate():
    t = 0
    while True:
        update_surface(t)
        t += 0.1
        yield

animate()
mlab.show()
