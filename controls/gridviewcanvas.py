
import tkinter as tk


class Marker:
    def __init__(self, item, x, y, text_item=None):
        self.position = [x, y]
        self.item = item
        self.text_item = text_item
        self.translation = None


class GridViewCanvas(tk.Canvas):
    class MarkerSetting:
        def __init__(self, style='rectangle', color='magenta'):
            self.style = style
            self.color = color

    def __init__(self, parent, grid_dist=30, *kwargs):
        super().__init__(parent, *kwargs)
        self.grid_distance = grid_dist

        self.counter = 0

        self.marker_settings = dict()
        self.marker_settings['default'] = self.MarkerSetting()
        self.command = 'default'
        self.marker_lists = dict()
        self.selected_marker = None
        self.marker_radius_px = 5

        for i in range(0, 100):
            line = self.create_line(0, int(i * self.grid_distance), 1000, int(i * self.grid_distance), fill='blue')
            line = self.create_line(int(i * grid_dist), 0, int(i * grid_dist), 1000, fill='blue')

        self.bind('<ButtonPress-1>', self.__on_mouse_press)
        self.bind('<B1-Motion>', self.__on_mouse_drag)
        self.bind('<ButtonRelease-1>', self.__on_mouse_release)

    def get_marker_on_canvas(self, x, y):
        for lists in self.marker_lists.values():
            for marker in lists:
                bbox = self.coords(marker.item)  # get image area
                if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
                    return marker # marker found
        return None # no marker found

    def clear_all_markers(self):
        for lists in self.marker_lists.values():
            for marker in lists:
                self.delete(marker.item)
                self.delete(marker.text_item)
                if marker.translation:
                    self.delete(marker.translation)
        self.marker_lists.clear()
        self.counter = 0
        # self.modified = False

    def get_marker_list(self):
        return self.marker_lists['default']

    def add_marker_at(self, x, y):
        canvas_click = [x, y]
        marker_radius = self.marker_radius_px
        if marker_radius < 2:
            marker_radius = 2
        if self.command not in self.marker_lists:
            self.marker_lists[self.command] = []
        try:
            setting = self.marker_settings[self.command]
        finally:
            setting = self.marker_settings['default']

        if setting.style == 'rectangle':
            mark = self.create_rectangle(canvas_click[0] - marker_radius, canvas_click[1] - marker_radius,
                                         canvas_click[0] + marker_radius, canvas_click[1] + marker_radius,
                                         width=2, outline=setting.color)
        elif setting.style == 'circle':
            mark = self.create_oval(canvas_click[0] - marker_radius, canvas_click[1] - marker_radius,
                                    canvas_click[0] + marker_radius, canvas_click[1] + marker_radius,
                                    width=2, outline=setting.color)
        else:
            mark = self.create_text(canvas_click[0] - marker_radius, canvas_click[1] - marker_radius,
                                    text='+', width=2, fill=setting.color)

        marker_text = self.create_text(canvas_click[0]+3*marker_radius, canvas_click[1]+2*marker_radius,
                                       text=F'{self.counter}', fill='red')
        self.counter += 1

        marker = Marker(mark, *canvas_click, marker_text)
        self.marker_lists[self.command].append(marker)
        self.selected_marker = marker
        # self.modified = True

    def set_translation(self, point_idx, vector):
        vector = self.create_line(self.marker_lists['default'][point_idx].position[0],
                                  self.marker_lists['default'][point_idx].position[1],
                                  self.marker_lists['default'][point_idx].position[0]+vector[0],
                                  self.marker_lists['default'][point_idx].position[1]+vector[1], fill='red')
        if self.marker_lists['default'][point_idx].translation:
            self.delete(self.marker_lists['default'][point_idx].translation)
        self.marker_lists['default'][point_idx].translation = vector

    def __on_mouse_press(self, event):
        canvas_click = [self.canvasx(event.x), self.canvasy(event.y)]

        marker_radius = self.marker_radius_px
        if marker_radius < 2:
            marker_radius = 2

        if self.selected_marker is not None:
            self.itemconfig(self.selected_marker.item, fill="")
        self.selected_marker = self.get_marker_on_canvas(canvas_click[0], canvas_click[1])

        if self.selected_marker is None:
            self.add_marker_at(canvas_click[0], canvas_click[1])

        self.itemconfig(self.selected_marker.item, fill="gray50")

    def __on_mouse_drag(self, event):
        marker_radius = self.marker_radius_px
        if marker_radius < 2:
            marker_radius = 2
        canvas_click = [self.canvasx(event.x), self.canvasy(event.y)]

        if self.selected_marker is not None:        # (self.command == 'select' or self.command == 'drag') and
            self.moveto(self.selected_marker.item, canvas_click[0]-marker_radius, canvas_click[1]-marker_radius)
            self.moveto(self.selected_marker.text_item, canvas_click[0]+2*marker_radius, canvas_click[1]+1*marker_radius)
            self.selected_marker.position = canvas_click
            # self.modified = True

    def __on_mouse_release(self, event):
        marker_radius = self.marker_radius_px

        if marker_radius < 2:
            marker_radius = 2
        canvas_click = [self.canvasx(event.x), self.canvasy(event.y)]

        if self.selected_marker is not None:
            self.moveto(self.selected_marker.item, canvas_click[0]-marker_radius, canvas_click[1]-marker_radius)
            self.moveto(self.selected_marker.text_item, canvas_click[0]+2*marker_radius, canvas_click[1]+1*marker_radius)
            self.selected_marker.position = canvas_click
            self.modified = True