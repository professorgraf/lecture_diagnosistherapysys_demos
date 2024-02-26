# Linear-Interpolation-Simulation Demonstrator
#
#  (c) 2024 - Prof. Dr. Markus Graf
#  Faculty of Informatics, University of Applied Sciences Heilbronn
#
#  Gnu GPL 3.0
#

import random
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import time
import numpy as np


def random_color():
    r = lambda: random.randint(0, 255)
    return '#{:02x}{:02x}{:02x}'.format(r(), r(), r())

def random_intensity():
    r = lambda: random.randint(0, 255)
    i = r()
    return '#{:02x}{:02x}{:02x}'.format(i, i, i)


def hex_to_rgb(hex_color):
    # Remove '#' if present
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]

    # Convert hexadecimal to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return r, g, b


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


class UIWindow:
    VERSION = "0.9"

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Linear Interpolation Demo")
        self.running = True
        self.show_intermediate_step = False

        self.window.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.window, width=400, height=400, bg="white")
        self.canvas.grid(column=0, row=0, sticky='NWSE')
        # self.canvas.pack(expand=True, fill=tk.BOTH)

        self.result = tk.Label(self.window, text="Drag the inner circle to interpolate. Right click to choose color.")
        self.result.grid(column=0, row=1, sticky='NW')

        # Matrices are as follows:
        # [ left up      right up   ]
        # [ left down    right down ]
        self.coords = [[ [25, 25],  [375, 25 ]],
                       [ [25, 375], [375, 375]]]
        self.rc = [['',''], ['','']]
        self.colors = [[random_intensity(), random_intensity()],
                       [random_intensity(), random_intensity()]]

        for n in range(0, 2):
            for m in range(0, 2):
                (x1, y1) = self.coords[n][m]
                self.rc[n][m] = self.canvas.create_rectangle(x1-25, y1-25, x1+25, y1+25,
                                                             fill=self.colors[n][m])
                self.canvas.tag_bind(self.rc[n][m], "<Button-2>", lambda event, i=n, j=m: self.change_color(event, i, j))

        self.temp_rect1 = self.canvas.create_rectangle(-50, 0, 0, 20, fill='white')
        self.temp_rect2 = self.canvas.create_rectangle(-50, 380, 0, 400, fill='white')

        self.position = [200, 200]
        self.draggable_element = self.canvas.create_oval(self.position[0] - 25, self.position[1] - 25,
                                                         self.position[0] + 25, self.position[1] + 25, fill="blue")

        self.canvas.tag_bind(self.draggable_element, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.draggable_element, "<ButtonRelease-1>", self.on_release)
        self.canvas.tag_bind(self.draggable_element, "<B1-Motion>", self.on_drag)

        self.canvas.tag_bind(self.draggable_element, "<Button-2>", self.on_toggle_intermediate_step)

    def interpolate_color(self, x, y):
        # calculate the interpolated color
        m = 0
        n = 0

        # gn = (xm+1-x)/(xm+1-xm) * color(xm,yn) + (x-xm)/(xm+1-xm) * color(xm+1, yn)
        rel_distance_to_right = (self.coords[n][m+1][0]-x)/(self.coords[n][m+1][0]-self.coords[n][m][0])
        rel_distance_to_left = (x-self.coords[n][m][0])/(self.coords[n][m+1][0]-self.coords[n][m][0])

        # with idx 0 --> upper linear interpolated color
        color_left = hex_to_rgb(self.colors[n][m])
        color_right = hex_to_rgb(self.colors[n][m+1])
        rgb0 = rel_distance_to_right * np.array(color_left) + rel_distance_to_left * np.array(color_right)
        if self.show_intermediate_step:
            r, g, b = rgb0
            color = rgb_to_hex(int(r), int(g), int(b))
            self.canvas.itemconfig(self.temp_rect1, fill=color)
            self.canvas.moveto(self.temp_rect1, 350*rel_distance_to_left, 0)
        else:
            self.canvas.moveto(self.temp_rect1, -50, 0)

        # with idx 1 --> lower linear interpolated color
        color_left = hex_to_rgb(self.colors[1][0])
        color_right = hex_to_rgb(self.colors[1][1])

        rgb1 = rel_distance_to_right*np.array(color_left) + rel_distance_to_left*np.array(color_right)
        if self.show_intermediate_step:
            r, g, b = rgb1
            color = rgb_to_hex(int(r), int(g), int(b))
            self.canvas.itemconfig(self.temp_rect2, fill=color)
            self.canvas.moveto(self.temp_rect2, 350*rel_distance_to_left, 380)
        else:
            self.canvas.moveto(self.temp_rect2, -50, 380)

        # now calculate relatively up and relatively down
        rel_distance_to_bottom = (self.coords[1][1][1]-y)/(self.coords[1][1][1]-self.coords[0][1][1])
        rel_distance_to_top = (y-self.coords[0][1][1])/(self.coords[1][1][1]-self.coords[0][1][1])

        r, g, b = rel_distance_to_bottom * rgb0 + rel_distance_to_top * rgb1

        color = rgb_to_hex(int(r), int(g), int(b))
        self.canvas.itemconfig(self.draggable_element, fill=color)

    def on_press(self, event):
        self.position[0] = event.x
        self.position[1] = event.y

    def on_release(self, event):
        self.interpolate_color( *self.position )

    def change_color(self, event, i, j):
        color = random_color()
        self.canvas.itemconfig(self.rc[i][j], fill=color)
        self.colors[i][j] = color

        # propagate color change to interpolation function
        self.interpolate_color( *self.position )

    def on_drag(self, event):
        dx = event.x - self.position[0]
        dy = event.y - self.position[1]

        if not (25 < self.position[0]+dx < 375):
            dx = 0
        if not (25 < self.position[1]+dy < 375):
            dy = 0
        self.position[0] += dx
        self.position[1] += dy
        # self.canvas.move(self.draggable_element, dx, dy)
        self.canvas.moveto(self.draggable_element, self.position[0]-25, self.position[1]-25)


        # recalculate the interpolation for the new position x,y
        self.interpolate_color( *self.position )

    def on_toggle_intermediate_step(self, event):
        self.show_intermediate_step = not self.show_intermediate_step
        self.interpolate_color( *self.position )

    def mainloop(self):
        while self.running:
            self.window.update_idletasks()
            self.window.update()
            # react on when training thread is finished
            #if not self.queue.empty() and self.queue.get_nowait() == 1:
            #    self.update_results()
            #time.sleep(0.1)


def main():
    app = UIWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
