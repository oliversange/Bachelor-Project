import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib as mpl

mpl.rcParams['xtick.labelsize'] = 13
mpl.rcParams['ytick.labelsize'] = 13

def plot_simulation_image(simulation_path, save_path, timestep):
    prey = np.load(os.path.join(simulation_path, 'prey.npy'))
    predator = np.load(os.path.join(simulation_path, 'predator.npy'))

    x_prey = prey[0, timestep]
    y_prey = prey[1, timestep]
    print(x_prey)

    x_predator = predator[0, timestep]
    y_predator = predator[1, timestep]
    fontsize = 15
    cmap = plt.cm.viridis
    plt.figure(figsize=(8, 8))
    plt.scatter(x_prey, y_prey, c=cmap(0.2), label='prey particles')
    plt.scatter(x_predator, y_predator, c=cmap(0.6), label='predator particle')
    plt.arrow(x_predator[0], y_predator[0], 0, 10, head_width=0.2, head_length=0.2, color = cmap(1.2), label=r'Predator-prey interaction range $R_{\mathrm{P}}$')
    plt.arrow(x_predator[0], y_predator[0]+ 10, 0, -9.8, head_width=0.2, head_length=0.2, color=cmap(1.2))
    plt.legend(fontsize=fontsize)
    plt.xlabel(r'x coordinates in units of $\sigma$', fontsize=fontsize)
    plt.ylabel(r'y coordinates in units of $\sigma$', fontsize=fontsize)
    #plt.xlim(0, 175)
    #plt.ylim(0, 175)
    plt.gca().set_aspect('equal')
    plt.savefig(save_path)
    plt.show()




simulation_path = '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_run1/simulation_n=100_T_A=20_T_0=40_T_0_predator=10_R=4.489848193237492_dt=1e-05_steps=3000000_boundary_condition=True'
save_path = '/Users/oliversange/Desktop/PLOTS/setup_with_predator.pdf'
timestep = 101000
plot_simulation_image(simulation_path, save_path, int(timestep/1000))