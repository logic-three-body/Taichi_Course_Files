# Authored by Tiantian Liu, Taichi Graphics.
import math

import taichi as ti

ti.init(arch=ti.gpu)

# global control
paused = ti.field(ti.i32, ())

# gravitational constant 6.67408e-11, using 1 for simplicity
G = 1

# number of planets
N = 3000
# unit mass
m = 1
M = 5000#big planet
# galaxy size
galaxy_size = 0.5
# planet radius (for rendering)
planet_radius = 2
Const_planet_radius = 30

# init vel
init_vel = 120

# time-step size
h = 1e-4
# substepping
substepping = 10

# center of the screen
center = ti.Vector.field(2, ti.f32, ())

# Hale
Start = ti.field(dtype=int,shape=())
#IsHale = ti.field(1, ti.f32, N)
IsHale = ti.field(dtype=int,shape=(1,N))


# pos, vel and force of the planets
# Nx2 vectors
pos = ti.Vector.field(2, ti.f32, N)
vel = ti.Vector.field(2, ti.f32, N)
force = ti.Vector.field(2, ti.f32, N)
Const_Pos=ti.Vector.field(2,ti.f32,())
Const_Pos[None]=[.5,.5]

@ti.kernel
def initialize():
    center[None] = [0.5, 0.5]
    for i in range(N):
        theta = ti.random() * 2 * math.pi
        r = (ti.sqrt(ti.random()) * 0.6 + 0.4) * galaxy_size
        offset = r * ti.Vector([ti.cos(theta), ti.sin(theta)])
        pos[i] = center[None] + offset
        vel[i] = [-offset.y, offset.x]
        vel[i] *= init_vel


@ti.kernel
def compute_force():
    # clear force
    for i in range(N):
        force[i] = [0.0, 0.0]

    # compute gravitational force
    for i in range(N):  # for each planet
        p = pos[i]
        for j in range(N):  # for each planet besides itself
            if i != j:  # double the computation for a better memory footprint and load balance
                diff = p - pos[j]
                r = diff.norm(1e-5)  # clamp to 1e-5 if diff<0

                # gravitational force -(GMm / r^2) * (diff/r) for i
                f = -G * m * m * (1.0 / r) ** 3 * diff  # '**' means pow,'**3' means pow(3)

                # assign to each particle
                force[i] += f

    #Const planet
    for i in range(N):
        diff = pos[i] - Const_Pos[None]
        #print(diff.norm())
        if diff.norm()<1e-2:
            IsHale[0,i] = 1

        r = diff.norm(1e-2)  # clamp to 1e-1 if diff<0
        f = -G * m * M * (1.0 / r) ** 3 * diff
        force[i] += f


@ti.kernel
def update():
    dt = h / substepping
    for i in range(N):
        # symplectic euler
        # vel[i] += dt * force[i] / m
        # pos[i] += dt * vel[i]
        if Start[None] and IsHale[0,i]:
            #print(IsHale[0,i])
            pos[i]=[-10000,-10000]
            vel[i]=[0,0]
        else:
            vel[i] += dt * force[i] / m
            pos[i] += dt * vel[i]



res = 500
gui = ti.GUI('N-body problem', (res, res))

initialize()
while gui.running:

    for e in gui.get_events(ti.GUI.PRESS):
        if e.key in [ti.GUI.ESCAPE, ti.GUI.EXIT]:
            exit()
        elif e.key == 'r':
            initialize()
        elif e.key == ti.GUI.SPACE:
            paused[None] = not paused[None]
        elif e.key == ti.GUI.LMB:
            Const_Pos[None] = [e.pos[0],e.pos[1]]
        elif e.key == ti.GUI.RMB:
            Start[None] = 1#start hale the planets

    if not paused[None]:
        for i in range(substepping):
            compute_force()
            update()

    #print(Start[None])

    gui.circles(pos.to_numpy(), color=0xffffff, radius=planet_radius)
    gui.circle(pos=Const_Pos[None], color=0xF9F3DF, radius=Const_planet_radius)
    gui.circle(pos=Const_Pos[None], color=0xCDF2CA, radius=Const_planet_radius/2)
    gui.circle(pos=Const_Pos[None], color=0xFFC898, radius=Const_planet_radius/4)


    gui.show()
