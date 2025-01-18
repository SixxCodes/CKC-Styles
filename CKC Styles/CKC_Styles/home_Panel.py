import tkinter as tk
from tkinter.messagebox import askyesno

from myUser_Panel import myUser_Window
from homePage_Panel import homePage_Window
from myCart_Panel import myCart_Window
from myOrder_Panel import myOrder_Window
from logOut_Panel import logout_Window
from help_Panel import help_Window
from about_Panel import about_Window

'''
tanan mga nakabutang dri:
1. about sa HOME sa sidebar Menu sa Home Panel
2. homepage and home is different
    *homepage, kung aha ang mga display products
    *home, ang kinatibukan, dri nakabutang ang users, ang homepage, 
    ang cart, ang orders, ang log out, ang help, ang about.
    *mao ni sya ang main, dri nakabutang tanan
'''

mainColor = "#d1101a"

class home_Panel_Window:
    def __init__(self, username):
        self.window = tk.Tk()
        self.window.title("CKC Styles")
        self.window.state('zoomed')
        self.window.configure(bg='white')
        self.window.resizable(False, False)

#===================ALL GUI===================
        self.username = username

        tk.Label(
            self.window, 
            text="CKC Styles", 
            bg='#fff', 
            font=('Calibri', 20, 'bold')).place(x=10,y=10)

        #icon paths
        hamburgerIconPath = tk.PhotoImage(file='D:/Zyrile/School/2nd Year/1st Term/IT5/CKC Styles/icons/toggle_btn_icon.png')

        myUserIconPath = tk.PhotoImage(file='D:/Zyrile/School/2nd Year/1st Term/IT5/CKC Styles/icons/user_icon.png')
        homeIconPath = tk.PhotoImage(file='D:/Zyrile/School/2nd Year/1st Term/IT5/CKC Styles/icons/home_icon.png')
        myCartIconPath = tk.PhotoImage(file='D:/Zyrile/School/2nd Year/1st Term/IT5/CKC Styles/icons/cart_icon.png')
        myOrderIconPath = tk.PhotoImage(file='D:/Zyrile/School/2nd Year/1st Term/IT5/CKC Styles/icons/order_icon.png')
        logOutIconPath = tk.PhotoImage(file='D:/Zyrile/School/2nd Year/1st Term/IT5/CKC Styles/icons/logOut_icon.png')

        helpIconPath = tk.PhotoImage(file='D:/Zyrile/School/2nd Year/1st Term/IT5/CKC Styles/icons/help_icon.png')
        aboutIconPath = tk.PhotoImage(file='D:/Zyrile/School/2nd Year/1st Term/IT5/CKC Styles/icons/about_icon.png')

        menu_bar_frame = tk.Frame(
            self.window, 
            bg=mainColor)
        
        self.menu_extended = False

        #buttons
        hamburgerBtn = tk.Button(
            menu_bar_frame, 
            image=hamburgerIconPath, 
            bg=mainColor, 
            border=0,
            activebackground=mainColor)
        hamburgerBtn.config(command=lambda: extend_menu_bar(menu_bar_frame, hamburgerBtn, self.window))
        hamburgerBtn.place(x=4, y=10)

        myUserBtn = tk.Button(
            menu_bar_frame, 
            image=myUserIconPath,
            bg=mainColor, 
            border=0,
            activebackground=mainColor,
            command=lambda: switch_indicator(
                offIndicator1=homeBtnIndicator,
                offIndicator2=myCartBtnIndicator,
                offIndicator3=myOrderBtnIndicator,
                offIndicator4=logOutBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=myUserBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=myUser_page(page_frame(self.window), self.username)))
        myUserBtn.place(x=9, y=130, width=30, height=40)

        myUserBtnIndicator = tk.Label(
            menu_bar_frame,
            bg=mainColor)
        myUserBtnIndicator.place(x=3,y=130, height=40, width=3)

        myUserBtnLabel = tk.Label(
            menu_bar_frame,
            text="My Account",
            bg=mainColor,
            fg='white',
            font=('Bold', 15),
            anchor=tk.W)
        myUserBtnLabel.place(x=45, y=130, width=105, height=40)
        myUserBtnLabel.bind('<Button-1>', lambda e: switch_indicator(
                offIndicator1=homeBtnIndicator,
                offIndicator2=myCartBtnIndicator,
                offIndicator3=myOrderBtnIndicator,
                offIndicator4=logOutBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=myUserBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=myUser_page(page_frame(self.window), self.username)))

        homeBtn = tk.Button(
            menu_bar_frame, 
            image=homeIconPath,
            bg=mainColor, 
            border=0,
            activebackground=mainColor,
            command=lambda: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=myCartBtnIndicator,
                offIndicator3=myOrderBtnIndicator,
                offIndicator4=logOutBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=homeBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=home_page(page_frame(self.window), self.username)))
        homeBtn.place(x=9, y=190, width=30, height=40)

        homeBtnIndicator = tk.Label(
            menu_bar_frame,
            bg='white')
        homeBtnIndicator.place(x=3,y=190, height=40, width=3)

        homeBtnLabel = tk.Label(
            menu_bar_frame,
            text="Home",
            bg=mainColor,
            fg='white',
            font=('Bold', 15),
            anchor=tk.W)
        homeBtnLabel.place(x=45, y=190, width=100, height=40)
        homeBtnLabel.bind('<Button-1>', lambda e: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=myCartBtnIndicator,
                offIndicator3=myOrderBtnIndicator,
                offIndicator4=logOutBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=homeBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=home_page(page_frame(self.window), self.username)))
                
        myCartBtn = tk.Button(
            menu_bar_frame, 
            image=myCartIconPath,
            bg=mainColor, 
            border=0,
            activebackground=mainColor,
            command=lambda: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myOrderBtnIndicator,
                offIndicator4=logOutBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=myCartBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=myCart_page(page_frame(self.window), self.username)))
        myCartBtn.place(x=9, y=250, width=30, height=40)

        myCartBtnIndicator = tk.Label(
            menu_bar_frame,
            bg=mainColor)
        myCartBtnIndicator.place(x=3,y=250, height=40, width=3)

        myCartBtnLabel = tk.Label(
            menu_bar_frame,
            text="My Cart",
            bg=mainColor,
            fg='white',
            font=('Bold', 15),
            anchor=tk.W)
        myCartBtnLabel.place(x=45, y=250, width=100, height=40)
        myCartBtnLabel.bind('<Button-1>', lambda e: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myOrderBtnIndicator,
                offIndicator4=logOutBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=myCartBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=myCart_page(page_frame(self.window), self.username)))

        myOrderBtn = tk.Button(
            menu_bar_frame, 
            image=myOrderIconPath,
            bg=mainColor, 
            border=0,
            activebackground=mainColor,
            command=lambda: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=logOutBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=myOrderBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=myOrder_page(page_frame(self.window), self.username)))
        myOrderBtn.place(x=9, y=310, width=30, height=40)

        myOrderBtnIndicator = tk.Label(
            menu_bar_frame,
            bg=mainColor)
        myOrderBtnIndicator.place(x=3,y=310, height=40, width=3)

        myOrderBtnLabel = tk.Label(
            menu_bar_frame,
            text="My Orders",
            bg=mainColor,
            fg='white',
            font=('Bold', 15),
            anchor=tk.W)
        myOrderBtnLabel.place(x=45, y=310, width=100, height=40)
        myOrderBtnLabel.bind('<Button-1>', lambda e: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=logOutBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=myOrderBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=myOrder_page(page_frame(self.window), self.username)))

        logOutBtn = tk.Button(
            menu_bar_frame, 
            image=logOutIconPath,
            bg=mainColor, 
            border=0,
            activebackground=mainColor,
            command=lambda: switch_indicator_noNewPanel(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=myOrderBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=logOutBtnIndicator,
                menuBar=menu_bar_frame, 
                hamburgerBtn=hamburgerBtn, 
                window=self.window,
                page=logOut_page(self.window)))
        logOutBtn.place(x=9, y=370, width=30, height=40)

        logOutBtnIndicator = tk.Label(
            menu_bar_frame,
            bg=mainColor)
        logOutBtnIndicator.place(x=3,y=370, height=40, width=3)
        
        logOutBtnLabel = tk.Label(
            menu_bar_frame,
            text="Log Out",
            bg=mainColor,
            fg='white',
            font=('Bold', 15),
            anchor=tk.W)
        logOutBtnLabel.place(x=45, y=370, width=100, height=40)
        logOutBtnLabel.bind('<Button-1>', lambda e: switch_indicator_noNewPanel(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=myOrderBtnIndicator,
                offIndicator5=settingsBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=logOutBtnIndicator,
                menuBar=menu_bar_frame, 
                hamburgerBtn=hamburgerBtn, 
                window=self.window,
                page=logOut_page(self.window)))

        #COMMENTED, FOR FUTURE PURPOSES
        '''settingsBtn = tk.Button(
            menu_bar_frame, 
            image=settingsIconPath,
            bg=mainColor, 
            border=0,
            activebackground=mainColor,
            command=lambda: switch_indicator_noNewPanel(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=myOrderBtnIndicator,
                offIndicator5=logOutBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=settingsBtnIndicator,
                menuBar=menu_bar_frame, 
                hamburgerBtn=hamburgerBtn, 
                window=self.window,
                page=settings_page(self.window)))
        settingsBtn.place(x=9, y=470, width=30, height=40)'''

        #no purpose since commented ang settings but dont delete kay ginagamit sa uban functions
        settingsBtnIndicator = tk.Label(
            menu_bar_frame,
            bg=mainColor)
        settingsBtnIndicator.place(x=3,y=470, height=40, width=3)

        #COMMENTED, FOR FUTURE PURPOSES
        '''settingsBtnLabel = tk.Label(
            menu_bar_frame,
            text="Settings",
            bg=mainColor,
            fg='white',
            font=('Bold', 15),
            anchor=tk.W)
        settingsBtnLabel.place(x=45, y=470, width=100, height=40)
        settingsBtnLabel.bind('<Button-1>', lambda e: switch_indicator_noNewPanel(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=myOrderBtnIndicator,
                offIndicator5=logOutBtnIndicator,
                offIndicator6=helpBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=settingsBtnIndicator,
                menuBar=menu_bar_frame, 
                hamburgerBtn=hamburgerBtn, 
                window=self.window,
                page=settings_page(self.window)))'''

        helpBtn = tk.Button(
            menu_bar_frame, 
            image=helpIconPath,
            bg=mainColor, 
            border=0,
            activebackground=mainColor,
            command=lambda: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=myOrderBtnIndicator,
                offIndicator5=logOutBtnIndicator,
                offIndicator6=settingsBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=helpBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=help_page(page_frame(self.window))))
        helpBtn.place(x=9, y=530, width=30, height=40)

        helpBtnIndicator = tk.Label(
            menu_bar_frame,
            bg=mainColor)
        helpBtnIndicator.place(x=3,y=530, height=40, width=3)
        
        helpBtnLabel = tk.Label(
            menu_bar_frame,
            text="Help",
            bg=mainColor,
            fg='white',
            font=('Bold', 15),
            anchor=tk.W)
        helpBtnLabel.place(x=45, y=530, width=100, height=40)
        helpBtnLabel.bind('<Button-1>', lambda e: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=myOrderBtnIndicator,
                offIndicator5=logOutBtnIndicator,
                offIndicator6=settingsBtnIndicator,
                offIndicator7=aboutBtnIndicator,
                onIndicator=helpBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=help_page(page_frame(self.window))))

        aboutBtn = tk.Button(
            menu_bar_frame, 
            image=aboutIconPath,
            bg=mainColor, 
            border=0,
            activebackground=mainColor,
            command=lambda: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=myOrderBtnIndicator,
                offIndicator5=logOutBtnIndicator,
                offIndicator6=settingsBtnIndicator,
                offIndicator7=helpBtnIndicator,
                onIndicator=aboutBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=about_page(page_frame(self.window))))
        aboutBtn.place(x=9, y=590, width=30, height=40)
        
        aboutBtnIndicator = tk.Label(
            menu_bar_frame,
            bg=mainColor)
        aboutBtnIndicator.place(x=3,y=590, height=40, width=3)

        aboutBtnLabel = tk.Label(
            menu_bar_frame,
            text="About",
            bg=mainColor,
            fg='white',
            font=('Bold', 15),
            anchor=tk.W)
        aboutBtnLabel.place(x=45, y=590, width=100, height=40)
        aboutBtnLabel.bind('<Button-1>', lambda e: switch_indicator(
                offIndicator1=myUserBtnIndicator,
                offIndicator2=homeBtnIndicator,
                offIndicator3=myCartBtnIndicator,
                offIndicator4=myOrderBtnIndicator,
                offIndicator5=logOutBtnIndicator,
                offIndicator6=settingsBtnIndicator,
                offIndicator7=helpBtnIndicator,
                onIndicator=aboutBtnIndicator,
                menuBar=menu_bar_frame, hamburgerBtn=hamburgerBtn, window=self.window,
                pageFrame=page_frame(self.window),
                page=about_page(page_frame(self.window))))

        page_frame(self.window)
        home_page(page_frame(self.window), self.username)

        menu_bar_frame.pack(
            side="right", 
            fill="y")
        menu_bar_frame.pack_propagate(flag=False)
        menu_bar_frame.configure(width=45)

        self.window.protocol('WM_DELETE_WINDOW', lambda: self.confirm(self.window))
        self.window.mainloop()  #murag "window.setVisible(true);"

    def confirm(self, window):
        answer = askyesno(title="Exit", message="Are you sure you want to exit?")
        if answer:
            window.destroy()

