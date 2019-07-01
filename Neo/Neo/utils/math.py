# Import the necessary libraries
import operator
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def get_interpolate_value(x_list, y_list, value):
    x = np.array(x_list)
    y = np.array(y_list)

    fitting_parameters, covariance = curve_fit(exponential_fit, x, y)
    a, b = fitting_parameters

    return float(exponential_fit(value, a, b))


def exponential_fit(x, a, b):
    res = a * np.log(x) + b
    if np.all(res < 0):
        return 0
    return res


def plot(x_list, y_list):
    x = np.array(x_list)
    y = np.array(y_list)

    fitting_parameters, covariance = curve_fit(exponential_fit, x, y)
    a, b = fitting_parameters

    y_pred = []
    x_pred = []
    for i in range(0, 100):
        x_pred.append(i)
        y_pred.append(exponential_fit(i, a, b))

    plt.plot(x_pred, y_pred, "-")
    plt.plot(x, y, '.')
    plt.show()
