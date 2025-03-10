import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Create simple plot to showcase WCA potential

# WCA potential
def wca(r):
    result = np.where(r <= 2**(1/6), 4 * 100* ((1/r)**12 - (1/r)**6) + 100, 0)
    return result

# Parameters
x = [2**(1/6), 2**(1/6)]
y = [0, 200]
x_1 = [1, 1]
y_1 = [0, 200]
cmap = plt.get_cmap("inferno")
fontsize = 14
r = np.linspace(0.1, 3, 500)

# Plotting
plt.plot(r, wca(r), c=cmap(0.2), label=r"WCA potential $U_{100, 1}$")
plt.plot(x, y, c=cmap(0.4), linewidth=0.8, linestyle="--", label=r"cutoff radius $r_c$")
plt.plot(x_1, y_1, c=cmap(0.5), linewidth=0.8, linestyle=":", label=r"particle diameter $\sigma$")
plt.ylim(0, 100)
plt.xlim(0.9 , 1.3)
plt.xlabel(r"distance between paricles $r$", fontsize=fontsize)
plt.ylabel(r"WCA potential $U_{\epsilon, \sigma}$", fontsize=fontsize)
plt.grid()
plt.legend(fontsize=fontsize)
plt.savefig("/Users/oliversange/Desktop/PLOTS/wca_potential.pdf")
plt.show()