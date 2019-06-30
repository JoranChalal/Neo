# Import the necessary libraries
import numpy
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit


def get_interpolate_value(x_list, y_list, x):
    # Fit with polyfit
    b, m = polyfit(x_list, y_list, 1)
    y = float(b) + float(m) * x
    return y


def plot(x_list, y_list):
    plt.plot(x_list, y_list, 'ro')

    # Fit with polyfit
    b, m = polyfit(x_list, y_list, 1)
    max_x = max(x_list) + 10

    x_regression = numpy.arange(0, max_x, 0.5)
    y_regression = float(b) + float(m) * x_regression
    plt.plot(x_list, y_list, '.')
    plt.plot(x_regression, y_regression, '-')
    axes = plt.gca()
    axes.set_xlim([0, max_x])
    plt.show()
