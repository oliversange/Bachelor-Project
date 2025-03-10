import numpy as np
import os
import re

# Calculate proximity within prey swarm
class Proximties:

    def __init__(self, parent_directory):
        self.subfolders = self.list_subfolders(parent_directory)
        self.det_proximity(self.subfolders)


    def list_subfolders(self, folder_path):
        subfolders = [os.path.join(folder_path, name) for name in os.listdir(folder_path)
                      if os.path.isdir(os.path.join(folder_path, name))]
        return subfolders


    def det_R(self, file_path):
        # Define a regular expression pattern to find 'R=<float>'
        pattern = r'R=([\d.]+)'

        # Search for the pattern in the file path
        match = re.search(pattern, file_path)

        if match:
            # Extract the float value from the match group
            return float(match.group(1))
        else:
            # Return None or raise an error if the pattern is not found
            raise ValueError("The pattern 'R=<float>' was not found in the file path.")

    def distance(self, a, b):
        return np.sqrt(a**2 + b**2)


    def det_proximity(self, subfolders):

        for subfolder in subfolders:
            file_path = os.path.join(subfolder, "prey.npy")
            distance_save_path = os.path.join(subfolder, "distance.npy")
            prox_number_save_path = os.path.join(subfolder, "particles_in_proximity.npy")

            print(file_path)
            data = np.load(file_path)

            R = self.det_R(file_path)

            x_positions = data[0]
            y_positions = data[1]

            particle_distance_cum = 0
            particles_in_prox_cum = 0

            for i, x in enumerate(x_positions):
                y = y_positions[i]
                eaten_particles_mask = x < 1000
                x_masked = x[eaten_particles_mask]
                y_masked = y[eaten_particles_mask]
                prey_size = np.size(x_masked)

                x_m = np.tile(x_masked, (prey_size, 1))
                y_m = np.tile(y_masked, (prey_size, 1))

                # Calculate the differences in x and y coordinates
                dx = x_m - x_m.T
                dy = y_m - y_m.T

                # apply boundary condition
                dx_bc = np.where(dx > 0.5 * 175, dx - 175, np.where(dx < -0.5 * 175, dx + 175, dx))
                dy_bc = np.where(dy > 0.5 * 175, dy - 175, np.where(dy < -0.5 * 175, dy + 175, dy))

                r_ij = self.distance(dx_bc, dy_bc)

                # fill diagonals
                np.fill_diagonal(r_ij, 0)

                # Calculate the average distance
                sum_distances = np.sum(r_ij)
                num_distances = prey_size * (prey_size - 1)  # Number of unique off-diagonal elements

                particle_distance = sum_distances / num_distances

                # Calculate the average number of particles within distance R
                neighbor_counts = np.sum(r_ij < R, axis=1)  # Count neighbors within distance R for each particle
                particles_in_prox = np.mean(neighbor_counts) - 1  # Subtract 1 to exclude self

                particles_in_prox_cum += particles_in_prox
                particle_distance_cum += particle_distance

            av_particles_in_prox = particles_in_prox_cum / 3000
            av_particle_distance = particle_distance_cum / 3000

            print(av_particles_in_prox)
            print(av_particle_distance)

            np.save(prox_number_save_path, av_particles_in_prox)
            np.save(distance_save_path, av_particle_distance)



if __name__ == "__main__":

    parent_directory = "/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_3T_A_R3_run3"

    Proximties(parent_directory)

