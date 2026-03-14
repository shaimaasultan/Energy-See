"""
Sultanian Protocol: Solar Charge & Burst Management Simulation
This simulation demonstrates the dynamic interplay between the Sultanian Protocol's energy management strategies and the resulting phase shifts. It introduces a critical trade-off:
- Passive Glide (Green): Efficient. It can be maintained for a long duration, but you are at the mercy of the current potential gradient.
- Burst Escape (Blue/Yellow): High performance but low efficiency. It consumes power 8 times faster. You use this only to "leap" across the peak of the 3-body "Scrunch."
- Critical Failure (Red): When the battery hits 0%, the Governor dies. The phase shift ($\Delta\Theta$) instantly becomes positive, and the craft is no longer in a "Shadow." It absorbs 100% of the external potential's force.    

To implement the Solar Recharge feature, we integrate a "Harvesting Mode" into the Governor's logic. 
In the Sultanian Protocol, when the external potential ($\Phi$) is low, the Graphene Shroud doesn't just sit idle; 
it acts as a wide-bandgap rectenna, converting background cosmic radiation and stray photons back into stored energy.
Python Dynamic Simulation: Sultanian Energy HarvestingIn this final iteration, we add logic 
where if the Intensity slider is set to a low value (representing the "Safe Zone" outside a singularity), the battery will begin to recharge.

The "Shadow" Conservation CycleThis creates a realistic mission profile for an astronaut or a Sultanian craft:
Preparation (Low Intensity): You stay in the "Safe Zone" ($Intensity < 0.6$). 
The green bar glows lime, and the battery recharges. You are gathering energy from the vacuum's background.
The Approach (Medium Intensity): As you get closer to the "Scrunch," the battery stops charging and begins a slow drain. 
The Resonant Shadow is now actively working to keep you invisible.The Leap (Burst Mode): You encounter the peak potential. You hit BURST. 
The battery drains rapidly, but your phase goes negative (Blue), pushing you through the danger zone quickly.
The Exit: Once through, you lower the intensity, the shroud switches back to harvesting mode, and you recover your energy for the next transit.

Strategic Conclusion
By adding this feature, you've turned the Sultanian Protocol from a one-way energy sink into 
a Sustainable Vacuum Engine. The material (Graphene-hBN) doesn't just hide you; it feeds you.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation

# --- Sultanian Simulation Parameters ---
x = np.linspace(-5, 5, 500)
shroud_active = True
burst_active = False
battery_level = 80.0  # Starting at 80% to demonstrate recharge

def calculate_phi(x, amplitude):
    return amplitude * np.exp(-(x**2) / 2)

# --- Plot Setup ---
fig, (ax, ax_bat) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [5, 1]})
plt.subplots_adjust(bottom=0.2, hspace=0.4)

initial_amp = 0.5 # Start at low intensity for recharge
phi_hill = calculate_phi(x, initial_amp)

line_phi, = ax.plot(x, phi_hill, 'r-', lw=2, label=r'Potential Hill ($\Phi$)')
line_gov, = ax.plot(x, -phi_hill, 'b--', lw=2, label=r'Governor Tuning ($\Psi$)')
line_total, = ax.plot(x, np.zeros_like(x), 'g-', lw=4, label=r'Total Phase ($\Delta\Theta$)')

ax.set_ylim(-3.5, 3.5)
ax.set_title("Sultanian Protocol: Energy Harvesting & Burst Management", fontsize=14)
ax.axhline(0, color='black', linewidth=1, alpha=0.5)
ax.legend(loc='upper right')
ax.grid(True, linestyle='--')

# --- Battery Bar Setup ---
bat_bar = ax_bat.barh(0, battery_level, color='green', height=0.5)[0]
ax_bat.set_xlim(0, 100)
ax_bat.set_yticks([])
ax_bat.set_xlabel("Battery Level (%)")
bat_text = ax_bat.text(50, 0, f"{battery_level:.1f}%", ha='center', va='center', fontweight='bold')

# --- Controls ---
ax_amp = plt.axes([0.2, 0.05, 0.35, 0.03])
s_amp = Slider(ax_amp, 'Intensity', 0.1, 3.0, valinit=initial_amp)

ax_burst = plt.axes([0.75, 0.04, 0.15, 0.05])
b_burst = Button(ax_burst, 'BURST', color='cyan', hovercolor='yellow')

def trigger_burst(event):
    global burst_active
    if battery_level > 5: # Safety interlock: Need 5% to burst
        burst_active = not burst_active
        b_burst.color = 'yellow' if burst_active else 'cyan'

b_burst.on_clicked(trigger_burst)

# --- Animation Loop: Drain vs. Recharge ---
def animate(i):
    global battery_level, shroud_active, burst_active
    
    amp = s_amp.val
    
    if battery_level > 0:
        if burst_active:
            # Aggressive Burst Drain
            battery_level -= 0.8
        elif amp > 1.2:
            # Active Shadowing Drain (High Potential)
            battery_level -= 0.15
        elif amp < 0.6:
            # SOLAR RECHARGE: Harvesting background potential
            # Rate increases the further you are from high potential
            recharge_rate = 0.2 * (0.6 - amp)
            battery_level = min(100.0, battery_level + recharge_rate)
        else:
            # Idle/Neutral State
            battery_level -= 0.02
    else:
        # Failure State
        shroud_active = False
        burst_active = False
        battery_level = 0

    # Update Logic
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
        # Recharge Visual indicator
        bat_bar.set_color('lime' if amp < 0.6 else 'green')

    bat_bar.set_width(battery_level)
    bat_text.set_text(f"{max(0, battery_level):.1f}%")
    return line_phi, line_gov, line_total, bat_bar

ani = animation.FuncAnimation(fig, animate, interval=100, blit=False)
plt.show()