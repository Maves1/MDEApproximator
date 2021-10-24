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
approxPlot = approxFigure.add_subplot(111)

ltesFigure = Figure(figsize=(6, 6), dpi=100)
ltesPlot = ltesFigure.add_subplot(111)

gtesFigure = Figure(figsize=(6, 6), dpi=100)
gtesPlot = gtesFigure.add_subplot(111)

platform = Platform()
eulerApproximator = EulerApproximator()
improvedEulerApproximator = ImprovedEulerApproximator()
rungeKuttaApproximator = RungeKuttaApproximator()

def animateMainPage(interval):

    try:
        x0 = float(app.frames[MainPage].textBoxX0.get("1.0", 'end-1c'))
        xFinal = float(app.frames[MainPage].textBoxX.get("1.0", 'end-1c'))
        y0 = float(app.frames[MainPage].textBoxY0.get("1.0", 'end-1c'))
        step = float(app.frames[MainPage].textBoxStep.get("1.0", 'end-1c'))

        if step <= 0:
            step = 0.01

        if x0 != app.x0 or xFinal != app.xFinal or y0 != app.y0 or step != app.step or\
            app.frames[MainPage].exactEnabledVar.get() != app.prevExactEnabled or\
            app.frames[MainPage].eulerEnabledVar.get() != app.prevEulerEnabled or\
            app.frames[MainPage].improvedEulerEnabledVar.get() != app.prevImprovedEulerEnabled or\
            app.frames[MainPage].rungeKuttaEnabledVar.get() != app.prevRungeKuttaEnabled:

            xs, ys = platform.getPoints(x0, xFinal, y0, step)

            approxPlot.clear()
            if app.frames[MainPage].exactEnabledVar.get() == 1:
                approxPlot.plot(xs, ys, label="Exact")
            if app.frames[MainPage].eulerEnabledVar.get() == 1:
                approxYs, ltes, gtes = platform.approximate(eulerApproximator, x0, xFinal, y0, step)
                approxPlot.plot(xs, approxYs, label="Euler")
            if app.frames[MainPage].improvedEulerEnabledVar.get() == 1:
                approxYs, ltes, gtes = platform.approximate(improvedEulerApproximator, x0, xFinal, y0, step)
                approxPlot.plot(xs, approxYs, label="Improved Euler")
            if app.frames[MainPage].rungeKuttaEnabledVar.get() == 1:
                approxYs, ltes, gtes = platform.approximate(rungeKuttaApproximator, x0, xFinal, y0, step)
                approxPlot.plot(xs, approxYs, label="Runge Kutta")

            approxPlot.legend()

            app.x0 = x0
            app.xFinal = xFinal
            app.y0 = y0
            app.step = step

            app.prevExactEnabled = app.frames[MainPage].exactEnabledVar.get()
            app.prevEulerEnabled = app.frames[MainPage].eulerEnabledVar.get()
            app.prevImprovedEulerEnabled = app.frames[MainPage].improvedEulerEnabledVar.get()
            app.prevRungeKuttaEnabled = app.frames[MainPage].rungeKuttaEnabledVar.get()
    except Exception:
        pass


def animateLTEPage(interval):

    try:

        xs, ys = platform.getPoints(app.x0, app.xFinal, app.y0, app.step)
        eulerLTES = platform.calcLTE(ys, app.x0, app.step, eulerApproximator)
        imprEulerLTES = platform.calcLTE(ys, app.x0, app.step, improvedEulerApproximator)
        rkLTES = platform.calcLTE(ys, app.x0, app.step, rungeKuttaApproximator)

        if app.frames[LTEPage].eulerEnabledVar.get() != app.prevEulerEnabled or\
            app.frames[LTEPage].improvedEulerEnabledVar.get() != app.prevImprovedEulerEnabled or\
            app.frames[LTEPage].rungeKuttaEnabledVar.get() != app.prevRungeKuttaEnabled:

            ltesPlot.clear()
            if app.frames[LTEPage].eulerEnabledVar.get() == 1:
                ltesPlot.plot(xs, eulerLTES, label="Euler")
            if app.frames[LTEPage].improvedEulerEnabledVar.get() == 1:
                ltesPlot.plot(xs, imprEulerLTES, label="Improved Euler")
            if app.frames[LTEPage].rungeKuttaEnabledVar.get() == 1:
                ltesPlot.plot(xs, rkLTES, label="Runge Kutta")

            ltesPlot.legend()

            app.prevExactEnabled = app.frames[LTEPage].exactEnabledVar.get()
            app.prevEulerEnabled = app.frames[LTEPage].eulerEnabledVar.get()
            app.prevImprovedEulerEnabled = app.frames[LTEPage].improvedEulerEnabledVar.get()
            app.prevRungeKuttaEnabled = app.frames[LTEPage].rungeKuttaEnabledVar.get()
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

        self.prevExactEnabled = 0
        self.prevEulerEnabled = 0
        self.prevImprovedEulerEnabled = 0
        self.prevRungeKuttaEnabled = 0

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, LTEPage):
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


        secondPageButton = ttk.Button(self, text="LTE / GTE", command=lambda: controller.show_frame(LTEPage))
        secondPageButton.grid(row=8, column=0)

        canvas = FigureCanvasTkAgg(approxFigure, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=8)

        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row=8, columnspan=3)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()

class LTEPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.exactEnabledVar = tk.IntVar()
        self.eulerEnabledVar = tk.IntVar()
        self.improvedEulerEnabledVar = tk.IntVar()
        self.rungeKuttaEnabledVar = tk.IntVar()
        eulerEnabled = ttk.Checkbutton(self, text="Euler", variable=self.eulerEnabledVar).grid(row=0, column=0,
                                                                                               sticky="w")
        improvedEulerEnabled = ttk.Checkbutton(self, text="Improved Euler", variable=self.improvedEulerEnabledVar) \
            .grid(row=1, column=0, sticky="w")
        rungeKuttaEnabled = ttk.Checkbutton(self, text="Runge-Kutta", variable=self.rungeKuttaEnabledVar) \
            .grid(row=2, column=0, sticky="w")

        canvas = FigureCanvasTkAgg(approxFigure, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, rowspan=4)

        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainPage))
        backButton.grid(row=3, column=0)

class GTEPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        x0 = 1.0
        xFinal = 1.5
        y0 = 2
        step = 0.1

        xs, ys = platform.getPoints(x0, xFinal, y0, step)
        approxYs, ltes, gtes = platform.approximate(eulerApproximator, x0, xFinal, y0, step)
        ltes = platform.calcLTE(ys, x0, step, eulerApproximator)
        gtes = platform.calcGTE(ys, approxYs)

        labelN0 = ttk.Label(self, text="n0")
        labelN0.grid(row=0, column=0)
        self.textBoxN0 = tk.Text(self, width=app.textBoxWidth, height=1)
        self.textBoxN0.grid(row=0, column=1)

        labelN = ttk.Label(self, text="n")
        labelN.grid(row=0, column=0)
        self.textBoxN = tk.Text(self, width=app.textBoxWidth, height=1)
        self.textBoxN.grid(row=0, column=1)

        canvas = FigureCanvasTkAgg(gtesFigure, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainPage))
        backButton.grid(row=1, column=0)

app = MDEApp()
app.style = ttk.Style()
app.style.theme_use("clam")
animationMain = animation.FuncAnimation(approxFigure, animateMainPage, 1000)
# animationLTE = animation.FuncAnimation(ltesFigure, animateLTEPage, 1000)

app.mainloop()