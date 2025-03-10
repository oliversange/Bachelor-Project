import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# Create state diagram plot

# Parameters
mpl.rcParams['xtick.labelsize'] = 13
mpl.rcParams['ytick.labelsize'] = 13
cmap = plt.cm.viridis
fontsize = 14
marker_size = 150
shape_dict = {0.1: ['h', 'h', 'h', 'h'], 1: ['h', 'h', 'p', 'p'], 10: ['p', 's', '^', '^'], 20: ['p', 's', '^', '^'], 30: ['p', '^', '^', '^'], 40: ['p', '^', '^', '^']}
my_dict = {'h':cmap(0.8), 'p':cmap(0.6), 's':cmap(0.4), '^':cmap(0.2)}
idx_h = 0
idx_p = 0
idx_s = 0
idx_t = 0

# Plot states
for torque in shape_dict:
    for i, shape in enumerate(shape_dict[torque]):
        if shape == '^' and idx_t == 0:
            plt.scatter(torque, i + 2, c=cmap(0.2), marker=shape, label='one group', s=marker_size)
            idx_t += 1
        if shape == 's' and idx_s == 0:
            plt.scatter(torque, i + 2, c=cmap(0.4), marker=shape, label='multiple cohesive groups', s=marker_size)
            idx_s += 1
        if shape == 'p' and idx_p == 0:
            plt.scatter(torque, i + 2, c=cmap(0.6), marker=shape, label='multiple loose groups', s=marker_size)
            idx_p += 1
        if shape == 'h' and idx_h == 0:
            plt.scatter(torque, i + 2, c=cmap(0.8), marker=shape, label='cloud', s=marker_size)
            idx_h += 1
        plt.scatter(torque, i + 2, marker=shape, c = my_dict[shape], s=marker_size)

# Add separation lines
line1_x = [0.4, 0.4, 4, 4]
line1_y = [6, 3.5, 3.5, 1]
plt.plot(line1_x, line1_y, c=cmap(0.8))

line2_x = [4, 4, 40]
line2_y = [6, 2.5, 2.5]
plt.plot(line2_x, line2_y, c=cmap(0.6))

line3_x = [4, 4, 25, 25, 60]
line3_y = [5, 3.5, 3.5, 2.5, 2.5]
plt.plot(line3_x, line3_y, c=cmap(0.4))

# Plotting
plt.subplots_adjust(top=0.85)
plt.xscale('log')
plt.xlabel(r'prey-prey interaction torque $T_{\mathrm{A}}$', fontsize=fontsize)
plt.ylabel(r'prey-prey interaction radius $R_{\mathrm{pp}}$ in $r_{\mathrm{c}}$', fontsize=fontsize)
plt.ylim(1.8, 5.2)
plt.xlim(0.08, 50)
plt.legend(loc='upper center', fontsize=fontsize, bbox_to_anchor=(0.5, 1.25), ncol=2)
plt.savefig('/Users/oliversange/Desktop/PLOTS/state_diagram.pdf')
plt.show()

