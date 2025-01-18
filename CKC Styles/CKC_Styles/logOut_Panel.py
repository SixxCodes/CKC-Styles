import tkinter as tk

'''
tanan mga nakabutang dri:
1. ang pag logout nga naa sa sidebar menu sa home panel
2. mugawas lang ang isa ka gamay nga window nga naay cancel button
3. wait lang ug seconds to fully log out
'''

class logout_Window:
    def __init__(self, mainWindow, login_callback):
        self.mainWindow = mainWindow
        self.login_callback = login_callback
        self.logOutWindow = tk.Toplevel(mainWindow)
        self.logOutWindow.title("Logging Out")
        self.logOutWindow.geometry('200x100+600+300')
        self.logOutWindow.configure(bg='white')
        self.logOutWindow.resizable(False, False)

        self.cancelled = False 
        self.logOutWindow.after(3000, self.perform_logout)  

    def btns(self):
        logOutLbl = tk.Label(self.logOutWindow, text="Logging out...", bg='white')
        logOutLbl.place(x=50, y=20)

        cancelBtn = tk.Button(
            self.logOutWindow,
            text="Cancel",
            bg="#d1101a",
            fg="white",
            activebackground="#ff4d4d",
            activeforeground="white",
            border=0,
            command=self.close_window
        )
        cancelBtn.place(x=90, y=60)

    #if gi-cancel ang logging out
    def close_window(self):
        self.cancelled = True  
        self.logOutWindow.destroy()  

    #if mu-logout na jud
    def perform_logout(self):
        if not self.cancelled:
            self.logOutWindow.destroy()  
            self.mainWindow.destroy() 
            self.login_callback() 