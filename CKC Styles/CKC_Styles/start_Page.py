import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import askyesno
from home_Panel import home_Panel_Window
import json
import tkinter.messagebox as msgbox
import os
'''
different imports ni sya nga okay ra gud isahon ang uban 
pero i need this to be like this para lang timailhan sa code nako
'''

class login_Panel_window:
    def __init__(self):#constructor ani nga class
        #main window
        self.window = tk.Tk()
        self.window.title("Login to CKC Styles")
        self.window.geometry('925x500+200+120')
        self.window.configure(bg="#fff")
        self.window.resizable(False, False)

        self.setup_ui() #ang mga UI

        self.window.protocol('WM_DELETE_WINDOW', lambda: self.confirm(self.window))
        self.window.mainloop()  #murag "window.setVisible(true);"
    
    #para pag mag-exit ka kay magpa-confirm pa sya
    def confirm(self, window):
        answer = askyesno(title="Exit", message="Are you sure you want to exit?")
        if answer:
            window.destroy()

#--------------------TANAN UI NA DRI--------------------
    def setup_ui(self):
        self.container = tk.Frame(self.window, width=925, height=500, bg='white')
        self.container.pack()

        #logo (left)
        self.image = tk.PhotoImage(file='D:/Zyrile/School/2nd Year/1st Term/IT5/CKC Styles/image design/logo.png')
        self.image_label = tk.Label(
            self.container, 
            image=self.image, 
            bg='white')
        self.image_label.place(x=0, y=80)

        #frame sa login (right)
        self.login_frame = tk.Frame(
            self.container, 
            width=350, 
            height=350, 
            bg='white')
        self.login_frame.place(x=480, y=70)
        
        #--------------------LOGIN UI--------------------
        #"Login"
        loginHeading = tk.Label(
            self.login_frame, 
            text='Log In', 
            fg='#d1101a', 
            bg='white', 
            font=('Microsoft YaHei UI Light', 23, 'bold'))
        loginHeading.place(x=30, y=5)

        #username entry
        self.user = tk.Entry(
            self.login_frame, 
            width=35, 
            fg='black', 
            border=0, 
            bg='white', 
            font=('Microsoft YaHei UI Light', 11))
        self.user.place(x=30, y=80)
        self.user.insert(0, "Enter username")
        self.user.bind('<FocusIn>', self.on_enter_user)
        self.user.bind('<FocusOut>', self.on_leave_user)

        #linya lang sa baba (istitik)
        tk.Frame(
            self.login_frame, 
            width=295, 
            height=2, 
            bg='black').place(x=25, y=107)

        #password
        self.pass_login = tk.Entry(
            self.login_frame, 
            width=35, 
            fg='black', 
            border=0, 
            bg='white', 
            font=('Microsoft YaHei UI Light', 11,))
        self.pass_login.place(x=30, y=150)
        self.pass_login.insert(0, "Enter password")
        self.pass_login.bind('<FocusIn>', self.on_enter_pass)
        self.pass_login.bind('<FocusOut>', self.on_leave_pass)

        #linya lang sa baba (istitik)
        tk.Frame(
            self.login_frame, 
            width=295, 
            height=2, 
            bg='black').place(x=25, y=177)

        #Login Button
        self.login_button = tk.Button(
            self.login_frame, 
            text="LOG IN", 
            bg="#d1101a", 
            fg="white", 
            activebackground="#ff4d4d",
            activeforeground="white",
            border=0,
            width = 39,
            pady=7,
            command=lambda: self.handle_login()
        )
        self.login_button.place(x=35, y=204)
        self.login_button.bind("<Enter>", self.on_hover)
        self.login_button.bind("<Leave>", self.on_leave)

        #Sign-up parts nga naa sa login frame
        label = tk.Label(
            self.login_frame, 
            text='New to CKC Styles?', 
            fg='black', 
            bg='white', 
            font=('Microsoft YaHei UI Light', 9))
        label.place(x=86, y=270)

        sign_up_label = tk.Button(
            self.login_frame, 
            width=6, 
            text="Sign Up", 
            border=0, 
            bg='white', 
            cursor='hand2', 
            fg='#d1101a',
            command=self.show_signup)
        sign_up_label.place(x=205, y=270)

        #--------------------SIGN UP UI--------------------
        #Signup frame (hidden sa ni sya)
        self.signup_frame = tk.Frame(
            self.container, 
            width=350, 
            height=350, 
            bg='white')
        
        #"Sign Up"
        tk.Label(
            self.signup_frame, 
            text='Sign Up', 
            fg='#d1101a', 
            bg='white', 
            font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=30, y=5)

        #signup username
        self.signupUser = tk.Entry(
            self.signup_frame,
            width=35, 
            fg='black', 
            border=0, 
            bg='white', 
            font=('Microsoft YaHei UI Light', 11))
        self.signupUser.place(x=30, y=80)
        self.signupUser.insert(0, "Enter username")
        self.signupUser.bind('<FocusIn>', self.on_enter_Suser)
        self.signupUser.bind('<FocusOut>', self.on_leave_Suser)
        
        #linya lang sa baba (istitik)
        tk.Frame(
            self.signup_frame, 
            width=295, 
            height=2, 
            bg='black').place(x=25, y=107)

        #sign up pass
        self.signup_pass = tk.Entry(
            self.signup_frame, 
            width=35, 
            fg='black', 
            border=0, 
            bg='white', 
            font=('Microsoft YaHei UI Light', 11))
        self.signup_pass.place(x=30, y=150)
        self.signup_pass.insert(0, "Enter password")
        self.signup_pass.bind('<FocusIn>', self.on_enter_Spass)
        self.signup_pass.bind('<FocusOut>', self.on_leave_Spass)

        #linya lang sa baba (istitik)
        tk.Frame(
            self.signup_frame, 
            width=295, 
            height=2, 
            bg='black').place(x=25, y=177)
        
        #sign up re-enter pass
        self.signup_reenterPass = tk.Entry(
            self.signup_frame, 
            width=35, 
            fg='black', 
            border=0, 
            bg='white', 
            font=('Microsoft YaHei UI Light', 11))
        self.signup_reenterPass.place(x=30, y=220)
        self.signup_reenterPass.insert(0, "Re-enter password")
        self.signup_reenterPass.bind('<FocusIn>', self.on_reenter_Spass)
        self.signup_reenterPass.bind('<FocusOut>', self.on_releave_Spass)

        tk.Frame(
            self.signup_frame, 
            width=295, 
            height=2, 
            bg='black').place(x=25, y=247)

        #sign up button
        self.signup_button = tk.Button(
            self.signup_frame, 
            width=39, 
            pady=7, 
            text='SIGN UP', 
            bg='#d1101a', 
            fg='white',
            command=lambda: self.signup_user(), 
            border=0).place(x=35, y=274)

        label_signup = tk.Label(
            self.signup_frame, 
            text='Already have an account?', 
            fg='black', 
            bg='white', 
            font=('Microsoft YaHei UI Light', 9))
        label_signup.place(x=80, y=330)

        #log in aron mubalik sa log in
        self.back_button = tk.Button(
            self.signup_frame, 
            text="Log In ", 
            border=0, 
            bg='white', 
            cursor='hand2', 
            fg='#d1101a', 
            command=self.go_back)
        self.back_button.place(x=230, y=330)

