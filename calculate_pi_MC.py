import random
import matplotlib.pyplot as plt
import numpy as np
import math

# Function to read sample sizes from a file
def read_sample_sizes_from_file(filename):
    try:
        with open(filename, 'r') as file:
            sample_sizes = [int(line.strip()) for line in file.readlines()]
            return sample_sizes
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found. Using default values.")
        return [100, 1000, 10000, 50000, 100000]  # Default sample sizes

# Function to estimate Pi
def estimate_pi(num_points):
    # Initialize counters and lists
    inside_circle = 0
    x_inside = []
    y_inside = []
    x_outside = []
    y_outside = []
    
    # Generate random points and check if they fall inside the unit circle
    for _ in range(num_points):
        x = random.uniform(-1, 1)  # x-coordinate in range [-1, 1]
        y = random.uniform(-1, 1)  # y-coordinate in range [-1, 1]
        
        # Check if the point is inside the unit circle (x^2 + y^2 <= 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1
            x_inside.append(x)
            y_inside.append(y)
        else:
            x_outside.append(x)
            y_outside.append(y)
    
    # Estimate Pi using the ratio of inside points to total points
    pi_estimate = 4 * inside_circle / num_points
    
    return pi_estimate, x_inside, y_inside, x_outside, y_outside

# Read sample sizes from a file (or use default values if file is not found)
sample_sizes = read_sample_sizes_from_file('sample_sizes.txt')

# Prepare lists to store Pi approximations for plotting
pi_values = []
sample_sizes_for_plot = []

# Calculate required number of rows and columns for subplots
num_samples = len(sample_sizes)
cols = 3
rows = math.ceil((num_samples + 1) / cols)  # Round up to the nearest integer, +1 for the Pi plot

# Adjust the figure size dynamically based on the number of subplots
fig_width = 6 * cols
fig_height = 6 * rows

# Set up the plot
fig, axs = plt.subplots(rows, cols, figsize=(fig_width, fig_height))

# Flatten the 2D array of axes for easier indexing
axs = axs.flatten()

# Generate plots for different sample sizes
for idx, sample_size in enumerate(sample_sizes):
    # Estimate Pi and get points
    pi_estimate, x_inside, y_inside, x_outside, y_outside = estimate_pi(sample_size)
    pi_values.append(pi_estimate)
    sample_sizes_for_plot.append(sample_size)
    
    # Plot the points inside and outside the circle
    ax = axs[idx]  # Select the appropriate subplot for the current sample size

    # Plot the points inside and outside the circle
    ax.scatter(x_inside, y_inside, color='blue', s=1, label='Inside Circle')
    ax.scatter(x_outside, y_outside, color='red', s=1, label='Outside Circle')
    
    # Circle visualization
    circle = plt.Circle((0, 0), 1, color='black', fill=False, linewidth=2)
    ax.add_artist(circle)
    
    # Formatting the plot
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(f"Sample Size: {sample_size}\nEstimated Pi: {pi_estimate:.5f}")
    ax.legend()

# Plot the Pi approximation and real Pi in the last subplot
# Always place the Pi approximation in the last subplot (regardless of how many sample sizes)
ax_pi = axs[num_samples]  # Last subplot for Pi approximation

# Plot Pi approximation
ax_pi.plot(sample_sizes_for_plot, pi_values, marker='o', linestyle='-', color='b', label='Approximated Pi')
ax_pi.axhline(y=np.pi, color='r', linestyle='--', label=f'Real Pi ≈ {np.pi:.5f}')
ax_pi.set_xscale('log')  # Logarithmic x-axis for better scaling
ax_pi.set_xlabel('Sample Size (Log scale)')
ax_pi.set_ylabel('Approximated Pi')
ax_pi.set_title('Pi Approximation vs Sample Size')
ax_pi.legend()
ax_pi.grid(True)

# Remove extra subplots if any (after the last used subplot)
for jdx in range(num_samples + 1, len(axs)):  # +1 because Pi plot is the last subplot
    fig.delaxes(axs[jdx])

# Adjust layout to avoid overlapping and ensure the plot fits nicely
plt.tight_layout()

# Show the plot with all subplots
plt.show()
