import tkinter as tk
from start_Page import StartPage

def open_login_form():
    root = tk.Tk()
    StartPage(root)
    root.mainloop()