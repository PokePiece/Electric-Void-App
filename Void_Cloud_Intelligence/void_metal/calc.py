

#derivatives

#a derivative is a rate of change: how things vary over time
    #has uses in control systems and ai system dynamics. derivatives model velocity, acceleration,
    #and temperature gradients

#approximate a derivative

def derivative (f, x, h=1e-5):
    return (f(x+h) - f(x)) / h

import matplotlib.pyplot as plt
import numpy as np

# Simulation parameters
dt = 0.01  # time step (s)
time = np.arange(0, 10, dt)

# System state
angle = 0.1  # radians (initial tilt)
angular_velocity = 0.0

# PID parameters (tweak these!)
Kp = 25.0
Ki = 1.0
Kd = 5.0

# PID state
integral = 0.0
previous_error = 0.0

# Physical constants
mass = 1.0  # kg
length = 1.0  # m
gravity = 9.81  # m/s²

#meme review

# Logging for plotting
angle_log = []

for t in time:
    # Error (we want angle to be 0)
    error = 0.0 - angle
    integral += error * dt
    derivative = (error - previous_error) / dt

    # PID output (force to apply at the base)
    torque = Kp * error + Ki * integral + Kd * derivative

    # Physics: update angular acceleration
    angular_acceleration = (torque - mass * gravity * length * np.sin(angle)) / (mass * length**2)
    
    # Integrate to get velocity and position (Euler method)
    angular_velocity += angular_acceleration * dt
    angle += angular_velocity * dt

    previous_error = error
    angle_log.append(np.degrees(angle))

# Plot the angle over time
plt.figure(figsize=(10, 4))
plt.plot(time, angle_log)
plt.axhline(0, color='gray', linestyle='--')
plt.title("Self-Balancing Bot Simulation")
plt.xlabel("Time (s)")
plt.ylabel("Angle (degrees)")
plt.grid(True)
plt.show()
