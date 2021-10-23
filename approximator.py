from abc import ABC, abstractmethod

class Approximator(ABC):
    @abstractmethod
    def calcNext(self, x_prev, y_prev, step):
        raise NotImplementedError

class EulerApproximator(Approximator):
    def calcNext(self, x_prev, y_prev, step):
        # TODO: Change the equation
        y_curr = y_prev + step * (y_prev ** 2 + x_prev * y_prev - x_prev ** 2) / (x_prev ** 2)
        return y_curr

class ImprovedEulerApproximator(Approximator):
    def calcNext(self, x_prev, y_prev, step):
        # TODO: Change the equation
        f = (y_prev ** 2 + x_prev * y_prev - x_prev ** 2) / (x_prev ** 2)
        x = x_prev + step / 2
        y = y_prev + step / 2 * f

        y_curr = y_prev + step * (y ** 2 + x * y - x ** 2) / (x ** 2)
        return y_curr

class RungeKuttaApproximator(Approximator):
    def calcNext(self, x_prev, y_prev, step):
        # TODO: Change the equation
        k1 = (y_prev ** 2 + x_prev * y_prev - x_prev ** 2) / (x_prev ** 2)

        x = x_prev + step / 2
        y = y_prev + step * k1 / 2
        k2 = (y ** 2 + x * y - x ** 2) / (x ** 2)

        y = y_prev + step * k2 / 2
        k3 = (y ** 2 + x * y - x ** 2) / (x ** 2)

        x = x_prev + step
        y = y_prev + step * k3
        k4 = (y ** 2 + x * y - x ** 2) / (x ** 2)

        y_curr = y_prev + step * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        return y_curr

class Platform:

    def calcExactSolution(self, x):
        # TODO: Change the equation
        y = (x * (1 + x ** 2 / 3)) / (1 - x ** 2 / 3)
        return y

    def getPoints(self, x0, x_final, y0, step):
        xs = [x0]
        ys = [y0]
        while x0 <= x_final:
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