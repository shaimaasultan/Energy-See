import numpy as np
import matplotlib.pyplot as plt
from dedalus import public as de
import logging

# 1. Basics & Domain (1D Fourier basis for periodic boundaries)
logger = logging.getLogger(__name__)
xbasis = de.Fourier('x', 512, bounds=(-10, 10))
domain = de.Domain([xbasis], np.float64)

# 2. Problem Setup
# We split the 2nd order wave equation into two 1st order equations:
# dt(u) - v = 0
# dt(v) - dx(dx(u)) = 0
problem = de.IVP(domain, variables=['u', 'v'])
problem.add_equation("dt(u) - v = 0")
problem.add_equation("dt(v) - dx(dx(u)) = 0")

# 3. Solver & Timestepping
solver = problem.build_solver(de.timesteppers.RK443)
solver.stop_sim_time = 15.0

# 4. Initial Conditions (The "Cancellation" setup)
u = solver.state['u']
v = solver.state['v']
x = domain.grid(0)

# Create two pulses moving toward each other
# Pulse A (Positive, moving right) + Pulse B (Negative, moving left)
u['g'] = np.exp(-(x+5)**2) - np.exp(-(x-5)**2)
# To give them velocity, we set v = -du/dt logic (approximate for wave packet)
v['g'] = 2*(x+5)*np.exp(-(x+5)**2) + 2*(x-5)*np.exp(-(x-5)**2)

# 5. Main Loop & Real-time Plotting
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(x, u['g'])
ax.set_ylim(-1.5, 1.5)
ax.set_title("1D Wave Cancellation Simulation")

while solver.ok:
    solver.step(0.05) # Timestep size
    if solver.iteration % 10 == 0:
        line.set_ydata(u['g'])
        plt.pause(0.01)
        if solver.sim_time >= solver.stop_sim_time:
            break

plt.ioff()
plt.show()