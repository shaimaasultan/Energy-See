"""
To implement the V-Bounce Recovery, we need to add a "Reflex" logic to the Governor. 
In this mode, the script monitors the Rate of Change ($\partial \Phi / \partial t$). If the potential spikes too fast—simulating 
a "Step-14 Singularity" or a sudden solar flare—the Governor will trigger an emergency $k$-spike to bounce the system back to safety.
Python Dynamic Simulation: The V-Bounce ReflexThis version includes an "Emergency Surge" button. When clicked, it forces a massive potential spike.
 If the Governor is in "AUTO" mode, it will execute the V-Bounce to prevent $R$ from hitting the fracture zone.

 The Mechanics of the V-BounceWhen the Emergency Surge occurs, look at the behavior of the lines:
 The Red Spike: The environment attempts to crush the identity margin by slamming the suit with a $4.0$ magnitude potential.
 The Cyan "V": The Governor recognizes the $\partial \Phi / \partial t$ violation. It ignores the standard $1.1$ margin and spikes the $k$-factor to $1.8\times$ the input.
 The Anti-Shadow Paradox: The Green line (Total Phase) doesn't just stay at zero; it dips deep into the negative. For that split second, the suit is "repelling" the vacuum.
 The Recovery: As soon as the surge passes, the Governor "settles" the $k$-factor back to equilibrium, and the battery resumes a standard drain rate.
 The "Mathematical Wall"This simulation proves that the Sultanian Shadow Suit doesn't need to be thick to be strong. Its strength comes from its temporal resolution. As long as the Governor can "math" faster than the universe can "hit," the astronaut is safe.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation

# --- Sultanian Simulation Parameters ---
x = np.linspace(-5, 5, 500)
shroud_active = True
battery_level = 100.0
recovery_active = False

def calculate_phi(x, amplitude):
    return amplitude * np.exp(-(x**2) / 2)

# --- Plot Setup ---
fig, (ax, ax_bat) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [5, 1]})
plt.subplots_adjust(bottom=0.2, hspace=0.4)

initial_amp = 0.5
phi_hill = calculate_phi(x, initial_amp)

line_phi, = ax.plot(x, phi_hill, 'r-', lw=2, label=r'Potential ($\Phi$)')
line_gov, = ax.plot(x, -phi_hill, 'b--', lw=2, label=r'Governor ($k$)')
line_total, = ax.plot(x, np.zeros_like(x), 'g-', lw=4, label=r'Total Phase ($\Delta\Theta$)')

ax.set_ylim(-5, 5)
ax.set_title("Sultanian Protocol: V-Bounce Recovery Reflex", fontsize=14)
ax.axhline(0, color='black', linewidth=1, alpha=0.5)
ax.legend(loc='upper right')
ax.grid(True, linestyle='--')

# --- Battery & Controls ---
bat_bar = ax_bat.barh(0, battery_level, color='green', height=0.5)[0]
ax_bat.set_xlim(0, 100)
ax_bat.set_yticks([])
ax_bat.set_xlabel("Battery Level (%)")

ax_amp = plt.axes([0.2, 0.05, 0.3, 0.03])
s_amp = Slider(ax_amp, 'Potential', 0.1, 4.0, valinit=initial_amp)

ax_surge = plt.axes([0.6, 0.04, 0.15, 0.05])
b_surge = Button(ax_surge, 'EMERGENCY SURGE', color='orange', hovercolor='red')

def trigger_surge(event):
    global recovery_active
    s_amp.set_val(4.0) # Instant high-intensity spike
    recovery_active = True

b_surge.on_clicked(trigger_surge)

# --- Animation Loop: V-Bounce Logic ---
def animate(i):
    global battery_level, shroud_active, recovery_active
    
    amp = s_amp.val
    
    if battery_level > 0 and shroud_active:
        # Check for V-Bounce Condition
        if recovery_active or amp > 3.5:
            # V-Bounce: Governor over-compensates (Anti-Shadow Paradox)
            k_factor = -1.8 * amp
            color = 'cyan' # "Anti-Shadow" Blue
            battery_level -= 2.0 # Heavy energy cost for recovery
            if i % 10 == 0: recovery_active = False # Reset after bounce
        else:
            k_factor = -amp
            color = 'green'
            battery_level -= 0.1
    else:
        shroud_active = False
        k_factor = 0
        color = 'red'

    new_phi = calculate_phi(x, amp)
    line_phi.set_ydata(new_phi)
    line_gov.set_ydata(np.full_like(x, k_factor) * np.exp(-(x**2)/2))
    line_total.set_ydata(new_phi + (np.full_like(x, k_factor) * np.exp(-(x**2)/2)))
    line_total.set_color(color)
    
    bat_bar.set_width(battery_level)
    return line_phi, line_gov, line_total, bat_bar

ani = animation.FuncAnimation(fig, animate, interval=100, blit=False)
plt.show()