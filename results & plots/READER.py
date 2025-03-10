import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import matplotlib as mpl

class Reader_Plotter:

    def __init__(self, parent_dirs, title, save_path):
        self.title = title
        self.shape_dict = {0.1: ['h', 'h', 'h', 'h'], 1: ['h', 'h', 'p', 'p'], 10: ['p', 's', '^', '^'], 20: ['p', 's', '^', '^'], 30: ['p', '^', '^', '^'], 40: ['p', '^', '^', '^']}
        self.cmap = plt.cm.viridis
        self.marker_size = 75
        self.color_dict = my_dict = {'h':self.cmap(0.8), 'p':self.cmap(0.6), 's':self.cmap(0.4), '^':self.cmap(0.2)}
        self.fontsize = 13
        eatings_dict, proximity_dict, distance_dict = self.get_data(parent_dirs)
        self.save_path = save_path
        self.plot_eatings_over_proximity(eatings_dict, proximity_dict, distance_dict)

    def path_reader(self, parent_dir):
        folder_paths = []
        for dirpath, dirnames, filenames in os.walk(parent_dir):
            for dirname in dirnames:
                folder_paths.append(os.path.join(dirpath, dirname))
        return folder_paths

    def get_data(self, parent_dirs):
        eatings_dicts = []
        proximity_dicts = []
        distance_dicts = []
        for parent_dir in parent_dirs:
            folder_paths = self.path_reader(parent_dir)
            eatings_dict, proximity_dict, distance_dict = self.data_shower(folder_paths)
            eatings_dicts.append(eatings_dict)
            proximity_dicts.append(proximity_dict)
            distance_dicts.append(distance_dict)
        av_eatings = self.average_calculator(eatings_dicts)
        av_proximity = self.average_calculator(proximity_dicts)
        av_distance = self.average_calculator(distance_dicts)
        print(eatings_dicts)
        print(av_eatings)

        return av_eatings, av_proximity, av_distance

    def average_calculator(self, dict_list):
        average_dict = {}
        for key in dict_list[0].keys():
            average_dict[key] = [(dict_list[0][key][i] + dict_list[1][key][i] + dict_list[2][key][i]) / 3 for i in range(len(dict_list[0][key]))]
        return  average_dict

    def data_shower(self, folder_paths):

        eatings_dict = {0.1: [0, 0, 0, 0], 1: [0, 0, 0, 0], 10: [0, 0, 0, 0], 20: [0, 0, 0, 0], 30: [0, 0, 0, 0], 40: [0, 0, 0, 0]}
        proximity_dict = {0.1: [0, 0, 0, 0], 1: [0, 0, 0, 0], 10: [0, 0, 0, 0], 20: [0, 0, 0, 0], 30: [0, 0, 0, 0], 40: [0, 0, 0, 0]}
        distance_dict = {0.1: [0, 0, 0, 0], 1: [0, 0, 0, 0], 10: [0, 0, 0, 0], 20: [0, 0, 0, 0], 30: [0, 0, 0, 0], 40: [0, 0, 0, 0]}

        for path in folder_paths:
            eatings = np.size(np.load(os.path.join(path, "eatings.npy")))
            proximity = float(np.load(os.path.join(path, "particles_in_proximity.npy")))
            distance = float(np.load(os.path.join(path, "distance.npy")))
            _, params = os.path.split(path)
            params = params.split('_')

            for param in params:
                if param.startswith("A="):
                    t_a = param.split('=')[1]
                if param.startswith("R="):
                    r = param.split('=')[1]
            eatings_dict[float(t_a)][int(r[0])-2] = eatings
            proximity_dict[float(t_a)][int(r[0]) - 2] = proximity
            distance_dict[float(t_a)][int(r[0]) - 2] = distance

        #print(eatings_dict)
        #print(proximity_dict)
        #print(distance_dict)

        return [eatings_dict, proximity_dict, distance_dict]

    def plot_eatings_over_proximity(self, eatings_dict, proximity_dict, distance_dict):
        print(eatings_dict)
        #print(proximity_dict)
        eatings = []
        proximity = []
        distance = []
        shapes = []

        for key in eatings_dict:
            for i in eatings_dict[key]:
                eatings.append(i)
        for key in self.shape_dict:
            for i in self.shape_dict[key]:
                shapes.append(i)
        for key in proximity_dict:
            for i in proximity_dict[key]:
                proximity.append(i)
        for key in distance_dict:
            for i in distance_dict[key]:
                distance.append(i)
        print(eatings_dict)
        # Create a figure and two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        # Plot data on the first subplot
        self.plot_first_plot(ax1, shapes, eatings, proximity)

        # Plot data on the second subplot
        self.plot_second_plot(ax2, shapes, eatings, distance)

        #fig.suptitle(self.title, fontsize=16)
        #plt.tight_layout(rect=[0, 0, 1, 0.98])  # Adjust rect to fit the suptitle
        plt.tight_layout()
        plt.grid()
        plt.savefig(self.save_path)
        plt.show()

    def plot_first_plot(self, ax1, shapes, eatings, proximity):
        idx_h = 0
        idx_p = 0
        idx_s = 0
        idx_t = 0
        for i, shape in enumerate(shapes):
            if shape == '^' and idx_t == 0:
                ax1.scatter(proximity[i], eatings[i], c=self.cmap(0.2), marker=shape, label='one cohesive group', s=self.marker_size)
                idx_t += 1
            if shape == 's' and idx_s == 0:
                ax1.scatter(proximity[i], eatings[i], c=self.cmap(0.4), marker=shape, label='multiple cohesive groups', s=self.marker_size)
                idx_s += 1
            if shape == 'p' and idx_p == 0:
                ax1.scatter(proximity[i], eatings[i], c=self.cmap(0.6), marker=shape, label='multiple loose groups', s=self.marker_size)
                idx_p += 1
            if shape == 'h' and idx_h == 0:
                ax1.scatter(proximity[i], eatings[i], c=self.cmap(0.8), marker=shape, label='cloud', s=self.marker_size)
                idx_h += 1
            ax1.scatter(proximity[i], eatings[i], c=self.color_dict[shape], marker=shape, s=self.marker_size)

        ax1.set_xlabel(r'proximity parameter $P$', fontsize=self.fontsize)
        ax1.set_ylabel(r'total number of eating events $N_{\mathrm{E}}$', fontsize=self.fontsize)
        ax1.set_ylim(0, 100)
        ax1.legend(fontsize=self.fontsize)
        ax1.grid()

    def plot_second_plot(self, ax2, shapes, eatings, distance):
        idx_h = 0
        idx_p = 0
        idx_s = 0
        idx_t = 0
        for i, shape in enumerate(shapes):
            if shape == '^' and idx_t == 0:
                ax2.scatter(distance[i], eatings[i], c=self.cmap(0.2), marker=shape, label='one cohesive group', s=self.marker_size)
                idx_t += 1
            if shape == 's' and idx_s == 0:
                ax2.scatter(distance[i], eatings[i], c=self.cmap(0.4), marker=shape, label='multiple cohesive groups', s=self.marker_size)
                idx_s += 1
            if shape == 'p' and idx_p == 0:
                ax2.scatter(distance[i], eatings[i], c=self.cmap(0.6), marker=shape, label='multiple loose groups', s=self.marker_size)
                idx_p += 1
            if shape == 'h' and idx_h == 0:
                ax2.scatter(distance[i], eatings[i], c=self.cmap(0.8), marker=shape, label='cloud', s=self.marker_size)
                idx_h += 1
            ax2.scatter(distance[i], eatings[i], c=self.color_dict[shape], marker=shape, s=self.marker_size)

        ax2.set_xlabel(r'average particle distance D in units of $\sigma$', fontsize=self.fontsize)
        ax2.set_ylabel(r'total number of eating events $N_{\mathrm{E}}$', fontsize=self.fontsize)
        ax2.set_ylim(0, 100)
        ax2.legend(fontsize=self.fontsize)

if __name__ == "__main__":

    # Create plot from simulation data

    # Plot parameters
    mpl.rcParams['xtick.labelsize'] = 12
    mpl.rcParams['ytick.labelsize'] = 12

    # Specify paths
    parent_dirs_T3 = ['/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_3T_A_R3_run1', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_3T_A_R3_run2', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_3T_A_R3_run3']
    parent_dirs_R3 = ['/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_run1', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_run2', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_run3']
    parent_dirs_R5 = ['/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R5_run1', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R5_run2', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R5_run3']
    parent_dirs_R9 = ['/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R9_run1', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R9_run2', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R9_run3']

    # Title
    title = r'$T_{\mathrm{0}} = 2T_{\mathrm{A}}$, $R_{\mathrm{p}} = 3 r_{\mathrm{c}}$'

    # Plot and save
    save_path = '/Users/oliversange/Desktop/PLOTS/T0=3TA_R=3rc_average.pdf'
    Reader_Plotter(parent_dirs_T3, title, save_path)

