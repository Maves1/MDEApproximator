import math
from abc import ABC, abstractmethod

class Approximator(ABC):
    @abstractmethod
    def calcNext(self, x_prev, y_prev, step):
        raise NotImplementedError

    def calcYPrime(self, x, y):
        if x == 0:
            x = x + 0.000001
        return y / x - y - x

class EulerApproximator(Approximator):
    def calcNext(self, x_prev, y_prev, step):
        y_curr = y_prev + step * self.calcYPrime(x_prev, y_prev)
        return y_curr

class ImprovedEulerApproximator(Approximator):
    def calcNext(self, x_prev, y_prev, step):
        y_curr = y_prev + step * self.calcYPrime(x_prev + step / 2, y_prev + (step / 2) * self.calcYPrime(x_prev, y_prev))
        return y_curr

class RungeKuttaApproximator(Approximator):
    def calcNext(self, x_prev, y_prev, step):
        k1 = self.calcYPrime(x_prev, y_prev)
        k2 = self.calcYPrime(x_prev + step / 2, y_prev + (step * k1) / 2)
        k3 = self.calcYPrime(x_prev + step / 2, y_prev + (step * k2) / 2)
        k4 = self.calcYPrime(x_prev + step, y_prev + step * k3)

        y_curr = y_prev + (step / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        return y_curr

class Platform:

    def calcConstant(self, x0, y0):
        c = (y0 + x0) / (math.e ** -x0 * x0)
        print(c)
        return c

    def calcExactSolution(self, x):
        y = self.c * (math.e ** -x) * x - x
        return y

    def getPoints(self, x0, xFinal, y0, step):
        self.c = self.calcConstant(x0, y0)

        xs = [x0]
        ys = [y0]
        while x0 <= xFinal:
            x0 += step
            y = self.calcExactSolution(x0)
            ys.append(y)
            xs.append(x0)
        return xs, ys

    def calcGTE(self, exactYs, approxYs):
        gtes = []
        for i in range(len(exactYs)):
            gtes.append(abs(approxYs[i] - exactYs[i]))
        return gtes

    def calcLTE(self, exactYs, x0, step, approximator):
        ltes = [0]
        x_curr = x0
        for i in range(1, len(exactYs)):
            curr_error = abs(approximator.calcNext(x_curr, exactYs[i - 1], step) - exactYs[i])
            ltes.append(curr_error)
            x_curr += step
        return ltes

    def approximate(self, approximator, x0, x_final, y0, step):
        self.c = self.calcConstant(x0, y0)

        approxYs = [y0]
        xs, ys = self.getPoints(x0, x_final, y0, step)

        y_prev = y0

        for i in range(1, len(xs)):
            y_curr = approximator.calcNext(xs[i - 1], y_prev, step)

            approxYs.append(y_curr)
            y_prev = y_curr

        gtes = self.calcGTE(ys, approxYs)
        ltes = self.calcLTE(ys, x0, step, approximator)

        return approxYs, gtes, ltes