#===================ALL PAGES===================
def page_frame(window):
    pageFrame = tk.Frame(window)
    pageFrame.place(relwidth=1.0, relheight=1.0, x=-45)
    return pageFrame

def myUser_page(mainFrame, username):
    myUser_Window(mainFrame, username)

def home_page(mainFrame, username):
    homePage_Window(mainFrame, username)
    
def myCart_page(mainFrame, username):
    myCart_Window(mainFrame, username)

def myOrder_page(mainFrame, username):
    myOrder_Window(mainFrame, username)

def logOut_page(mainFrame):
    def open_login_form():
        import tkinter as tk
        from start_Page import login_Panel_window

        login_Panel_window()

    logout_Window(mainFrame, open_login_form)

def help_page(mainFrame):
    help_Window(mainFrame)

def about_page(mainFrame):
    about_Window(mainFrame)
    
#switch pages nga naay window
def switch_indicator(offIndicator1, 
                     offIndicator2, 
                     offIndicator3, 
                     offIndicator4, 
                     offIndicator5, 
                     offIndicator6, 
                     offIndicator7, 
                     onIndicator,
                     menuBar,
                     hamburgerBtn, 
                     window,
                     pageFrame,
                     page):

    offIndicator1.config(bg=mainColor)
    offIndicator2.config(bg=mainColor)
    offIndicator3.config(bg=mainColor)
    offIndicator4.config(bg=mainColor)
    offIndicator5.config(bg=mainColor)
    offIndicator6.config(bg=mainColor)
    offIndicator7.config(bg=mainColor)

    onIndicator.config(bg='white')

    if menuBar.winfo_width() > 45:
        fold_menu_bar(menuBar, hamburgerBtn, window)

    #BACKUP CODE ONLY
    '''for frame in pageFrame.winfo_children():
        frame.destroy()

    page()'''

