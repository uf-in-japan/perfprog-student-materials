# Adapted by Jennifer "Ferby" Cremer and Jeremiah Blanchard, 2020, University of Florida
# Derived from source at https://matplotlib.org/examples/showcase/mandelbrot.html
from math import log
from abc import ABC, abstractmethod
import asyncio
import struct
import itertools

class Fractal(ABC):
    @abstractmethod
    # Constructor - at a minimum, must set passed in attributes and the x and y ranges
    def __init__(self, image_width, image_height, iterations):
        pass

    # Generate tasks to calculate set data and return receptical image matrix
    @abstractmethod
    def generate_tasks(self, smm, num_tasks):
        return None, None

    # Properties for common traits among fractals
    @property
    def x_range(self):
        return self._x_range

    @x_range.setter
    def x_range(self, new_range):
        self._x_range = new_range

    @property
    def y_range(self):
        return self._y_range

    @y_range.setter
    def y_range(self, new_range):
        self._y_range = new_range

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, new_dimensions):
        self._dimensions = new_dimensions

    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, new_iterations):
        self._iterations = new_iterations


class Mandelbrot(Fractal):
    _X_BOUNDARY = (-2.25, 0.75)
    _Y_BOUNDARY = (-1.25, 1.25)


    # These one-line functions *should* be inlined by python... (skeptical look at interpreter...)
    def complex_list_to_bytes(self, clist):
        return b''.join([struct.pack('dd', num.real, num.imag) for num in clist])


    def bytes_to_complex_list(self, seq):
        return [complex(*struct.unpack('dd', seq[index * 16:(index+1)*16])) for index in range(len(seq) // 16)]


    def data_to_image_matrix(self, data):
        return [struct.unpack('d' * self.dimensions[0], row_data[:-1]) for row_data in data[3]]


    def __init__(self, image_width, image_height, iterations):
        self.x_range = Mandelbrot._X_BOUNDARY
        self.y_range = Mandelbrot._Y_BOUNDARY
        self.dimensions = (image_width, image_height)
        self.iterations = iterations
        self.horizon = 0x1000000000


    # Wraps a task call so that we can mark it as done when it completes
    def run_task(self, task_no, done_array, function, parameters):
        if done_array[task_no]:
            raise Exception("Tried to run task which was already completed!")

        value = function(*parameters)
        done_array[task_no] = 1
        return value


    # Calculates information for a particular row of coordinates (used for async tasks)
    def row_set_calc(self, horizon, iterations, row_range, Z, N, C, Q):
        log_horizon = log(log(horizon)) / log(2)
        for row in row_range:
            c = self.bytes_to_complex_list(C[row][:-1])
            z = self.bytes_to_complex_list(Z[row][:-1])
            q = list(struct.unpack('d' * self.dimensions[0], Q[row][:-1]))
            n = list(struct.unpack('d' * self.dimensions[0], N[row][:-1]))

            for col in range(len(c)):
                for round in range(iterations):
                    if abs(z[col]) < horizon:
                        z[col] = z[col] ** 2 + c[col]
                        n[col] = round
                if n[col] == iterations - 1: n[col] = 0

                # This is ugly as sin, but it is the fastest way to do this.
                try:
                    q[col] = n[col] + 1 - log(log(abs(z[col])))/log(2) + log_horizon
                except:
                    q[col] = 0.0

            C[row] = self.complex_list_to_bytes(c) + b'\n'
            N[row] = struct.pack('d' * self.dimensions[0], *n) + b'\n'
            Z[row] = self.complex_list_to_bytes(z) + b'\n'
            Q[row] = struct.pack('d' * self.dimensions[0], *q) + b'\n'


    # Generates tasks to generate the Mandelbrot Set data and returns the receptical image matrix
    def generate_tasks(self, smm, num_tasks):
        dx = (self.x_range[1] - self.x_range[0]) / (self.dimensions[0] - 1) if self.dimensions[0] > 1 else 0
        dy = (self.y_range[1] - self.y_range[0]) / (self.dimensions[1] - 1) if self.dimensions[1] > 1 else 0
        task_rows = self.dimensions[1] / num_tasks

        X = [self.x_range[0] + dx * index for index in range(self.dimensions[0])]
        Y = [self.y_range[0] + dy * index for index in range(self.dimensions[1])]

        # So the ShareableList type is broken and truncates zeroes (ugh)... so we add '\n' to the end to prevent this.
        C = smm.ShareableList([self.complex_list_to_bytes([complex(real, imag) for real in X]) + b'\n' for imag in Y])
        N = smm.ShareableList([struct.pack('d', 0) * self.dimensions[0] + b'\n' for _ in range(self.dimensions[1])])
        Z = smm.ShareableList([struct.pack('d', 0) * self.dimensions[0] * 2 + b'\n' for _ in range(self.dimensions[1])])
        Q = smm.ShareableList([struct.pack('d', 0) * self.dimensions[0] + b'\n' for _ in range(self.dimensions[1])])
        D = smm.ShareableList([0 for _ in range(num_tasks)])

        ranges = [range(round(task_no * task_rows), round((task_no + 1) * task_rows)) for task_no in range(num_tasks)]
        lambda_generator = (lambda rows, id: (lambda: self.run_task(id, D, self.row_set_calc, (self.horizon, self.iterations, rows, Z, N, C, Q))))
        tasks = [lambda_generator(row_range, id) for id, row_range in enumerate(ranges)]
        return tasks, (C, N, Z, Q, D)
