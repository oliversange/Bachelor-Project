import numpy as np
import matplotlib.pyplot as plt
import os
import re
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib as mpl

mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14

class Plots:

    def __init__(self, parent_directories, save_path):

        self.linestyle_dict = {0.1: [':', ':', ':', ':'], 1: [':', ':', '-.', '-.'], 10: ['-.', '--', '-', '-'], 20: ['-.', '--', '-', '-'], 30: ['-.', '-', '-', '-'], 40: ['-.', '-', '-', '-']}
        self.linestyle_name = {':':'cloud', '-.': 'multiple loose groups', '--':'multiple cohesive groups', '-':'one cohesive group'}
        self.fontsize = 15
        self.cmap = plt.cm.viridis
        self.parent_directories = parent_directories
        folder_paths_list = self.get_folder_paths(parent_directories)
        path_dict = self.create_path_dict(folder_paths_list)
        print(path_dict)
        self.save_path = save_path
        self.main_plot(path_dict)

    def get_folder_paths(self, parent_directories):

        folder_paths_list = [[], [], []]

        for i, folder_paths in enumerate(folder_paths_list):
            # Iterate over the directories in the parent directory
            for dirpath, dirnames, filenames in os.walk(parent_directories[i]):
                for dirname in dirnames:
                    folder_paths.append(os.path.join(dirpath, dirname))

        return folder_paths_list

    def create_path_dict(self, folder_paths_list):

        path_dict = {0.1: [[], [], []], 1:[[], [], []], 10:[[], [], []], 20:[[], [], []], 30:[[], [], []], 40:[[], [], []]}
        for i, folder_paths in enumerate(folder_paths_list):
            for path in sorted(folder_paths):
                path_dict[self.det_T_A(path)][i].append(path)

        return path_dict

    def det_T_A(self, file_path):
        # Define a regular expression pattern to find 'R=<float>'
        pattern = r'T_A=([\d.]+)'

        # Search for the pattern in the file path
        match = re.search(pattern, file_path)

        if match:
            return float(match.group(1))

    def det_R(self, file_path):
        # Define a regular expression pattern to find 'R=<float>'
        pattern = r'R=([\d.]+)'

        # Search for the pattern in the file path
        match = re.search(pattern, file_path)

        if match:
            return match.group(1)[0] + r"$r_{\mathrm{c}}$"


    def main_plot(self, path_dict):

        fig = plt.figure(figsize=(15, 10))
        subplot_idx = 1

        for torque in path_dict:
            plt.subplot(2, 3, subplot_idx)
            cmap = plt.cm.viridis
            linestyles = self.linestyle_dict[torque]
            idx = 1

            for i, path in enumerate(sorted(path_dict[torque][0])):
                color = cmap(0.3 * idx)
                R = self.det_R(path)
                linestyle = linestyles[int(R[0])-2]
                #print(path)
                #print(R)
                self.survival_plotter(path_dict[torque], i, R, color, linestyle)

                idx += 1

            #plt.legend(fontsize = self.fontsize)
            plt.ylim((0, 100))
            plt.title(r"$T_{\mathrm{A}}$ = " + str(torque), fontsize=self.fontsize)

            subplot_idx += 1
        #plt.suptitle(r"Survivor functions for the parameters $T_0 = 3T_A$, $R_{\mathrm{prey\_pred}} = 3r_c$", fontsize=16)
        #plt.subplots_adjust(top=0.9)
        plt.tight_layout()
        self.legend(fig)
        plt.savefig(self.save_path)
        plt.show()

    def legend(self, fig):
        custom_lines = [Line2D([0], [0], color='black', linestyle=':', label='cloud'),
                        Line2D([0], [0], color='black', linestyle='-.', label='multiple loose groups'),
                        Line2D([0], [0], color='black', linestyle='--', label='multiple cohesive groups'),
                        Line2D([0], [0], color='black', linestyle='-', label='one cohesive group'),
                        Patch(color=self.cmap(0.3), label=r'$R_{\mathrm{pp}} = 2r_{\mathrm{c}}$'),
                        Patch(color=self.cmap(0.6), label=r'$R_{\mathrm{pp}} = 3r_{\mathrm{c}}$'),
                        Patch(color=self.cmap(0.9), label=r'$R_{\mathrm{pp}} = 4r_{\mathrm{c}}$'),
                        Patch(color=self.cmap(1.2), label=r'$R_{\mathrm{pp}} = 5r_{\mathrm{c}}$')]
        fig.legend(handles = custom_lines,loc='lower center', ncol=4, fontsize=self.fontsize)
        plt.subplots_adjust(bottom=0.15)
    """
    def hist_plotter(self):
        data = np.load(self.selected_folder_path + "eatings.npy")
        hist, bins = np.histogram(data, bins=100000)
        plt.bar(bins[:-1], hist, width=np.diff(bins / 2), edgecolor='black')
        plt.xlabel('time')
        plt.ylabel('eatings')
    """

    def survival_plotter(self, selected_folder_paths, i, label, color, linestyle):
        selected_folder_paths = np.array(selected_folder_paths).T[i]
        total_data = np.array([])
        for selected_folder_path in selected_folder_paths:
            data = np.load(selected_folder_path + "/eatings.npy")
            print(np.shape(data))
            total_data = np.append(total_data, data)
        hist, bin_edges = np.histogram(total_data, bins=100000)

        # Calculate the cumulative sum of the histogram values
        cumulative_hist = 300 - np.cumsum(hist)

        # Plot the cumulative histogram
        plt.plot(bin_edges[:-1], cumulative_hist / 3, c=color, linestyle=linestyle)
        plt.xlabel(r'time t in units of $\tau_{\mathrm{r}}$', fontsize = self.fontsize)
        plt.ylabel('Survivorship function $S(t)$', fontsize = self.fontsize)


parent_dirs_R9 = ['/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R9_run1', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R9_run2', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R9_run3']
parent_dirs_R5 = ['/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R5_run1', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R5_run2', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_R5_run3']
parent_dirs_R3 = ['/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_run1', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_run2', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_2T_A_run3']
parent_dirs_T3 = ['/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_3T_A_R3_run1', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_3T_A_R3_run2', '/Users/oliversange/Desktop/BA_Desktop/Compressed simulations/data_3T_A_R3_run3']

save_path = '/Users/oliversange/Desktop/PLOTS/data_2T_A_R9_average_big_plot.pdf'

A = Plots(parent_dirs_R9, save_path)