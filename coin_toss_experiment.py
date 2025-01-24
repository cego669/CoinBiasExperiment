import numpy as np
import sympy
from scipy.stats import binom
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider

############################## SETUP

# Coin bias starts at 0.5
bias = 0.5

# Defining main variables (theta, n and k)
theta = sympy.symbols("theta", real=True)
n = sympy.symbols("n", integer=True)
k = sympy.symbols("k", integer=True)

# Defining main functions
P_theta = 1 # A priori pdf for theta
P_n_k_given_theta = sympy.factorial(n)/(sympy.factorial(n - k) * sympy.factorial(k)) * theta**k * (1 - theta)**(n - k) # A posteriori for n, k given theta (binomial)
P_n_k = sympy.simplify(sympy.integrate(P_theta * P_n_k_given_theta, (theta, 0, 1))) # A priori for n, k

# A posteriori for theta given n, k
def P_theta_given_n_k(theta_value, n_value, k_value):
    expression = (P_theta * P_n_k_given_theta)/P_n_k
    return expression.subs([(theta, theta_value),
                            (n, n_value),
                            (k, k_value)]).evalf(4) # we need to evaluate this function at a linspace for theta (0 to 1)

############################## INTERACTIVE PLOT

# We start with 0 tosses and therefor 0 heads
N = 0
K = 0
title = "Coin tosses: "
info = lambda k, n: f" ({n} tosses, {k} heads)"

# Calculating respective probability density values using P_theta_given_n_k
thetas = np.linspace(0, 1, 100) # 100 points for theta
probs = [P_theta_given_n_k(t, N, K) for t in thetas]

# Initial plot
fig, ax = plt.subplots()
line, = ax.plot(thetas, probs, "--", color="black")
ax.set_xlabel(r"$\theta$" + " (coin bias)")
ax.set_ylabel(r"$P(\theta|n=$" + str(N) + r"$, k=$" + str(K) + r"$)$" + " (probability density function)")
ax.set_title(title + info(K, N))

# oooooooo Interactive button: toss next coin with given bias oooooooo
ax_button = plt.axes([0.41, 0.94, 0.2, 0.05])
toss_button = Button(ax_button, "Toss next coin", color="white", hovercolor="gray")

def new_coin_toss(val):
    global N, K, title, line
    N += 1 # Adding one more toss
    if binom.rvs(n=1, p=bias) > 0: # If heads...
        title += "H"
        K += 1
    else: # If tail
        title += "T"
    
    # Updating plot for the new toss
    probs = [P_theta_given_n_k(t, N, K) for t in thetas]
    line.set_ydata(probs)
    ax.set_ylabel(r"$P(\theta|n=$" + str(N) + r"$, k=$" + str(K) + r"$)$" + " (probability density function)")
    ax.set_title(title + info(K, N))
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

# oooooooo Interactive button: clear plot oooooooo
ax_button2 = plt.axes([0.8, 0.008, 0.1, 0.05])
clear_button = Button(ax_button2, "Clear", color="white", hovercolor="gray")

def clear(val):
    global N, K, title, line
    N = 0 # Clearing tosses
    K = 0
    title = "Coin tosses: "

    # Clearing plot
    probs = [P_theta_given_n_k(t, N, K) for t in thetas]
    line.set_ydata(probs)
    ax.set_ylabel(r"$P(\theta|n=$" + str(N) + r"$, k=$" + str(K) + r"$)$" + " (probability density function)")
    ax.set_title(title + info(K, N))
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

# oooooooo Interactive slider: change coin bias oooooooo
ax_slider = plt.axes([0.92, 0.25, 0.03, 0.5])
bias_slider = Slider(ax_slider, 'Bias', 0, 1, valinit=bias, orientation='vertical')

def update_bias(val):
    global bias
    bias = bias_slider.val # Just updates coin bias given the value in the slider

# Commiting each event
bias_slider.on_changed(update_bias)
toss_button.on_clicked(new_coin_toss)
clear_button.on_clicked(clear)

# Show the plot
plt.show()