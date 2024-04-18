import math

import numpy as np


class Function:
    def calc(self, x):
        pass
    def calc_points(self, a, b, step):
        x_vals = np.arange(a, b+step, step)

        y_vals = [self.calc(x) for x in x_vals]
        return list(x_vals), y_vals
class interpolation_newton_polynomial(Function):
    def __init__(self, data_points):
        self.data_points = data_points # list of tuples
        self.interpolation_array = [[0 for x in range(i)] for i in range(len(data_points), 0, -1)]
        self.func = []
        self.coefs = []
        self.interpolate()
        self.calc_segments()

    def calc_val(self, val_prev_on_axis, val_to_left, x2, x1):
        return (val_prev_on_axis - val_to_left) / (x2-x1)
    def interpolate(self):
        # initial points
        for i, (x, y) in enumerate(self.data_points):
            self.interpolation_array[i][0] = y
        # calculating values top to bottom on axes

        for i in range(1, len(self.interpolation_array)):

            initial_x_val = self.data_points[i][0]
            (x, y) = (i, 0)
            while x > 0:
                (x, y) = (x - 1, y + 1) # next element on axis
                element_on_left = self.interpolation_array[x][y - 1]
                prev_element_on_axis = self.interpolation_array[x + 1][y - 1]
                self.interpolation_array[x][y] = self.calc_val(prev_element_on_axis, element_on_left, initial_x_val, self.data_points[x][0])

    def calc(self, x):
        result = self.coefs[0]
        for i, segment in enumerate(self.func):
            segment_val = self.coefs[i+1]
            for val in segment:
                segment_val *= x + val
            result += segment_val
        return result

    def calc_segments(self):
        self.coefs = self.interpolation_array[0]
        self.func = [[-self.data_points[j][0] for j in range(i)] for i in range(1, len(self.data_points))]
    def print_interpolation_array(self):
        for row in self.interpolation_array:
            print(row)
class Abs(Function):
    def calc(self, x):
        return abs(x)

class Polynomial(Function):
    def __init__(self, coefs):
        if len(coefs) > 0:
            self.coefs = coefs
        else:
            raise Exception("No coefficients")

    def calc(self, x):
        result = self.coefs[0]
        for coef in self.coefs[1:]:
            result = coef + x * result
        return result


class Trygonometrical(Function):
    def __init__(self, func_index):
        if func_index == 0:
            self.func = math.sin
        elif func_index == 1:
            self.func = math.cos
        elif func_index == 2:
            self.func = math.tan
        elif func_index == 3:
            self.func = lambda x: 1 / math.tan(x)
        else:
            raise Exception("Wrong index")


    def calc(self, x):
        return self.func(x)


class Exponential(Function):
    def __init__(self, b):
        if b > 0:

            self.b = b
        else:
            raise Exception("Wrong base")
    def calc(self, x):
        return self.b ** x


class Composition(Function):
    def __init__(self, functions):
        if len(functions) > 0:
            self.functions = functions
        else:
            raise Exception("No functions")

    def calc(self, x):
        result = x
        for function in reversed(self.functions):
            result = function.calc(result)
        return result
