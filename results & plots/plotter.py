import matplotlib.pyplot as plt
import numpy as np

def overview_plotter(eatings):
    for eating in eatings:
        av_array = np.repeat(eating, 4)
        plt.scatter(av_array, [2, 3, 4, 5], s=np.array(eatings[eating])**3/1000, c="black")
    plt.xlabel(r"strength $T_A$")
    plt.ylabel(r"radius $R$ in $r_c$")
    plt.title(r"Prey torque interactions")
    plt.xscale("log")
    plt.savefig('/Users/oliversange/Desktop/eatings_R_3_3T_A_run1_overview.pdf')
    plt.show()
if __name__ == '__main__':

    # Create simple overview plot

    eatings_R_3_3T_A_run1 = {0.1: [49, 59, 56, 66], 1: [55, 60, 78, 72], 10: [41, 45, 67, 46], 20: [72, 73, 60, 56],
                             30: [58, 73, 50, 72], 40: [33, 31, 70, 64]}
    overview_plotter(eatings_R_3_3T_A_run1)