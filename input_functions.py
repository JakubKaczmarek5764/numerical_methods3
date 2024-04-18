import random

import numpy as np

import functions
import matplotlib.pyplot as plt


def plotting(func, a, b, points=None, step=None):
    if not step:
        step = abs(a - b)/100
    x_vals, y_vals = func.calc_points(a, b, step)
    plt.grid(True)
    plt.plot(x_vals, y_vals)
    plt.axhline(y=0, c='green')
    if a <= 0 <= b:
        plt.axvline(x=0, c='green')
    if points:
        plt.scatter(x=[point[0] for point in points], y=[point[1] for point in points])
def input_polynomial():
    print("Podaj wspolczynniki wielomianu po spacji: ")
    coefs = [float(x) for x in input().split()]
    return functions.Polynomial(coefs)
def input_trygonometrical():
    print("Podaj rodzaj funkcji trygonometrycznej: ")
    print("0 - sin \n1 - cos\n2 - tan \n3 - ctg")
    index = int(input())
    return functions.Trygonometrical(index)

def intro(): # zlozenia funkcji podawane sa od lewej do prawej, czyli w przypadku zlozenia f(g(x)) najpierw podajemy funkcje f

    print("Wybierz z ilu funkcji ma byc zlozenie:")
    count = int(input())
    funcs = []
    for i in range(count):
        print(f"Wybierz rodzaj funkcji {i+1}: \n0 - Wielomianowa \n1 - Trygonometryczna \n2 - Moduł")
        choice = int(input())
        if choice == 0:
            funcs.append(input_polynomial())
        elif choice == 1:
            funcs.append(input_trygonometrical())
        elif choice == 2:
            funcs.append(functions.Abs())
        else:
            raise Exception("Zly wybor")

    output_function = functions.Composition(funcs)

    print("Wprowadz krance przedzialu po spacji: ")
    (a, b) = (float(x) for x in input().split())
    print("Wprowadz liczbe wezlow: ")
    num_of_nodes = int(input())
    print("Wprowadz sposob wprowadzania wezlow: \n0 - z pliku \n1 - jitter \n2 - wybor losowy")
    method = int(input())
    # tu input trzeba zrobic tak, zeby na koncu points mial odpowiednie punkty [(x0, y0), (x1, y1), ...]
    x_points = jitter(a, b, num_of_nodes)
    points = [(x, output_function.calc(x)) for x in x_points]
    print(points)
    interpolate(output_function, a, b, points)

def interpolate(func, a, b, points):
    plotting(func, a, b)
    interpolated_func = functions.interpolation_newton_polynomial(points)
    plotting(interpolated_func, a, b, points)

def jitter(a, b, num_of_nodes, range = None):
    step = (b - a) / num_of_nodes
    if not range: range = step / 4
    x_points = np.arange(a, b+step, step=step)
    return [one_point_jitter(x, range) for x in x_points]

def one_point_jitter(x, range):
    return x - random.random() * range - range / 2
def built_in_functions():
    funcs = [
        functions.Polynomial([2.1, 2.3, -2.5]),
        functions.Trygonometrical(3),
        functions.Polynomial([2.1, 1])
    ]
    comp1 = functions.Composition([functions.Polynomial([2.1, 2.3, -2.5]),
                                   functions.Exponential(2.1),
                                   functions.Polynomial([2.1, 1])])
    comp2 = functions.Composition([functions.Trygonometrical(0), functions.Trygonometrical(1)])
    a = 0.1
    b = 3
    num_of_nodes = 10
    x_points = jitter(a, b,10)
    print(x_points)
    func_ptr = functions.Trygonometrical(0)
    points = [(x, func_ptr.calc(x)) for x in x_points]
    interpolate(func_ptr, a, b, points)
    plt.show()

