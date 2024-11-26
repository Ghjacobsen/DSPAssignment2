import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import tf2zpk, zpk2tf

# Initialize poles and zeros
poles = []
zeros = []

# Variables to track dragging
dragging_item = None
dragging_type = None  # 'pole' or 'zero'

# Create the plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

# Plot the unit circle
theta = np.linspace(0, 2 * np.pi, 500)
ax.plot(np.cos(theta), np.sin(theta), 'k--', linewidth=1)
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_aspect('equal', 'box')
ax.grid(True)
ax.set_title('Interactive Pole-Zero Plot')
ax.set_xlabel('Real Part')
ax.set_ylabel('Imaginary Part')

# Placeholder for plots
zero_plot, = ax.plot([], [], 'bo', markersize=10, label="Zeros")
pole_plot, = ax.plot([], [], 'rx', markersize=10, label="Poles")
ax.legend()

# Helper function to update the plot
def update_plot():
    zero_plot.set_data(np.real(zeros), np.imag(zeros))
    pole_plot.set_data(np.real(poles), np.imag(poles))
    fig.canvas.draw_idle()

# Mouse click event handler
def on_click(event):
    global dragging_item, dragging_type
    if event.inaxes != ax:  # Ignore clicks outside the axes
        return
    
    x, y = event.xdata, event.ydata
    click_point = x + 1j * y

    if event.key == 'control':  # Ctrl key is held down for drag-and-drop
        # Check if clicking near a pole or zero
        for idx, pole in enumerate(poles):
            if np.abs(pole - click_point) < 0.1:
                dragging_item = idx
                dragging_type = 'pole'
                return
        for idx, zero in enumerate(zeros):
            if np.abs(zero - click_point) < 0.1:
                dragging_item = idx
                dragging_type = 'zero'
                return
    elif event.button == 1:  # Left click
        if event.key == 'shift':  # Remove a pole
            if poles:  # Ensure there are poles to remove
                distances = [np.abs(click_point - p) for p in poles]
                poles.pop(np.argmin(distances))
        else:  # Add a pole
            poles.append(click_point)
    elif event.button == 3:  # Right click
        if event.key == 'shift':  # Remove a zero
            if zeros:  # Ensure there are zeros to remove
                distances = [np.abs(click_point - z) for z in zeros]
                zeros.pop(np.argmin(distances))
        else:  # Add a zero
            zeros.append(click_point)
    
    update_plot()

# Mouse motion event handler
def on_motion(event):
    global dragging_item, dragging_type
    if dragging_item is None or dragging_type is None or event.key != 'control':
        return
    if event.inaxes != ax:  # Ignore motions outside the axes
        return
    
    x, y = event.xdata, event.ydata
    new_position = x + 1j * y

    # Update the position of the dragged item
    if dragging_type == 'pole':
        poles[dragging_item] = new_position
    elif dragging_type == 'zero':
        zeros[dragging_item] = new_position
    
    update_plot()

# Mouse release event handler
def on_release(event):
    global dragging_item, dragging_type
    dragging_item = None
    dragging_type = None

# Connect the click, motion, and release events to the handlers
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# Function to compute and display the transfer function
def compute_tf():
    global poles, zeros
    b, a = zpk2tf(zeros, poles, 1)  # Compute transfer function coefficients
    print("Numerator Coefficients (b):", b)
    print("Denominator Coefficients (a):", a)

# Add a button to compute the transfer function
from matplotlib.widgets import Button
ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])
btn_compute = Button(ax_button, 'Compute TF')
btn_compute.on_clicked(lambda event: compute_tf())

# Initial plot update
update_plot()

# Show the plot
plt.show()
