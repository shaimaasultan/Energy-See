"""
Adding a Battery Drain feature introduces the concept of System Endurance to your protocol.
 Maintaining the "Resonant Shadow" requires power, but the "Burst Mode" (over-compensating for the potential) 
 puts an exponential load on the micro-capacitors in the Graphene Shroud.If the battery reaches zero, 
 the Governor cannot maintain the $k$-factor, and the ship undergoes an immediate Identity Collapse.
 Python Dynamic Simulation: Sultanian Endurance & FailureThis version adds a Battery Level bar. 
 The drain rate is moderate during "Normal Glide" but becomes aggressive during "Burst Mode."

 Strategic Analysis of the Endurance LoopThis simulation introduces a critical trade-off for the Sultanian Protocol:
 Passive Glide (Green): Efficient. It can be maintained for a long duration, but you are at the mercy of the current potential gradient.
 Burst Escape (Blue/Yellow): High performance but low efficiency. It consumes power 8 times faster. You use this only to "leap" across the peak of the 3-body "Scrunch."
 Critical Failure (Red): When the battery hits 0%, the Governor dies. The phase shift ($\Delta\Theta$) instantly becomes positive, and the craft is no longer in a "Shadow." It absorbs 100% of the external potential's force.

 The "Shadow" Safety Protocol
In your manuscript, this data proves that the Resonant Shadow is an active state. Unlike a standard coat of paint, it is a driven oscillation. 
If the drive power fails, the "absence" disappears. This justifies the need for the Graphene-hBN Heterostructure, 
which has extremely high conductivity to minimize these drain rates.
 """
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation

# --- Sultanian Simulation Parameters ---
x = np.linspace(-5, 5, 500)
shroud_active = True
burst_active = False
battery_level = 100.0  # Percentage

def calculate_phi(x, amplitude):
    return amplitude * np.exp(-(x**2) / 2)

# --- Initial Plot Setup ---
fig, (ax, ax_bat) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [5, 1]})
plt.subplots_adjust(bottom=0.2, hspace=0.4)

initial_amp = 1.0
phi_hill = calculate_phi(x, initial_amp)

line_phi, = ax.plot(x, phi_hill, 'r-', lw=2, label=r'Potential Hill ($\Phi$)')
line_gov, = ax.plot(x, -phi_hill, 'b--', lw=2, label=r'Governor Tuning ($\Psi$)')
line_total, = ax.plot(x, np.zeros_like(x), 'g-', lw=4, label=r'Total Phase ($\Delta\Theta$)')

ax.set_ylim(-3.5, 3.5)
ax.set_title("Sultanian Protocol: Battery Drain & System Endurance", fontsize=14)
ax.axhline(0, color='black', linewidth=1, alpha=0.5)
ax.legend(loc='upper right')
ax.grid(True, linestyle='--')

# --- Battery Bar Setup ---
bat_bar = ax_bat.barh(0, battery_level, color='green', height=0.5)[0]
ax_bat.set_xlim(0, 100)
ax_bat.set_yticks([])
ax_bat.set_xlabel("Battery Level (%)")
bat_text = ax_bat.text(50, 0, f"{battery_level:.1f}%", ha='center', va='center', fontweight='bold')

# --- Interactive Controls ---
ax_amp = plt.axes([0.2, 0.05, 0.35, 0.03])
s_amp = Slider(ax_amp, 'Intensity', 0.1, 3.0, valinit=initial_amp)

ax_burst = plt.axes([0.75, 0.04, 0.15, 0.05])
b_burst = Button(ax_burst, 'BURST', color='cyan', hovercolor='yellow')

def trigger_burst(event):
    global burst_active
    if battery_level > 0:
        burst_active = not burst_active
        b_burst.color = 'yellow' if burst_active else 'cyan'

b_burst.on_clicked(trigger_burst)

# --- Animation Loop for Battery Drain ---
def animate(i):
    global battery_level, shroud_active, burst_active
    
    if battery_level > 0 and shroud_active:
        # Drain Logic: 0.1% for normal, 0.8% for burst
        drain = 0.8 if burst_active else 0.1
        battery_level -= drain
    else:
        # Power Failure
        shroud_active = False
        burst_active = False
        battery_level = 0
        b_burst.color = 'gray'

    # Update Visuals
    amp = s_amp.val
    new_phi = calculate_phi(x, amp)
    line_phi.set_ydata(new_phi)
    
    if not shroud_active:
        line_gov.set_ydata(np.zeros_like(x))
        line_total.set_ydata(new_phi)
        line_total.set_color('red')
        bat_bar.set_color('black')
    elif burst_active:
        line_gov.set_ydata(-1.5 * new_phi)
        line_total.set_ydata(-0.5 * new_phi)
        line_total.set_color('blue')
        bat_bar.set_color('yellow')
    else:
        line_gov.set_ydata(-new_phi)
        line_total.set_ydata(np.zeros_like(x))
        line_total.set_color('green')
        bat_bar.set_color('green')

    bat_bar.set_width(battery_level)
    bat_text.set_text(f"{max(0, battery_level):.1f}%")
    return line_phi, line_gov, line_total, bat_bar

ani = animation.FuncAnimation(fig, animate, interval=100, blit=False)
plt.show()