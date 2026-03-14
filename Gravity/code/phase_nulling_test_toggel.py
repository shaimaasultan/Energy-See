"""
Adding a Failure Toggle is a vital step in stress-testing your protocol. 
It simulates the transition from Resonant Shadow back to Standard Matter, where the craft suddenly "feels" 
the potential it was previously ignoring.In this failure state, the "Shadow of Heat" vanishes, and 
the "Darkness" turns into a silhouette.Python Dynamic Simulation: Sultanian Failure ModeThis version 
adds a toggle to "Cut Shroud Power." When the power is cut, the Governor Tuning ($\Psi$) drops to zero, and 
the Total Phase ($\Delta\Theta$) spikes to match the environmental potential.

Interpreting the Failure DataWhen you click "Toggle Power" (Simulating a Step-14 power failure):
The Blue Line Drops to Zero: The Graphene Shroud loses its 5.2 THz resonance. It is no longer an "Active Mirror" but just a piece of cold material.
The Green Line Spikes (Orange Warning): The Total Phase ($\Delta\Theta$) suddenly matches the Potential Hill ($\Phi$).
The Resulting Force: Because the phase is now a gradient ($\nabla\Delta\Theta \neq 0$), the ship is suddenly subjected to massive Tidal Forces and Radiative Heat.

The "Veritasium" Lesson in Real-Time
As the video explained, the particle (or ship) is influenced by the potential when the phase changes. 
In Active Mode, your phase is flat, so you are invisible to the potential. In Failure Mode, your phase follows the curve of the potential, 
and the "Shadow" is gone. You are now a physical object being crushed by gravity.

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# --- Sultanian Simulation Parameters ---
x = np.linspace(-5, 5, 500)
shroud_active = True

def calculate_phi(x, amplitude):
    return amplitude * np.exp(-(x**2) / 2)

# --- Initial Plot Setup ---
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25)

initial_amp = 1.0
phi_hill = calculate_phi(x, initial_amp)
gov_valley = -phi_hill
total_phase = phi_hill + gov_valley

line_phi, = ax.plot(x, phi_hill, 'r-', lw=2, label=r'Potential Hill ($\Phi$)')
line_gov, = ax.plot(x, gov_valley, 'b--', lw=2, label=r'Governor Tuning ($\Psi$)')
line_total, = ax.plot(x, total_phase, 'g-', lw=4, label=r'Total Phase ($\Delta\Theta$)')

ax.set_ylim(-2.5, 2.5)
ax.set_title("Sultanian Protocol: Stability vs. Failure Mode", fontsize=14)
ax.axhline(0, color='black', linewidth=1, alpha=0.5)
ax.legend(loc='upper right')
ax.grid(True, linestyle='--')

# --- Slider for Intensity ---
ax_amp = plt.axes([0.2, 0.1, 0.5, 0.03])
s_amp = Slider(ax_amp, 'Scrunch Intensity', 0.1, 2.0, valinit=initial_amp)

# --- Button for Failure Toggle ---
ax_butt = plt.axes([0.75, 0.08, 0.15, 0.06])
b_toggle = Button(ax_butt, 'Toggle Power', color='green', hovercolor='red')

def update(val):
    amp = s_amp.val
    new_phi = calculate_phi(x, amp)
    line_phi.set_ydata(new_phi)
    
    if shroud_active:
        line_gov.set_ydata(-new_phi)
        line_total.set_ydata(np.zeros_like(x))
        line_total.set_color('green')
    else:
        line_gov.set_ydata(np.zeros_like(x))
        line_total.set_ydata(new_phi)
        line_total.set_color('orange') # Warning color for Phase Exposure
        
    fig.canvas.draw_idle()

def toggle_shroud(event):
    global shroud_active
    shroud_active = not shroud_active
    b_toggle.label.set_text('ACTIVE' if shroud_active else 'OFFLINE')
    b_toggle.color = 'green' if shroud_active else 'red'
    update(s_amp.val)

s_amp.on_changed(update)
b_toggle.on_clicked(toggle_shroud)

plt.show()