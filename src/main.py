"""
In this script, the slope and deflection of a simply supported beam are calculated from the curvature using the trapezoidal rule.
See: https://www.engineeringskills.com/posts/beam-deflection-calculator
"""

import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(linewidth=200)


def plot_values(x_axis, y_axis, title, invert_y_axis=False):
    plt.plot(x_axis, y_axis)
    plt.title(title)
    plt.grid()
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    if invert_y_axis:
        plt.gca().invert_yaxis()
    plt.xlim(0, np.max(x_axis))
    plt.show()


def get_bending_moments(x_axis, load, length):
    bending_moment = np.array([])
    for i in range(len(x_axis)):
        x_pos = x_axis[i]
        moment = (x_pos * (load * length) / 2) - (load * x_pos * (x_pos/2))  # Nm
        bending_moment = np.append(bending_moment, moment)
    return bending_moment


def get_curvatures(bending_moment_list, modulus, inertia):
    curvature_list = bending_moment_list / (modulus * inertia)
    return curvature_list


def get_slopes(dx, x_axis, curvature_list, slope_init):
    slope_list = np.array([])
    for i in range(len(x_axis)):
        if i == 0:
            slope = slope_init
        else:
            slope = slope + (dx/2) * (curvature_list[i] + curvature_list[i-1])
        slope_list = np.append(slope_list, slope)
    return slope_list


def get_deflections(dx, x_axis, slope_list):
    deflection_list = np.array([])
    for i in range(len(x_axis)):
        if i == 0:
            deflection = 0
        else:
            deflection = deflection + (dx/2) * (slope_list[i] + slope_list[i-1])
        deflection_list = np.append(deflection_list, deflection)
    return deflection_list


def main():
    load = 10 * 10**3  # N
    length = 5  # m
    dx = 0.1  # m
    inertia = (1/12)*0.3*0.5**3  # m^4
    modulus = 30 * 10**9  # Pa

    # Space mesh
    x_axis = np.arange(0, length, dx)
    x_axis = np.append(x_axis, length)

    # Bending moments on a simply supported beam
    bending_moment_list = get_bending_moments(x_axis, load, length)

    # Curvatures
    curvature_list = get_curvatures(bending_moment_list, modulus, inertia)

    # Slopes from an arbitrary (incorrect) initial slope
    slope_init_0 = 0
    slope_list = get_slopes(dx, x_axis, curvature_list, slope_init_0)
    slope_midspan = slope_list[int(len(slope_list) / 2)]

    # Slopes from a correct initial slope
    slope_error = (0 - slope_midspan)  # Slope in the middle of a simply supported beam must be zero
    slope_init_1 = slope_init_0 + slope_error
    slope_list = get_slopes(dx, x_axis, curvature_list, slope_init_1)

    # Deflection
    deflection_list = get_deflections(dx, x_axis, slope_list)

    # Using matplotlib, create figures for: bending moment, curvature, slope, and deflection
    plot_values(x_axis, bending_moment_list, 'Bending Moment', True)
    plot_values(x_axis, curvature_list, 'Curvature')
    plot_values(x_axis, slope_list, 'Slope')
    plot_values(x_axis, deflection_list, 'Deflection')

    # Evaluate the deflection at mid-span (compare it with the theoretical value)
    deflection_mid = deflection_list[int(len(deflection_list) / 2)]
    print('Calculated deflection at mid-span:', deflection_mid)

    deflection_mid_theor = - (5/384) * (load * length**4) / (modulus * inertia)
    print('Theoretical deflection at mid-span:', deflection_mid_theor)

    error = abs(deflection_mid_theor - deflection_mid) / deflection_mid_theor
    print('Error: ', round(error, 9), '%')


if __name__ == '__main__':
    main()

