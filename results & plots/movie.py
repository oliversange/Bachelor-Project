import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import re
import matplotlib as mpl

mpl.rcParams['xtick.labelsize'] = 13
mpl.rcParams['ytick.labelsize'] = 13

size = 175
cmap = plt.get_cmap("inferno")

def update(frame):
    global size
    global selected_folder
    plt.clf()  # Clear the previous frame
    for i in range(len(x_values[0])):
        plt.plot(x_values[frame, i], y_values[frame, i], marker='o', markersize=500/size, color=cmap(0.2))

    plt.plot(x_values[frame, 0], y_values[frame, 0], marker='o', markersize=500 / size, label='Prey', color=cmap(0.2))

    plt.plot(predator_x[frame], predator_y[frame], marker='o', markersize=800/size, label='Predator', color=cmap(0.6))
    fontsize = 15
    # plot
    plt.xlabel(r'x coordinates in units of $\sigma$', fontsize=fontsize)
    plt.ylabel(r'y coordinates in units of $\sigma$', fontsize=fontsize)
    plt.gca().set_aspect('equal')
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.gca().set_aspect('equal')

    plt.legend(fontsize=fontsize, loc='upper right')

    # info text
    info_text = f'T_A={selected_folder[21:24]}\nT_0={selected_folder[29:32]}\nT_0={selected_folder[47:49]}'
    """
    plt.text(15, 170, info_text, fontsize=10, ha='center', va='top', bbox=dict(facecolor='lightgray', alpha=0.5))
    plt.legend(loc='upper right')
    """

def get_simulation_folders(base_path):
    simulation_folders = [folder for folder in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder))]
    return simulation_folders

def select_simulation_folder(simulation_folders):
    print("Available simulation folders:")
    for i, folder in enumerate(simulation_folders, start=1):
        print(f"{i}. {folder}")

    while True:
        try:
            selected_index = int(input("Select a folder by entering its number: "))
            selected_folder = simulation_folders[selected_index - 1]
            return selected_folder
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid folder number.")

def plot_animation(folder_path):
    # Load arrays from the specified folder
    prey_s_path = os.path.join(folder_path, 'prey.npy')
    predator_s_path = os.path.join(folder_path, 'predator.npy')
    eatings_s_path = os.path.join(folder_path, 'eatings.npy')

    positions = np.load(prey_s_path)
    predator_positions = np.load(predator_s_path)
    eatings = np.load(eatings_s_path)

    global x_values, y_values, predator_x, predator_y
    x_values = np.array(positions[0])
    y_values = np.array(positions[1])
    predator_x = predator_positions[0]
    predator_y = predator_positions[1]

    fig, ax = plt.subplots(figsize=(8, 8))  # Set figure size to better fit the plot
    ani = FuncAnimation(fig, update, frames=range(0, len(x_values), 1), interval=2, repeat=False)


    # Save the animation as an MP4 video with tight layout
    output_path = '/Users/oliversange/Desktop/BA Verteidigung plots/optimum.mp4'
    ani.save(output_path, writer='ffmpeg', fps=30, dpi=200, savefig_kwargs={'bbox_inches': 'tight', 'pad_inches': 0})

    plt.show()

# Example usage:
base_simulation_path = '/Users/oliversange/Library/Mobile Documents/com~apple~CloudDocs/Physikstudium/BA/BA_Desktop/Compressed simulations/data_2T_A_run1'
simulation_folders = sorted(get_simulation_folders(base_simulation_path))

if not simulation_folders:
    print("2T_A Cloud")
else:
    selected_folder = select_simulation_folder(simulation_folders)
    selected_folder_path = os.path.join(base_simulation_path, selected_folder)
    plot_animation(selected_folder_path)

