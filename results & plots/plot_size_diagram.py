import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

def plot_size_overview(eatings_dict, save_path):

    cmap = plt.cm.viridis
    fontsize = 14
    marker_size = 150
    shape_dict = {0.1: ['h', 'h', 'h', 'h'], 1: ['h', 'h', 'p', 'p'], 10: ['p', 's', '^', '^'], 20: ['p', 's', '^', '^'], 30: ['p', '^', '^', '^'], 40: ['p', '^', '^', '^']}
    my_dict = {'h':cmap(0.8), 'p':cmap(0.6), 's':cmap(0.4), '^':cmap(0.2)}

    idx_h = 0
    idx_p = 0
    idx_s = 0
    idx_t = 0

    for torque in shape_dict:
        for i, shape in enumerate(shape_dict[torque]):
            if shape == '^' and idx_t == 0:
                plt.scatter(torque, i + 2, c=cmap(0.2), marker=shape, label='one group', s=80)
                idx_t += 1
            if shape == 's' and idx_s == 0:
                plt.scatter(torque, i + 2, c=cmap(0.4), marker=shape, label='multiple cohesive groups', s=80)
                idx_s += 1
            if shape == 'p' and idx_p == 0:
                plt.scatter(torque, i + 2, c=cmap(0.6), marker=shape, label='multiple loose groups', s=80)
                idx_p += 1
            if shape == 'h' and idx_h == 0:
                plt.scatter(torque, i + 2, c=cmap(0.8), marker=shape, label='cloud', s=80)
                idx_h += 1
            plt.scatter(torque, i + 2, marker=shape, c = my_dict[shape], s=eatings_dict[torque][i]**3/1000)

    line1_x = [0.4, 0.4, 4, 4]
    line1_y = [6, 3.5, 3.5, 1]
    plt.plot(line1_x, line1_y, c=cmap(0.8))

    line2_x = [4, 4, 40]
    line2_y = [6, 2.5, 2.5]
    plt.plot(line2_x, line2_y, c=cmap(0.6))

    line3_x = [4, 4, 25, 25, 60]
    line3_y = [5, 3.5, 3.5, 2.5, 2.5]
    plt.plot(line3_x, line3_y, c=cmap(0.4))

    # Adjust the layout to make room for the legend
    plt.subplots_adjust(top=0.85)
    plt.xscale('log')
    plt.xlabel(r'prey-prey interaction torque $T_{\mathrm{A}}$', fontsize=fontsize)
    plt.ylabel(r'prey-prey interaction radius $R_{\mathrm{pp}}$ in $r_{\mathrm{c}}$', fontsize=fontsize)
    plt.ylim(1.8, 5.2)
    plt.xlim(0.08, 50)
    plt.legend(loc='upper center', fontsize=fontsize, bbox_to_anchor=(0.5, 1.25), ncol=2)
    plt.savefig(save_path)
    plt.show()

if __name__=='__main__':

    # Plot size diagram

    mpl.rcParams['xtick.labelsize'] = 13
    mpl.rcParams['ytick.labelsize'] = 13

    eatings_R3 = {0.1: [51.666666666666664, 52.666666666666664, 56.0, 64.33333333333333], 1: [49.0, 58.333333333333336, 68.33333333333333, 81.0], 10: [48.333333333333336, 57.333333333333336, 69.33333333333333, 80.0], 20: [60.666666666666664, 70.33333333333333, 57.333333333333336, 82.33333333333333], 30: [59.333333333333336, 65.33333333333333, 59.333333333333336, 79.0], 40: [43.666666666666664, 31.333333333333332, 60.0, 84.33333333333333]}
    eatings_R5 = {0.1: [45.0, 46.666666666666664, 37.333333333333336, 40.0], 1: [39.666666666666664, 44.333333333333336, 48.333333333333336, 55.666666666666664], 10: [52.666666666666664, 35.666666666666664, 44.666666666666664, 61.666666666666664], 20: [56.333333333333336, 41.0, 70.66666666666667, 60.0], 30: [59.333333333333336, 54.333333333333336, 37.666666666666664, 66.0], 40: [58.0, 58.666666666666664, 59.666666666666664, 71.33333333333333]}
    eatings_R9 = {0.1: [45.666666666666664, 44.666666666666664, 48.666666666666664, 51.333333333333336], 1: [42.333333333333336, 43.0, 46.333333333333336, 44.0], 10: [58.0, 50.0, 57.0, 36.333333333333336], 20: [70.66666666666667, 74.66666666666667, 72.66666666666667, 65.33333333333333], 30: [79.33333333333333, 43.333333333333336, 72.33333333333333, 86.0], 40: [78.0, 85.33333333333333, 92.66666666666667, 74.33333333333333]}
    eatings_T3 = {0.1: [45.0, 52.0, 46.333333333333336, 52.0], 1: [46.666666666666664, 48.333333333333336, 57.0, 56.333333333333336], 10: [50.666666666666664, 48.666666666666664, 59.0, 50.333333333333336], 20: [40.333333333333336, 52.666666666666664, 41.333333333333336, 57.666666666666664], 30: [58.666666666666664, 55.0, 62.666666666666664, 61.333333333333336], 40: [53.666666666666664, 50.333333333333336, 64.66666666666667, 57.666666666666664]}

    save_path = '/Users/oliversange/Desktop/PLOTS/size_diagram_T3.pdf'
    plot_size_overview(eatings_T3, save_path)