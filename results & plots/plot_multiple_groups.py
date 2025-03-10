import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib as mpl

def plot_simulation_image(simulation_path, save_path, timestep):

    # Load data
    prey = np.load(os.path.join(simulation_path, 'prey.npy'))
    predator = np.load(os.path.join(simulation_path, 'predator.npy'))

    # Extract positions
    x_prey = prey[0, timestep]
    y_prey = prey[1, timestep]
    x_predator = predator[0, timestep]
    y_predator = predator[1, timestep]

    # Plotting
    fontsize = 15
    cmap = plt.cm.viridis
    plt.figure(figsize=(8, 8))
    plt.scatter(x_prey, y_prey, c=cmap(0.2), label='prey particles', s = 5)
    #plt.scatter(x_predator, y_predator, c=cmap(0.6), label='predator particle')
    #plt.arrow(x_predator[0], y_predator[0], 0, 10, head_width=0.2, head_length=0.2, color = cmap(1.2), label=r'Predator-prey interaction range $R_{\mathrm{P}}$')
    #plt.arrow(x_predator[0], y_predator[0]+ 10, 0, -9.8, head_width=0.2, head_length=0.2, color=cmap(1.2))
    plt.legend(fontsize=fontsize, loc="upper right")
    plt.xlabel(r'x coordinates in units of $\sigma$', fontsize=fontsize)
    plt.ylabel(r'y coordinates in units of $\sigma$', fontsize=fontsize)
    plt.xlim(0, 175)
    plt.ylim(0, 175)
    plt.gca().set_aspect('equal')
    plt.savefig(save_path)
    plt.show()


if __name__=='__main__':

    # Plot simulation situation
    mpl.rcParams['xtick.labelsize'] = 14
    mpl.rcParams['ytick.labelsize'] = 14
    simulation_path = '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_run1/simulation_n=100_T_A=20_T_0=40_T_0_predator=10_R=2.244924096618746_dt=1e-05_steps=3000000_boundary_condition=True'
    save_path = '/Users/oliversange/Desktop/PLOTS/prey_multiple_groups.pdf'
    timestep = 210000
    plot_simulation_image(simulation_path, save_path, int(timestep/1000))