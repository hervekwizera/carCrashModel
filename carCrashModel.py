import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from playsound import playsound
import threading

# === PARAMETERS ===
m1 = 1200  # kg (car 1 mass)
m2 = 1000  # kg (car 2 mass)
v1i = 15   # m/s (initial velocity car 1)
v2i = -10  # m/s (initial velocity car 2)
e = 0.3    # restitution coefficient

# === FINAL VELOCITIES ===
v1f = ((m1 - e * m2) * v1i + (1 + e) * m2 * v2i) / (m1 + m2)
v2f = ((m2 - e * m1) * v2i + (1 + e) * m1 * v1i) / (m1 + m2)

# === KINETIC ENERGY ===
ke_before = 0.5 * m1 * v1i**2 + 0.5 * m2 * v2i**2
ke_after = 0.5 * m1 * v1f**2 + 0.5 * m2 * v2f**2
ke_loss = ke_before - ke_after

# === PRINT RESULTS ===
print("\n=== Results ===")
print(f"Final velocity of car 1: {v1f:.2f} m/s")
print(f"Final velocity of car 2: {v2f:.2f} m/s")
print(f"Kinetic energy lost: {ke_loss:.2f} J\n")

# === ANIMATION SETUP ===
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 10)
ax.set_title("Car Crash Simulation")
ax.set_xlabel("Position (m)")
ax.set_ylabel("Lanes")
ax.grid(True)

# Cars as rectangles
car1 = Rectangle((10, 2.5), 5, 1.5, color='blue')
car2 = Rectangle((80, 5.5), 5, 1.5, color='red')
ax.add_patch(car1)
ax.add_patch(car2)

# Trails
trail1, = ax.plot([], [], 'b--', linewidth=1)
trail2, = ax.plot([], [], 'r--', linewidth=1)
history1, history2 = [], []

# Texts for speed and KE
speed_text = ax.text(5, 9.5, '', fontsize=10)
energy_text = ax.text(5, 9.0, '', fontsize=10)

# Timing
x1, x2 = 10, 80
dt = 0.1
crash_time = abs((x2 - x1) / (v1i - v2i))
sound_played = False

# === FUNCTIONS ===
def play_sound():
    playsound("crash_sound.mp3")

def init():
    trail1.set_data([], [])
    trail2.set_data([], [])
    return car1, car2, trail1, trail2, speed_text, energy_text

def update(frame):
    global x1, x2, sound_played
    t = frame * dt

    if t < crash_time:
        x1 = 10 + v1i * t
        x2 = 80 + v2i * t
        v1, v2 = v1i, v2i
    else:
        if not sound_played:
            threading.Thread(target=play_sound).start()
            sound_played = True

        t_after = t - crash_time
        x1 = 10 + v1i * crash_time + v1f * t_after
        x2 = 80 + v2i * crash_time + v2f * t_after
        v1, v2 = v1f, v2f

    # Update car positions
    car1.set_xy((x1, 2.5))
    car2.set_xy((x2, 5.5))

    # Flash color on crash
    if abs(t - crash_time) < dt:
        car1.set_color('yellow')
        car2.set_color('yellow')
    elif t > crash_time:
        car1.set_color('blue')
        car2.set_color('red')

    # Update trails
    history1.append(x1 + 2.5)
    history2.append(x2 + 2.5)
    trail1.set_data(history1, [3.25] * len(history1))
    trail2.set_data(history2, [6.25] * len(history2))

    # Update info texts
    speed_text.set_text(f"v1: {v1:.2f} m/s, v2: {v2:.2f} m/s")
    energy_text.set_text(f"KE lost: {ke_loss:.2f} J")

    return car1, car2, trail1, trail2, speed_text, energy_text

# === ANIMATE ===
ani = animation.FuncAnimation(fig, update, frames=200, init_func=init,
                              interval=50, blit=True)

plt.show()