#--------------------FOR BACKEND OF USER SIGNUP AND LOGIN--------------------
    #for login
    """
    ga-handle sa pag log-in sa user
    ga-check if naa ba sa database ang imohang gi-enter nga username
    """
    def handle_login(self):
        username = self.user.get() #kwaon ang gi-enter sa entry
        password = self.pass_login.get() #kwaon ang gi-enter sa entry

        #debugging message aron mabaw-an nga ang error is tungod kay wla pay nahimong database
        db_path = "database.json"
        if not os.path.exists(db_path):
            messagebox.showerror("Error", "Database not found. Please sign up first.")
            return

        #ug naa ang database, i-read
        with open(db_path, "r") as db_file:
            data = json.load(db_file)

        user_found = False
        password_correct = False

        for user in data.get("users", []):
            if user["username"] == username:
                user_found = True
                if user["password"] == password:
                    password_correct = True
                break

        if user_found and password_correct:
            messagebox.showinfo("Welcome", f"Welcome to CKC Styles, {username}!") #i-welcome ang user ug naa syay account na
            self.window.destroy()  #i-close ang login nya proceed na sa main content
            self.show_user_panel(username)
            home_Panel_Window(username)  #show ang main content
        elif not user_found and not password_correct:
            messagebox.showerror("Invalid", "Invalid username and password!")
        elif user_found and not password_correct:
            messagebox.showerror("Invalid", "Invalid password!")
        elif not user_found:
            messagebox.showerror("Invalid", "Invalid username!")

    '''
    indirect import aron ma-avoid ang circular import
    the logic: from login -> main content -> logout -> login -> main content...
    pero for some reasons, dli musugot si python na naay patuyok nga import
    pero to make the login main content logout possible
    mao ni ang solution
    '''
    def show_user_panel(self, username):
        from home_Panel import home_Panel_Window
        home_panel = home_Panel_Window(username)  

    #for sign up
    #i-load tanan users aron mabaw-an ang mga user sa database
    def load_users(self):
        try:
            with open('database.json', 'r') as file:
                data = json.load(file)
                return data.get("users", [])
        except FileNotFoundError:
            return [] 
        except json.JSONDecodeError:
            return [] 
        
    #i-save ang bag-ong gibutang nga user
    def save_users(self, users):
        try:
            with open('database.json', 'r+') as file:
                data = json.load(file)
                data["users"] = users  
                file.seek(0)
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving users: {e}")

    def signup_user(self):
        #kwaon tanan mga gipangbutang sa entries
        username = self.signupUser.get()
        password = self.signup_pass.get()
        reentered_password = self.signup_reenterPass.get()

        if password != reentered_password:
            msgbox.showerror("Error", "Passwords do not match!")
            return

        if not username.strip() or not password.strip():
            msgbox.showerror("Error", "Username or Password cannot be empty!")
            return

        #i-load tanan aron ma-compare nato sa database if existing na ba ang username nga gi-input
        users = self.load_users()

        if any(user["username"] == username for user in users):
            msgbox.showerror("Error", "Username already exists!")
            return

        #if new user jud, buhatan na syag ing-ani nga dictionary sa database
        new_user = {
            "user_id": len(users) + 1,  
            "username": username,
            "password": password,  
            "profileUser": "",
            "firstName": "", 
            "lastName": "", 
            "email": "", 
            "phoneNum": "",  
            "address": "",  
            "gender": "",
            "birthday": "",
            "is_seller": False,
            "shop_name": "",
            "bio_seller": "",
            "cart": [], 
            "orders": [] #
        }

        users.insert(0, new_user)

        #save
        self.save_users(users)
        
        #messagebox aron mabaw-an nga confirmed na ang signing
        msgbox.showinfo("Success", f"User {username} created successfully!")

 #--------------------PAMPALIGHT SA BUTTON IF MUDUOL ANG CURSOR--------------------
    def on_hover(self, event):
        self.login_button.configure(bg="#ff4d4d") 

    def on_leave(self, event):
        self.login_button.configure(bg="#d1101a")

