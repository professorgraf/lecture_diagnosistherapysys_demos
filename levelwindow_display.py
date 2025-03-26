# Medical Image Viewer Demo - Image adjustment Demonstrator
#
#  shows the concept of level / window adjustments (especially for CT images)
#
#  (c) 2025 - Prof. Dr. Markus Graf
#  Faculty of Informatics, University of Applied Sciences Heilbronn
#
#  Gnu GPL 3.0
#

import numpy as np
import pydicom
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

class MedicalImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Image Viewer")

        self.initial_level = 40
        self.initial_window = 80

        # load the image
        self.load_button = tk.Button(root, text="Load Image...", command=self.load_image)
        self.load_button.pack(side=tk.TOP)
        self.img_title = tk.Label(root, text="-")
        self.img_title.pack(side=tk.TOP)

        # display the image
        self.image_label = tk.Label(root)
        self.image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # sliders for level and window
        self.level_slider = tk.Scale(root, label="Level", from_=-1024, to=3071, orient=tk.HORIZONTAL, command=self.update_image)
        self.level_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.level_slider.set(self.initial_level)
        self.window_slider = tk.Scale(root, label="Window", from_=1, to=4096, orient=tk.HORIZONTAL, command=self.update_image)
        self.window_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.window_slider.set(self.initial_window)

        # Initialize variables
        self.image = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # self.image = np.array(Image.open(file_path)) # cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            dicom_image = pydicom.dcmread(file_path)
            self.image = np.array(dicom_image.pixel_array, dtype=int)

            # bring the image into hounsfield units
            if hasattr(dicom_image, "RescaleIntercept"):
                self.image = dicom_image.RescaleSlope * self.image + dicom_image.RescaleIntercept

            print(f"min: {self.image.min()}, max: {self.image.max()}")
            if self.image is not None:
                self.img_title.config(text=os.path.split(file_path)[1])
                self.display_image()

    def apply_level_window(self, image, level, window):
        min_val = level - (window / 2)
        max_val = level + (window / 2)
        windowed_image = np.clip(image, min_val, max_val)
        windowed_image = ((windowed_image - (min_val)) / window) * 255
        print(f"{windowed_image.min()},{windowed_image.max()} ")
        return windowed_image.astype(np.uint8)

    def display_image(self):
        level = self.level_slider.get()
        window = self.window_slider.get()
        windowed_image = self.apply_level_window(self.image, level, window)
        pil_image = Image.fromarray(windowed_image)
        tk_image = ImageTk.PhotoImage(image=pil_image)

        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

    def update_image(self, val):
        if self.image is not None:
            level = self.level_slider.get()
            window = self.window_slider.get()
            windowed_image = self.apply_level_window(self.image, level, window)
            pil_image = Image.fromarray(windowed_image)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("520x420")
    app = MedicalImageViewer(root)
    root.mainloop()



'''
    head and neck
        brain W:80 L:40
        subdural W:130-300 L:50-100
        stroke W:8 L:32 or W:40 L:40 3
        temporal bones W:2800 L:600 or W:4000 L:700
        soft tissues: W:350–400 L:20–60 4

    chest
        lungs W:1500 L:-600
        mediastinum W:350 L:50
        vascular/heart W: 600 L: 200 or e.g. W: 1000 L: 400

    abdomen
        soft tissues W:400 L:50
        liver W:150 L:30

    spine
        soft tissues W:250 L:50
        bone W:1800 L:400
'''