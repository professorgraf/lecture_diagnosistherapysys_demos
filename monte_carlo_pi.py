# Monte-Carlo-Simulation Demonstrator to "estimate pi"
#
#  (c) 2024 - Prof. Dr. Markus Graf
#  Faculty of Informatics, University of Applied Sciences Heilbronn
#
# This programm "estimates pi" by the probability ratio of points being in a unity-circle compared
# to its bounding rectangle  Which leads to the fact that the probability of random points landing
# inside the circle in relation to landing in the rectangle is (if just enough points used) equal to
# the ratio of the surface of these geoemtric figures:
#
#  p(element in circle) = #elements in circle / #elements in total
#     = #elements in circle / #elements in rectangle
#     = A(circle) / A(rect)
#     = (pi x r^2) / (2xr)^2 = pi/4
#
#  IMPORTANT NOTE:
#  This project is just to demonstrate Monte-Carlo in a lecture and for the sake of simplicity
#  it uses python's built-in random() number generator!!!
#
#  Therefore, it does not make use of a "TRUE RANDOM NUMBER GENERATOR!!!"
#  which means: for a real monte-carlo simulation you want to make sure to have "REAL RANDOM NUMBERS"
#
#  Gnu GPL 3.0
#

import random
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import time


class UIWindow:
    VERSION = "0.9"

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Monte Carlo PI")
        self.running = True

        self.window.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.window, width=400, height=400, bg="white")
        self.canvas.grid(column=0, row=0, sticky='NWSE')
        # self.canvas.pack(expand=True, fill=tk.BOTH)

        self.result = tk.Label(self.window, text="Pi is approximately")
        self.result.grid(column=0, row=1, sticky='NW')

        self.points = []
        self.rectangle_count = 0
        self.circle_count = 0

        self.clear()

        self.canvas.bind("<Button-1>", self.add_points)

    def clear(self):
        self.points = []
        self.rectangle_count = 0
        self.circle_count = 0

    def add_points(self, event):
        if self.rectangle_count < 30:
            self.add_point(event)
        else:
            if self.rectangle_count < 2000:
                for i in range(0, 100):
                    self.add_point(event)
            else:
                for i in range(0, 1000):
                    self.add_point(event)

    def add_point(self, event):
        # x, y = event.x, event.y
        x = random.random()*2 - 1
        y = random.random()*2 - 1

        self.points.append((x, y))

        is_inside_circle = False

        self.rectangle_count += 1
        if x**2+y**2 <= 1:
            self.circle_count += 1
            is_inside_circle = True
        self.plot_point(200+(200*x), 200+200*y, is_inside_circle)

        self.result.config(text="Pi is approx. 4 x {}/{}  = {}".format(self.circle_count,
                                                                       self.rectangle_count,
                                                                       4*self.circle_count/self.rectangle_count))

    def plot_point(self, x, y, inside_circle):
        color_text = "blue"
        if inside_circle:
            color_text = "red"
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=color_text, outline=color_text)

    def mainloop(self):
        while self.running:
            self.window.update_idletasks()
            self.window.update()
            # react on when training thread is finished
            #if not self.queue.empty() and self.queue.get_nowait() == 1:
            #    self.update_results()
            time.sleep(0.1)


def main():
    app = UIWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
