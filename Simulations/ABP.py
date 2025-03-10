import numpy as np
from tqdm import tqdm

# Class for simulating ABP swarm chased by predator
class ABP:
    def __init__(self, D, v0, v_pred, D_rot, mu, mu_r, T_A, T_0, T_0_predator, R_prey, R_prey_pred, R_pred_prey, dt, number_of_steps, number_of_particles, boundary_condition):

        self.D = D
        self.v0 = v0
        self.v_pred = v_pred
        self.D_rot = D_rot
        self.dt = dt
        self.mu = mu
        self.mu_r = mu_r
        self.R_prey = R_prey
        self.R_prey_pred = R_prey_pred
        self.R_pred_prey = R_pred_prey
        self.T_A = T_A
        self.T_0 = T_0
        self.T_0_predator = T_0_predator
        self.number_of_steps = number_of_steps + 1
        self.number_of_particles = number_of_particles
        self.boundary_condition = boundary_condition
        self.L = 175
        self.eating_rate = 0
        self.eatings = []
        self.passed_time = 0

    def distance(self, a, b):
        return np.sqrt(a**2 + b**2)

    def calculate_prey_starting_parameters(self):

        # Initial condition

        rc = 2 ** (1 / 6)

        """
        x = np.zeros(self.number_of_particles)
        y = np.zeros(self.number_of_particles)
        theta = np.zeros(self.number_of_particles)
        r0 = 87.5
        x[0] = r0
        y[0] = r0
        theta[0] = 0
        num = 1

        for r in range(1, 19):
            for i in range(6 * r):
                if num < self.number_of_particles:
                    x[num] = r0 + r * rc * np.cos(i * 2 * np.pi / (6 * r) + (r - 1) * np.pi / 6)
                    y[num] = r0 + r * rc * np.sin(i * 2 * np.pi / (6 * r) + (r - 1) * np.pi / 6)
                    theta[num] = (i * 2 * np.pi / (6 * r) + (r - 1) * np.pi / 6) - np.pi
                    num += 1
                else:
                    break
        theta = (theta + np.pi) % (2 * np.pi) - np.pi
        """
        grid_size=10
        spacing=2
        center=175 / 2
        x = np.linspace(center - (grid_size // 2) * spacing, center + (grid_size // 2) * spacing, grid_size)
        y = np.linspace(center - (grid_size // 2) * spacing, center + (grid_size // 2) * spacing, grid_size)
        x, y = np.meshgrid(x, y)
        theta = np.random.uniform(0, 2 * np.pi, 100)
        return x.flatten(), y.flatten(), theta

    def calculate_predator_starting_parameters(self, number, x, y):
        if number == 1:
            pred_x = np.random.uniform(80000000, 81000000, 1)
            pred_y = np.random.uniform(80000000, 81000000, 1)
            pred_theta = np.random.uniform(np.pi / 4, np.pi / 4, 1)
        if number == 2:
            pred_x = np.array([np.sum(x) / self.number_of_particles])
            pred_y = np.array([np.sum(y) / self.number_of_particles - self.R_pred_prey])
            pred_theta = np.array([np.pi/2])
        return pred_x, pred_y, pred_theta

    def simulation(self):

        # Prey starting parameters
        x, y, theta = self.calculate_prey_starting_parameters()

        # Predator starting parameters
        pred_x, pred_y, pred_theta = self.calculate_predator_starting_parameters(1, x, y)

        #run simulation
        return self.simulate(x, y, theta, pred_x, pred_y, pred_theta)

    def simulate(self, x, y, theta, pred_x, pred_y, pred_theta):
        x_list = []
        y_list = []
        theta_list = []
        pred_x_list = []
        pred_y_list = []
        pred_theta_list = []
        steps = 0

        for step in tqdm(range(1, self.number_of_steps), desc='Running simulation', unit='timestep'):

            # Save variables
            if step % 1000 == 0:

                x_list.append(np.copy(x))
                y_list.append(np.copy(y))
                theta_list.append(np.copy(theta))

                pred_x_list.append(np.copy(pred_x))
                pred_y_list.append(np.copy(pred_y))
                pred_theta_list.append(np.copy(pred_theta))

            # Clock
            self.passed_time += self.dt

            # Calculate position
            WCA = self.WCA(x, y)
            x_change = self.v0 * np.cos(theta) * self.dt + np.sqrt(2 * self.D * self.dt) * np.random.randn(
                self.number_of_particles) + self.mu * WCA[0] * self.dt
            y_change = self.v0 * np.sin(theta) * self.dt + np.sqrt(2 * self.D * self.dt) * np.random.randn(
                self.number_of_particles) + self.mu * WCA[1] * self.dt

            pred_x_change = (self.v_pred * np.cos(pred_theta) * self.dt + np.sqrt(
                2 * self.D * self.dt) * np.random.randn(1))
            pred_y_change = (self.v_pred * np.sin(pred_theta) * self.dt + np.sqrt(
                2 * self.D * self.dt) * np.random.randn(1))

            theta_change = self.mu_r * self.det_T(x, y, theta, pred_x, pred_y, pred_theta) * self.dt + np.sqrt(2 * self.D_rot * self.dt) * np.random.randn(self.number_of_particles)
            pred_theta_change = self.mu_r * self.det_pred_T(x, y, theta, pred_x, pred_y, pred_theta) * self.dt + np.sqrt(2 * self.D_rot * self.dt) * np.random.randn(1)

            x += x_change
            y += y_change
            pred_x += pred_x_change
            pred_y += pred_y_change
            theta += theta_change
            pred_theta += pred_theta_change

            # introduce predator
            if steps == 100000:
                pred_x, pred_y, pred_theta = self.calculate_predator_starting_parameters(2, x, y)
            steps += 1

            # apply boundary condition
            if self.boundary_condition:
                #change coordinates according to boundary condition
                x = np.where(x > self.L, x - self.L, np.where(x < 0, x + self.L, x))
                y = np.where(y > self.L, y - self.L, np.where(y < 0, y + self.L, y))
                pred_x = np.where(pred_x > self.L, pred_x - self.L, np.where(pred_x < 0, pred_x + self.L, pred_x))
                pred_y = np.where(pred_y > self.L, pred_y - self.L, np.where(pred_y < 0, pred_y + self.L, pred_y))

        return (np.array([x_list, y_list]), np.array([pred_x_list, pred_y_list]),
                np.array(self.eatings))

    def det_T(self, x, y, theta, pred_x, pred_y, pred_theta):

        # Determine the Prey-Prey-Term
        x_m = np.tile(x, (self.number_of_particles, 1))
        y_m = np.tile(y, (self.number_of_particles, 1))
        theta_matrix = np.tile(theta, (self.number_of_particles, 1))

        # Calculate distance in x and y coordinates
        dx = x_m - x_m.T
        dy = y_m - y_m.T
        delta_theta = theta_matrix - theta_matrix.T

        #apply boundary condition
        if self.boundary_condition:
            dx = np.where(dx > 0.5 * 175, dx - 175, np.where(dx < -0.5 * 175, dx + 175, dx))
            dy = np.where(dy > 0.5 * 175, dy - 175, np.where(dy < -0.5 * 175, dy + 175, dy))

        # Calculate the distances between particles
        distances = self.distance(dx, dy)

        # Exclude the diagonal elements (i == j)
        np.fill_diagonal(distances, np.inf)

        u = np.column_stack((np.cos(theta), np.sin(theta)))
        u_n = u / np.linalg.norm(u)
        cp = (u_n[:, 0, np.newaxis] * dy - u_n[:, 1, np.newaxis] * dx) / distances

        # Calculate the Prey-Prey-Term
        prey_term = self.T_A * np.sum(np.where((self.R_prey - distances) > 0, 1, 0) * (np.sin(delta_theta) + 0.5 * cp), axis=1)

        # calculate Predator-Prey distances in x and y coordinates
        distance_pred_particle_x = x - pred_x
        distance_pred_particle_y = y - pred_y

        # apply boundary condition
        if self.boundary_condition:
            distance_pred_particle_x = np.where(distance_pred_particle_x > 0.5 * 175, distance_pred_particle_x - 175, np.where(distance_pred_particle_x < -0.5 * 175, distance_pred_particle_x + 175, distance_pred_particle_x))
            distance_pred_particle_y = np.where(distance_pred_particle_y > 0.5 * 175, distance_pred_particle_y - 175, np.where(distance_pred_particle_y < -0.5 * 175, distance_pred_particle_y + 175, distance_pred_particle_y))

        #calculate distance
        pred_distance = self.distance(distance_pred_particle_x, distance_pred_particle_y)

        pred_cp = np.cos(pred_theta) * distance_pred_particle_y - np.sin(pred_theta) * distance_pred_particle_x

        # Calculate the Predator-Prey-Term
        predator_term = self.T_0 * np.where((self.R_prey_pred - pred_distance) > 0, 1, 0) * (pred_cp / pred_distance)

        T = prey_term + predator_term
        return T

    def det_pred_T(self, x, y, theta, pred_x, pred_y, pred_theta):

        #calculate distance in x and y coordinates
        pred_prey_x = x - pred_x
        pred_prey_y = y - pred_y
        if self.boundary_condition:
            pred_prey_x = np.where(pred_prey_x > 0.5 * 175, pred_prey_x - 175, np.where(pred_prey_x < -0.5 * 175, pred_prey_x + 175, pred_prey_x))
            pred_prey_y = np.where(pred_prey_y > 0.5 * 175, pred_prey_y - 175, np.where(pred_prey_y < -0.5 * 175, pred_prey_y + 175, pred_prey_y))

        #calculate distance
        pred_prey_x_y = self.distance(pred_prey_x, pred_prey_y)

        #eating mechanism
        bed = pred_prey_x_y < 1.0
        x[bed] += 1000000000000
        if np.any(x[bed]):
            self.eatings.append(self.passed_time)

        # Calculate cross product components
        pred_cp = np.cos(pred_theta) * pred_prey_y - np.sin(pred_theta) * pred_prey_x

        # Calculate T_P_j
        T_P_j = self.T_0_predator * np.sum(np.where(pred_prey_x_y < self.R_pred_prey, 1.0, 0.0) * (pred_cp / pred_prey_x_y))

        return T_P_j

    def WCA(self, x, y):
        x_m = np.tile(x, (self.number_of_particles, 1))
        y_m = np.tile(y, (self.number_of_particles, 1))

        # Calculate the differences in x and y coordinates
        dx = x_m - x_m.T
        dy = y_m - y_m.T

        # apply boundary condition
        if self.boundary_condition:
            dx = np.where(dx > 0.5 * 175, dx - 175, np.where(dx < -0.5 * 175, dx + 175, dx))
            dy = np.where(dy > 0.5 * 175, dy - 175, np.where(dy < -0.5 * 175, dy + 175, dy))

        r_ij = self.distance(dx, dy)

        #fill diagonals
        np.fill_diagonal(r_ij, np.inf)
        np.fill_diagonal(dx, 0)
        np.fill_diagonal(dy, 0)

        force_x_i = -1 * np.sum(np.where(r_ij < 2**(1/6), 1.0, 0.0) * dx * 4800 * (1 / r_ij ** 14 - 0.5 * 1 / r_ij ** 8), axis=1)
        force_y_i = -1 * np.sum(np.where(r_ij < 2**(1/6), 1.0, 0.0) * dy * 4800 * (1 / r_ij ** 14 - 0.5 * 1 / r_ij ** 8), axis=1)

        return [force_x_i, force_y_i]
