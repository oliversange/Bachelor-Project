import ABP
import numpy as np
import os
import matplotlib.pyplot as plt

# Run ABP predator prey simulation

# Loop over T_As
T_As = [0.1, 1, 10, 20, 30, 40]

for T in T_As:

    # Loop over r_cs
    r_cs= [2, 3, 4, 5]

    for rc in r_cs:

        # Parameters
        D = 0.333
        v_pred = 40.0
        v0 = 26.666666
        D_rot = 1
        mu = 1
        mu_r = 3
        r_c = 2**(1/6)
        T_A = T
        T_0 = 3* T
        T_0_predator = 10
        R_prey = rc * r_c
        R_prey_pred = 3* r_c
        R_pred_prey = 10
        dt = 0.00001
        number_of_steps = 3000000
        number_of_particles = 100
        boundary_condition = True

        # Run
        particles = ABP.ABP(D, v0, v_pred, D_rot, mu, mu_r, T_A, T_0, T_0_predator, R_prey, R_prey_pred, R_pred_prey, dt, number_of_steps, number_of_particles, boundary_condition)
        positions, predator_positions, eatings = particles.simulation()
        output_folder = f'/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_3T_A_R3_run4/simulation_n={number_of_particles}_T_A={T_A}_T_0={T_0}_T_0_predator={T_0_predator}_R={R_prey}_dt={dt}_steps={number_of_steps}_boundary_condition={boundary_condition}'

        # Save results
        os.makedirs(output_folder, exist_ok=True)
        np.save(os.path.join(output_folder, 'prey.npy'), positions)
        np.save(os.path.join(output_folder, 'predator.npy'), predator_positions)
        np.save(os.path.join(output_folder, 'eatings.npy'), eatings)

        # Create histogram
        hist, bins = np.histogram(eatings, bins=20)
        plt.bar(bins[:-1], hist, width=np.diff(bins/2), edgecolor='black')
        plt.xlabel('time')
        plt.ylabel('eatings')
        plt.savefig(os.path.join(output_folder, 'histogram.pdf'))

        del positions
        del predator_positions
        del eatings

