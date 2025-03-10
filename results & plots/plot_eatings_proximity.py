import matplotlib.pyplot as plt

def plot_eatings_over_proximity(eatings_dict, proximity_dict, save_path):
    eatings = []
    proximity = []

    for key in eatings_dict:
        for i in eatings_dict[key]:
            eatings.append(i)
    for key in proximity_dict:
        for i in proximity_dict[key]:
            proximity.append(i)

    plt.scatter(proximity, eatings)
    plt.xlabel(r"average number of prey particles within interaction range")
    plt.ylabel("eatings")
    plt.savefig(save_path)
    plt.show()

eatings_R_9_2T_A_run1 = {0.1: [50, 53, 57, 61], 1: [50, 42, 60, 65], 10: [60, 57, 53, 29], 20: [67, 84, 76, 77], 30: [77, 70, 72, 94], 40: [88, 70, 84, 78]}
proximity_R_9_2T_A_run1 = {0.1: [0.51, 0.95, 1.59, 2.12], 1: [0.46, 1.88, 5.09, 6.97], 10: [1.04, 4.95, 4.47, 19.09], 20: [1.03, 5.31, 6.14, 11.39], 30: [1.03, 2.88, 7.23, 0], 40: [0.68, 3.93, 7.67, 7.79]}

save_path = "/Users/oliversange/Desktop/eatings_over_proximity_R_9_2T_A_run1.pdf"

plot_eatings_over_proximity(eatings_R_9_2T_A_run1, proximity_R_9_2T_A_run1, save_path)