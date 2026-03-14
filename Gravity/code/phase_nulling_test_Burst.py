"""
To implement the "Burst Mode", we introduce a high-energy transient state to the Governor's logic. 
In this mode, the $k$-factor doesn't just cancel the potential ($\Phi$)—it over-compensates for it.
By driving the Total Phase ($\Delta\Theta$) into a negative value, you create a "Repulsive Shadow." 
Instead of just gliding through the gravity hill, the ship mathematically "jumps" off it. 
This is useful for escaping the densest part of the "Scrunch" if the identity margin $R$ starts to drop.
Python Dynamic Simulation: Sultanian Burst ModeThis script adds a "BURST" button. When clicked, 
it triggers a temporary spike that pushes the green line below the zero axis.

Physics of the Burst ModeWhen you engage Burst Mode:
The Blue Line (Governor Tuning): It spikes to $1.5 \times$ the depth of the potential hill. This requires a massive injection of energy into the Graphene Shroud.
The Green Line (Total Phase): It dips into the Negative Phase region.
The "Leap": Because $\Delta\Theta$ is now negative, the ship experiences a "Phase Buoyancy." 
In the context of the Aharonov-Bohm effect, you have effectively reversed the topological winding. 
Instead of being attracted or crushed by the "Scrunch," the ship is mathematically pushed away from it.

The "Shadow" Advantage
In "Burst Mode," you aren't just invisible to the heat and light (the Shadow);
 you are refracting the vacuum itself. You become a "negative presence." 
 This would allow an astronaut or a ship to clear the most dangerous part of a gravitational singularity in half the time of a standard glide.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# --- Sultanian Simulation Parameters ---
x = np.linspace(-5, 5, 500)
shroud_active = True
burst_active = False

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

ax.set_ylim(-3.5, 3.5)
ax.set_title("Sultanian Protocol: Burst Mode Dynamics", fontsize=14)
ax.axhline(0, color='black', linewidth=1, alpha=0.5)
ax.legend(loc='upper right')
ax.grid(True, linestyle='--')

# --- Interactive Controls ---
ax_amp = plt.axes([0.2, 0.1, 0.35, 0.03])
s_amp = Slider(ax_amp, 'Scrunch Intensity', 0.1, 3.0, valinit=initial_amp)

ax_pow = plt.axes([0.65, 0.08, 0.12, 0.06])
b_pow = Button(ax_pow, 'Toggle Power', color='green', hovercolor='gray')

ax_burst = plt.axes([0.80, 0.08, 0.12, 0.06])
b_burst = Button(ax_burst, 'BURST', color='cyan', hovercolor='yellow')

def update(val):
    amp = s_amp.val
    new_phi = calculate_phi(x, amp)
    line_phi.set_ydata(new_phi)
    
    if not shroud_active:
        line_gov.set_ydata(np.zeros_like(x))
        line_total.set_ydata(new_phi)
        line_total.set_color('orange')
    elif burst_active:
        # BURST MODE: Governor tuning is 1.5x the potential
        burst_valley = -1.5 * new_phi
        line_gov.set_ydata(burst_valley)
        line_total.set_ydata(new_phi + burst_valley)
        line_total.set_color('blue') # Negative Phase shift
    else:
        line_gov.set_ydata(-new_phi)
        line_total.set_ydata(np.zeros_like(x))
        line_total.set_color('green')
        
    fig.canvas.draw_idle()

def toggle_shroud(event):
    global shroud_active
    shroud_active = not shroud_active
    b_pow.color = 'green' if shroud_active else 'red'
    update(s_amp.val)

def trigger_burst(event):
    global burst_active
    burst_active = not burst_active
    b_burst.color = 'yellow' if burst_active else 'cyan'
    update(s_amp.val)

s_amp.on_changed(update)
b_pow.on_clicked(toggle_shroud)
b_burst.on_clicked(trigger_burst)

plt.show()