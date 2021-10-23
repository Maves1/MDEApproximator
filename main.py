import matplotlib
import matplotlib.animation as animation
matplotlib.use("TkAgg")
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

from approximator import *

style.use("ggplot")

approxFigure = Figure(figsize=(6, 6), dpi=100)
axPlot = approxFigure.add_subplot(111)

errorsFigure = Figure(figsize=(6, 6), dpi=100)
errPlot = errorsFigure.add_subplot(111)

platform = Platform()
eulerApproximator = EulerApproximator()
improvedEulerApproximator = ImprovedEulerApproximator()
rungeKuttaApproximator = RungeKuttaApproximator()

def animate(interval):

    try:
        x0 = float(app.frames[MainPage].textBoxX0.get("1.0", 'end-1c'))
        xFinal = float(app.frames[MainPage].textBoxX.get("1.0", 'end-1c'))
        y0 = float(app.frames[MainPage].textBoxY0.get("1.0", 'end-1c'))
        step = float(app.frames[MainPage].textBoxStep.get("1.0", 'end-1c'))

        if step <= 0:
            step = 0.01

        xs, ys = platform.getPoints(x0, xFinal, y0, step)

        axPlot.clear()
        if app.frames[MainPage].exactEnabledVar.get() == 1:
            axPlot.plot(xs, ys, label="Exact")
        if app.frames[MainPage].eulerEnabledVar.get() == 1:
            approxYs, ltes, gtes = platform.approximate(eulerApproximator, x0, xFinal, y0, step)
            axPlot.plot(xs, approxYs, label="Euler")
        if app.frames[MainPage].improvedEulerEnabledVar.get() == 1:
            approxYs, ltes, gtes = platform.approximate(improvedEulerApproximator, x0, xFinal, y0, step)
            axPlot.plot(xs, approxYs, label="Improved Euler")
        if app.frames[MainPage].rungeKuttaEnabledVar.get() == 1:
            approxYs, ltes, gtes = platform.approximate(rungeKuttaApproximator, x0, xFinal, y0, step)
            axPlot.plot(xs, approxYs, label="Runge Kutta")

        axPlot.legend()

        app.x0 = x0
        app.xFinal = xFinal
        app.y0 = y0
        app.step = step
    except Exception:
        pass


class MDEApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "MDEApproximator")

        self.x0 = 1.0
        self.xFinal = 1.5
        self.y0 = 2
        self.step = 0.1

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, SecondPage):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

        self.show_frame(MainPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        self.textBoxWidth = 15

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=1)

        labelX0 = ttk.Label(self, text="x0")
        labelX0.grid(row=0, column=0)
        self.textBoxX0 = tk.Text(self, width=self.textBoxWidth, height=1)
        self.textBoxX0.grid(row=0, column=1)

        labelX = ttk.Label(self, text="x")
        labelX.grid(row=1, column=0)
        self.textBoxX = tk.Text(self, width=self.textBoxWidth, height=1)
        self.textBoxX.grid(row=1, column=1)

        labelStep = ttk.Label(self, text="step")
        labelStep.grid(row=2, column=0)
        self.textBoxStep = tk.Text(self, width=self.textBoxWidth, height=1)
        self.textBoxStep.grid(row=2, column=1)

        labelY0 = ttk.Label(self, text="y0")
        labelY0.grid(row=3, column=0)
        self.textBoxY0 = tk.Text(self, width=self.textBoxWidth, height=1)
        self.textBoxY0.grid(row=3, column=1)

        self.exactEnabledVar = tk.IntVar()
        self.eulerEnabledVar = tk.IntVar()
        self.improvedEulerEnabledVar = tk.IntVar()
        self.rungeKuttaEnabledVar = tk.IntVar()
        exactEnabled = ttk.Checkbutton(self, text="Exact", variable=self.exactEnabledVar).grid(row=4, column=0, sticky="w")
        eulerEnabled = ttk.Checkbutton(self, text="Euler", variable=self.eulerEnabledVar).grid(row=5, column=0, sticky="w")
        improvedEulerEnabled = ttk.Checkbutton(self, text="Improved Euler", variable=self.improvedEulerEnabledVar)\
            .grid(row=6, column=0, sticky="w")
        rungeKuttaEnabled = ttk.Checkbutton(self, text="Runge-Kutta", variable=self.rungeKuttaEnabledVar)\
            .grid(row=7, column=0, sticky="w")


        secondPageButton = ttk.Button(self, text="LTE / GTE", command=lambda: controller.show_frame(SecondPage))
        secondPageButton.grid(row=8, column=0)

        canvas = FigureCanvasTkAgg(approxFigure, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=8)

        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row=8, columnspan=3)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()

class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        x0 = 1.0
        xFinal = 1.5
        y0 = 2
        step = 0.1

        labelX0 = ttk.Label(self, text="x0")
        labelX0.grid(row=0, column=0)
        self.textBoxX0 = tk.Text(self, width=self.textBoxWidth, height=1)
        self.textBoxX0.grid(row=0, column=1)

        xs, ys = platform.getPoints(x0, xFinal, y0, step)
        approxYs, ltes, gtes = platform.approximate(eulerApproximator, x0, xFinal, y0, step)
        ltes = platform.calcLTE(ys, x0, step, eulerApproximator)
        gtes = platform.calcGTE(ys, approxYs)

        errPlot.plot(xs, ltes, label="LTE")
        errPlot.plot(xs, gtes, label="GTE")
        errPlot.legend()

        canvas = FigureCanvasTkAgg(errorsFigure, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainPage))
        backButton.grid(row=1, column=0)

app = MDEApp()
app.style = ttk.Style()
app.style.theme_use("clam")
animationFunction = animation.FuncAnimation(approxFigure, animate, 1000)

app.mainloop()