#--------------------PLACEHOLDERS SA LOGIN--------------------
    def on_enter_user(self, event):
        if self.user.get() == "Enter username":
            self.user.delete(0, tk.END)
            self.user.config(fg="black")

    def on_leave_user(self, event):
        if not self.user.get():
            self.user.insert(0, "Enter username")
            self.user.config(fg="black")

    def on_enter_pass(self, event):
        if self.pass_login.get() == "Enter password":
            self.pass_login.delete(0, tk.END)
            self.pass_login.config(fg="black", show="✧")

    def on_leave_pass(self, event):
        if not self.pass_login.get():
            self.pass_login.insert(0, "Enter password")
            self.pass_login.config(fg="black", show="")

#--------------------PLACEHOLDERS SA SIGNUP--------------------
    def on_enter_Suser(self, event):
        if self.signupUser.get() == "Enter username":
            self.signupUser.delete(0, tk.END)
            self.signupUser.config(fg="black")

    def on_leave_Suser(self, event):
        if not self.signupUser.get():
            self.signupUser.insert(0, "Enter username")
            self.signupUser.config(fg="black")

    def on_enter_Spass(self, event):
        if self.signup_pass.get() == "Enter password":
            self.signup_pass.delete(0, tk.END)
            self.signup_pass.config(fg="black", show="✧")

    def on_leave_Spass(self, event):
        if not self.signup_pass.get():
            self.signup_pass.insert(0, "Enter password")
            self.signup_pass.config(fg="black", show="")

    def on_reenter_Spass(self, event):
        if self.signup_reenterPass.get() == "Re-enter password":
            self.signup_reenterPass.delete(0, tk.END)
            self.signup_reenterPass.config(fg="black", show="✧")

    def on_releave_Spass(self, event):
        if not self.signup_reenterPass.get():
            self.signup_reenterPass.insert(0, "Re-enter password")
            self.signup_reenterPass.config(fg="black", show="")

#--------------------PARA SA SLIDE ANIMATIONS SA LOGIN AND SIGNUP--------------------
    def show_signup(self):
        self.animate_slide()

    def animate_slide(self):
        step = 10
        login_x = 480
        signup_x = 925

        def slide():
            nonlocal login_x, signup_x
            if login_x < 925:
                self.login_frame.place(x=login_x, y=70)
                login_x += step

                self.signup_frame.place(x=signup_x, y=70)
                signup_x -= step

                self.window.after(10, slide)
            else:
                self.login_frame.place_forget()
                self.signup_frame.place(x=480, y=70)

        self.signup_frame.place(x=925, y=70)
        slide()

    def go_back(self):
        step = 10
        login_x = 925
        signup_x = 480

        def slide_back():
            nonlocal login_x, signup_x
            if login_x > 480:
                self.login_frame.place(x=login_x, y=70)
                login_x -= step

                self.signup_frame.place(x=signup_x, y=70)
                signup_x += step

                self.window.after(10, slide_back)
            else:
                self.signup_frame.place_forget()
                self.login_frame.place(x=480, y=70)

        self.signup_frame.place(x=480, y=70)
        slide_back()

'''
mao ra ni sya ang .py file nga ma-run kay naa dri ang 
main which is dapat sad kay mao mn ni sya aha ka mag-log in nga .py file
'''
if __name__ == "__main__":
    login_Panel_window()