#switch pages nga wlay window
def switch_indicator_noNewPanel(offIndicator1, 
                     offIndicator2, 
                     offIndicator3, 
                     offIndicator4, 
                     offIndicator5, 
                     offIndicator6, 
                     offIndicator7, 
                     onIndicator,
                     menuBar,
                     hamburgerBtn, 
                     window,
                     page):

    offIndicator1.config(bg=mainColor)
    offIndicator2.config(bg=mainColor)
    offIndicator3.config(bg=mainColor)
    offIndicator4.config(bg=mainColor)
    offIndicator5.config(bg=mainColor)
    offIndicator6.config(bg=mainColor)
    offIndicator7.config(bg=mainColor)

    onIndicator.config(bg='white')

    if menuBar.winfo_width() > 45:
        fold_menu_bar(menuBar, hamburgerBtn, window)

    #BACKUP CODE ONLY
    '''for frame in pageFrame.winfo_children():
        frame.destroy()

    page()'''

#===================SIDEBAR ANIMATIONS===================
def extend_menu_bar(menuBar, hamburgerBtn, window):
    menuBar.lift()
    extend_animation(menuBar, window)
    hamburgerBtn.config(command=lambda: fold_menu_bar(menuBar, hamburgerBtn, window))

def fold_menu_bar(menuBar, hamburgerBtn, window):
    fold_animation(menuBar, window)
    hamburgerBtn.config(command=lambda: extend_menu_bar(menuBar, hamburgerBtn, window))

def fold_animation(menuBar, window, target_width=45):
    current_width = menuBar.winfo_width()

    if current_width > target_width:
        current_width -= 10
        menuBar.config(width=current_width)

        window.update_idletasks()

        window.after(8, lambda: fold_animation(menuBar, window, target_width))
    else:
        menuBar.config(width=target_width)

def extend_animation(menuBar, window, target_width=200):
    current_width = menuBar.winfo_width()

    if current_width < target_width:
        current_width += 10
        menuBar.config(width=current_width)

        window.update_idletasks()

        window.after(8, lambda: extend_animation(menuBar, window, target_width))
    else:
        menuBar.config(width=target_width)