import tkinter as tk
from tkinter import PhotoImage
import time

image_paths = ["C:/Users/USER/Pictures/Wallpaper/images1.png", 
               "C:/Users/USER/Pictures/Wallpaper/images2.png", 
               "C:/Users/USER/Pictures/Wallpaper/images1.png",
               "C:/Users/USER/Pictures/Wallpaper/images2.png"]

class ImageCarousel:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Carousel with Tkinter")
        self.root.geometry("500x450")

        self.images = [PhotoImage(file=img) for img in image_paths]
        self.current_index = 0

        self.canvas = tk.Canvas(root, width=500, height=350)
        self.canvas.pack()

        self.current_image = self.canvas.create_image(250, 175, image=self.images[self.current_index])

        self.prev_button = self.canvas.create_text(30, 175, text="<", font=("Arial", 24), fill="gray", state="hidden")
        self.next_button = self.canvas.create_text(470, 175, text=">", font=("Arial", 24), fill="gray", state="hidden")

        self.canvas.bind("<Enter>", self.show_buttons)
        self.canvas.bind("<Leave>", self.hide_buttons)

        self.dot_frame = tk.Frame(root)
        self.dot_frame.pack(pady=10)
        self.dots = []
        self.create_dots()

        self.auto_slide_delay = 3000  # 3 seconds
        self.last_activity_time = time.time()
        self.start_auto_slide()

    def create_dots(self):
        for i in range(len(self.images)):
            dot = tk.Label(self.dot_frame, text="●", font=("Arial", 14), fg="gray")
            dot.grid(row=0, column=i, padx=5)
            self.dots.append(dot)
        self.update_dots()

    def update_dots(self):
        for i, dot in enumerate(self.dots):
            if i == self.current_index:
                dot.config(fg="black")  # Active dot
            else:
                dot.config(fg="gray")   # Inactive dots

    def show_buttons(self, event):
        self.canvas.itemconfig(self.prev_button, state="normal")
        self.canvas.itemconfig(self.next_button, state="normal")

    def hide_buttons(self, event):
        self.canvas.itemconfig(self.prev_button, state="hidden")
        self.canvas.itemconfig(self.next_button, state="hidden")

    def slide_image(self, new_index, direction="left"):
        if direction == "left":
            start_x = 750  # New image starts off-screen to the right
            step = -10
        else:
            start_x = -250  # New image starts off-screen to the left
            step = 10

        new_image = self.canvas.create_image(start_x, 175, image=self.images[new_index])

        for _ in range(50):  # 50 steps for smooth animation
            self.canvas.move(self.current_image, step, 0)
            self.canvas.move(new_image, step, 0)
            self.root.update()
            time.sleep(0.01)

        self.canvas.delete(self.current_image)
        self.current_image = new_image
        self.current_index = new_index
        self.update_dots()

    def next_image(self, event=None):
        new_index = (self.current_index + 1) % len(self.images)
        self.slide_image(new_index, direction="left")
        self.last_activity_time = time.time()

    def prev_image(self, event=None):
        new_index = (self.current_index - 1) % len(self.images)
        self.slide_image(new_index, direction="right")
        self.last_activity_time = time.time()

    def start_auto_slide(self):
        if time.time() - self.last_activity_time > self.auto_slide_delay / 1000:
            self.next_image()
        self.root.after(self.auto_slide_delay, self.start_auto_slide)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    carousel = ImageCarousel(root)

    root.after(10, lambda: carousel.canvas.tag_bind(carousel.prev_button, "<Button-1>", carousel.prev_image))
    root.after(10, lambda: carousel.canvas.tag_bind(carousel.next_button, "<Button-1>", carousel.next_image))

    root.mainloop()