import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps, ImageDraw
from tkinter import messagebox, simpledialog, filedialog
import json
'''
different imports ni sya nga okay ra gud isahon ang uban 
pero i need this to be like this para lang timailhan sa code nako
'''

'''
tanan mga nakabutang dri:
1. about sa User Panel sa sidebar Menu sa Home Panel
2. Fill up ka as a buyer
3. Pwede ka mahimog seller (if nakafill up na ka sa buyer form)
'''

mainColor = "#d1101a"

class myUser_Window:
    def __init__ (self, mainFrame, username):
        self.myUserPageFrame = tk.Frame(mainFrame)

        self.username = username 
        
        self.create_header()
        self.dp()
        self.left_User_Details()
        self.right_User_Frame()

        dividerFrame = tk.Frame(
            self.myUserPageFrame, 
            width=1, 
            height=500, 
            bg='black').place(x=500, y=140)

        self.myUserPageFrame.pack(fill=tk.BOTH, expand=True)
    
    def create_header(self):
        header_frame = tk.Frame(self.myUserPageFrame, bg=mainColor, height=60)
        header_frame.pack(side="top", fill="x")

#===================PROFILE PICTURE===================
    def dp(self, is_seller=False): 
        dpFrame = tk.Frame(self.myUserPageFrame, width=200, height=200)
        dpFrame.pack(side='left', padx=220, pady=40, anchor="n")

        profile_button = tk.Button(dpFrame, bd=0, command=lambda: self.change_profile_picture(profile_button, is_seller))
        profile_button.pack()

        profile_key = "profileSeller" if is_seller else "profileUser"
        self.load_profile_image(profile_button, profile_key, size=(100, 100))

    def crop_to_circle(self, image, size):
        #himuog lingin ang image
        image = image.resize(size, Image.Resampling.LANCZOS)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        result = ImageOps.fit(image, size, centering=(0.5, 0.5))
        result.putalpha(mask)
        return result

    def load_profile_image(self, button, profile_key, size=(100, 100)):
        user_data = self.get_current_user_data()
        profile_image_path = user_data.get(profile_key)

        if profile_image_path and os.path.exists(profile_image_path):
            image = Image.open(profile_image_path)
        else:
            #ug wla pay image, grey placeholder lang sa
            image = Image.new("RGB", size, color="grey")
            draw = ImageDraw.Draw(image)
            draw.ellipse((20, 20, size[0] - 20, size[1] - 20), fill="lightgrey")

        self.update_profile_button(button, image, size)

    def update_profile_button(self, button, image, size):
        #update sa dp
        cropped_image = self.crop_to_circle(image, size)
        photo = ImageTk.PhotoImage(cropped_image)
        button.config(image=photo)
        button.image = photo  

    def change_profile_picture(self, button, is_seller=False, size=(100, 100)):
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if file_path:
            image = Image.open(file_path)
            self.update_profile_button(button, image, size)

            profile_key = "profileSeller" if is_seller else "profileUser"
            user_data = self.get_current_user_data()
            user_data[profile_key] = file_path
            self.save_user_data(user_data)

#===================ABOUT BACKEND===================
    #kwaon ang data ana lang nga specific nga user
    def get_current_user_data(self):
        #read gikan sa json
        with open("database.json", "r") as file:
            database = json.load(file)
        
        users = database.get("users", [])
        
        #for loop aron pangitaon sa database ang user nga naggamit karon
        for user in users:
            if user["username"] == self.username:
                return user 
        
        raise ValueError("User not found in the database.")

    def save_user_data(self, user_data):
        with open("database.json", "r") as file:
            database = json.load(file)

        users = database.get("users", [])

        for user in users:
            if user["username"] == user_data["username"]:  
                user.update(user_data)  
                break

        with open("database.json", "w") as file:
            json.dump(database, file, indent=4)
 
    def load_user_name(self):
            db_path = "database.json"
            if not os.path.exists(db_path):
                return

            with open(db_path, "r") as db_file:
                data = json.load(db_file)

            current_username = self.username  

            for user in data["users"]:
                if user["username"] == current_username:
                    self.firstNameEnt.insert(0, user.get("firstName", ""))
                    self.lastNameEnt.insert(0, user.get("lastName", ""))
                    break

    def save_user_name(self, first_name, last_name):
        db_path = "database.json"
        if not os.path.exists(db_path):
            messagebox.showerror("Error", "Database not found.")
            return

        with open(db_path, "r") as db_file:
            data = json.load(db_file)

        current_username = self.username 

        user_found = False
        for user in data["users"]:
            if user["username"] == current_username:
                user_found = True
                user["firstName"] = first_name
                user["lastName"] = last_name
                break

        if user_found:
            with open(db_path, "w") as db_file:
                json.dump(data, db_file, indent=4)
            messagebox.showinfo("Success", "User details saved successfully!")
        else:
            messagebox.showerror("Error", "User not found in the database.")                

#===================USER DETAILS GUI===================
    def left_User_Details(self):
        username = tk.Label(
            self.myUserPageFrame, 
            text=f"{self.username}", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 14, 'bold'))
        username.place(x=146, y=210, width=250, height=40)

        firstNameLbl = tk.Label(
            self.myUserPageFrame, 
            text="First Name", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 14))
        firstNameLbl.place(x=10, y=260, width=230, height=40)

        self.firstNameEnt = tk.Entry(
            self.myUserPageFrame, 
            width=35, 
            fg='black', 
            border=1, 
            font=('Microsoft YaHei UI Light', 11))
        self.firstNameEnt.place(x=200, y=260, width=260, height=30)

        lastNameLbl = tk.Label(
            self.myUserPageFrame, 
            text="Last Name", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 14))
        lastNameLbl.place(x=10, y=320, width=230, height=40)

        self.lastNameEnt = tk.Entry(
            self.myUserPageFrame, 
            width=35, 
            fg='black', 
            border=1, 
            font=('Microsoft YaHei UI Light', 11))
        self.lastNameEnt.place(x=200, y=320, width=260, height=30)

        self.load_user_name()

        saveBtn = tk.Button(
            self.myUserPageFrame, 
            text="SAVE", 
            bg=mainColor, 
            fg="white", 
            activebackground="#ff4d4d",
            activeforeground="white",
            border=0,
            command=lambda: self.save_user_name(self.firstNameEnt.get(), self.lastNameEnt.get())
        )
        saveBtn.place(x=360, y=380, width=90, height=30)

        myStore = tk.Button(
            self.myUserPageFrame,
            bg=mainColor,
            fg='#fff',
            bd=0,
            text="My Store",
            activebackground="#ff4d4d",
            activeforeground="white",
            font=(14),
            command=self.myStore_Initial)
        myStore.place(x=100, y=630, width=150, height=40)

        #COMMENTED, JUST FOR FUTURE PURPOSES
        '''myWallet = tk.Button(
            self.myUserPageFrame, 
            text="My Wallet",
            fg='#fff',
            bg=mainColor,
            bd=0,
            activebackground="#ff4d4d",
            activeforeground="white",
            font=(14))
        myWallet.place(x=290, y=630, width=150, height=40)'''

    def right_User_Frame(self):
        rightUserFrame = tk.Frame(self.myUserPageFrame, height=900, width=1000)
        rightUserFrame.pack(side='right', padx=20, pady=20)

        rightUserDetails = tk.Frame(rightUserFrame, height=900, width=1000)
        rightUserDetails.pack(side='right')

        myAccountPgNm = tk.Label(
            rightUserDetails, 
            text="My Account", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 20, 'bold'))
        myAccountPgNm.place(x=8, y=10, width=160, height=40)

        messageLbl = tk.Label(
            rightUserDetails, 
            text="Manage and protect your account here.", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 13))
        messageLbl.place(x=8, y=48, width=305, height=40)

        emailAddressLbl = tk.Label(
            rightUserDetails, 
            text="Email Address", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 14))
        emailAddressLbl.place(x=40, y=120, width=129, height=40)

        self.emailAddressEnt = tk.Entry(
            rightUserDetails, 
            width=40, 
            fg='black', 
            border=1, 
            bg='white',
            font=('Microsoft YaHei UI Light', 14))
        self.emailAddressEnt.place(x=230, y=120)

        phoneNumberLbl = tk.Label(
            rightUserDetails, 
            text="Phone Number", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 14))
        phoneNumberLbl.place(x=40, y=180, width=140, height=40)

        self.phoneNumberEnt = tk.Entry(
            rightUserDetails, 
            width=40, 
            fg='black', 
            border=1, 
            bg='white',
            font=('Microsoft YaHei UI Light', 14))
        self.phoneNumberEnt.place(x=230, y=180)

        addressLbl = tk.Label(
            rightUserDetails, 
            text="Address", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 14))
        addressLbl.place(x=8, y=240, width=140, height=40)

        self.addressEnt = tk.Entry(
            rightUserDetails, 
            width=40, 
            fg='black', 
            border=1, 
            bg='white',
            font=('Microsoft YaHei UI Light', 14))
        self.addressEnt.place(x=230, y=240)

        genderLbl = tk.Label(
            rightUserDetails, 
            text="Gender", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 14))
        genderLbl.place(x=5, y=300, width=138, height=40)

        self.gender_var = tk.StringVar()

        femaleChkbtn = tk.Checkbutton(
            rightUserDetails,
            text="Female",
            indicatoron=True,
            border=1,
            variable=self.gender_var,      
            onvalue="Female",         
            offvalue="",
            font=('Microsoft YaHei UI Light', 14))
        femaleChkbtn.place(x=230, y=300, width=136, height=40)
        
        maleChkbtn = tk.Checkbutton(
            rightUserDetails,
            text="Male",
            indicatoron=True,
            border=1,
            variable=self.gender_var,
            onvalue="Male",
            offvalue="",
            font=('Microsoft YaHei UI Light', 14))
        maleChkbtn.place(x=384, y=300, width=136, height=40)
        
        otherChkbtn = tk.Checkbutton(
            rightUserDetails,
            text="Other",
            indicatoron=True,
            border=1,
            variable=self.gender_var,
            onvalue="Other",
            offvalue="",
            font=('Microsoft YaHei UI Light', 14))
        otherChkbtn.place(x=538, y=300, width=136, height=40)

        birthdayLbl = tk.Label(
            rightUserDetails, 
            text="Birthday", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 14))
        birthdayLbl.place(x=8, y=360, width=140, height=40)
        
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        self.monthVar = tk.StringVar()
        self.monthVar.set(months[0]) 

        monthCombobox = ttk.Combobox(
            rightUserDetails, 
            textvariable=self.monthVar, 
            values=months, 
            state="readonly",
            width=10, 
            font=('Microsoft YaHei UI Light', 14)
        )
        monthCombobox.place(x=230, y=360)

        days = [str(i) for i in range(1, 32)]
        self.dayVar = tk.StringVar()
        self.dayVar.set(days[0])

        dayCombobox = ttk.Combobox(
            rightUserDetails, 
            textvariable=self.dayVar, 
            values=days, 
            state="readonly",
            width=10, 
            font=('Microsoft YaHei UI Light', 14)
        )
        dayCombobox.place(x=384, y=360)

        years = [str(i) for i in range(1900, 2026)]    
        self.yearVar = tk.StringVar()
        self.yearVar.set(years[0])

        yearCombobox = ttk.Combobox(
            rightUserDetails, 
            textvariable=self.yearVar, 
            values=years, 
            state="readonly",
            width=10, 
            font=('Microsoft YaHei UI Light', 14)
        )
        yearCombobox.place(x=538, y=360)

        saveBtn = tk.Button(
            rightUserDetails, 
            text="SAVE", 
            bg=mainColor, 
            fg="white", 
            activebackground="#ff4d4d",
            activeforeground="white",
            border=0,
            command=lambda: self.save_user_details()
        )
        saveBtn.place(x=320, y=450, width=100, height=30)

        self.load_user_details()

#===================SA MGA GI-ENTER NA DETAILS===================
    def save_user_details(self):
        email = self.emailAddressEnt.get()
        phone = self.phoneNumberEnt.get()
        address = self.addressEnt.get()
        gender = self.gender_var.get()
        birthday = f"{self.monthVar.get()} {self.dayVar.get()}, {self.yearVar.get()}"

        db_path = "database.json"
        if not os.path.exists(db_path):
            messagebox.showerror("Error", "Database not found.")
            return

        with open(db_path, "r") as db_file:
            data = json.load(db_file)

        current_username = self.username 

        user_found = False
        for user in data["users"]:
            if user["username"] == current_username:
                user_found = True
                user["email"] = email
                user["phoneNum"] = phone
                user["address"] = address
                user["gender"] = gender
                user["birthday"] = birthday
                break

        if user_found:
            with open(db_path, "w") as db_file:
                json.dump(data, db_file, indent=4)
            messagebox.showinfo("Success", "User details saved successfully!")
        else:
            messagebox.showerror("Error", "User not found.")

    def load_user_details(self):
        db_path = "database.json"
        if not os.path.exists(db_path):
            return

        with open(db_path, "r") as db_file:
            data = json.load(db_file)

        current_username = self.username 

        for user in data["users"]:
            if user["username"] == current_username:
                self.emailAddressEnt.insert(0, user.get("email", ""))
                self.phoneNumberEnt.insert(0, user.get("phoneNum", ""))
                self.addressEnt.insert(0, user.get("address", ""))
                self.gender_var.set(user.get("gender", ""))
                birthday = user.get("birthday", "").split()
                if len(birthday) == 3:
                    self.monthVar.set(birthday[0])
                    self.dayVar.set(birthday[1])
                    self.yearVar.set(birthday[2])
                break


#===================SELLER===================
    #prompts and requirements bag-o ka pwede mahimo ug seller
    def myStore_Initial(self):
        db_path = "database.json"
        if not os.path.exists(db_path):
            messagebox.showerror("Error", "Database not found.")
            return

        with open(db_path, "r") as db_file:
            data = json.load(db_file)

        username = self.username #ang current user
        user_found = False
        buyer_details_filled = True 
        
        for user in data.get("users", []):
            if user["username"] == username:
                user_found = True

                '''
                i-check sa ug naka fill up ba ka
                if wla, dli ka pwede mahimog seller
                '''
                if not user["firstName"] or not user["lastName"] or not user["email"] or not user["phoneNum"] or not user["address"]:
                    buyer_details_filled = False

                '''
                Pare-enter ug password ug seller na
                for security purposes
                '''
                if user["is_seller"]:
                    # If the user is already a seller, prompt for password
                    password = simpledialog.askstring("Re-enter Password", "Please re-enter your password to access your store:", show="*")
                    if password == user["password"]:
                        seller_window = tk.Toplevel(self.myUserPageFrame)
                        seller_Page(seller_window, self, self.username)
                    else:
                        messagebox.showerror("Error", "Incorrect password. Access denied.")
                    return  # Exit after password validation
                    
                break
        
        if not user_found:
            messagebox.showerror("Error", "User not found.")
            return

        #if wla pa ka fill up sa tanan entries sa form, dli ka pwede mahimog seller
        if not buyer_details_filled:
            messagebox.showerror("Error", "Please complete your buyer details first before becoming a seller.")
            return

        #confirm if gusto ba jud mahimog seller
        response = messagebox.askyesno("Become a Seller", "Do you want to become a seller?")
        if not response:
            return  

        password = simpledialog.askstring("Re-enter Password", "Please re-enter your password:", show="*")

        for user in data.get("users", []):
            if user["username"] == username and password == user["password"]:
                #ang is_seller sa user nga naka false sa pinaka-una kay mahimo na ug True
                user["is_seller"] = True
                messagebox.showinfo("Success", "You are now a seller!")

                with open(db_path, "w") as db_file:
                    json.dump(data, db_file, indent=4)
                
                #open seller window nga sa hard code, nakabutang sa class nga seller_Page
                seller_window = tk.Toplevel(self.myUserPageFrame)
                seller_Page(seller_window, self, self.username)
                break
            elif user["username"] == username:
                messagebox.showerror("Error", "Incorrect password. Access denied.")
                break

class seller_Page:
    PROFILE_IMAGE_FILE_SELLER = "profile_image_seller.png"

    def __init__(self, root, user_page, username):
        self.root = root
        self.root.title("Seller Dashboard")
        self.root.geometry("1000x500+180+100")
        self.root.resizable(False, False)
        self.sellerPage = user_page

        self.username_inseller = username

        self.products = []
        self.orders = {
            "to_pay": [],
            "to_ship": [],
            "to_receive": [],
            "completed": [], 
            "return_and_refund": [] #not implented, for future purposes
        }

        self.dp()

        dividerFrame = tk.Frame(
            self.root, 
            width=1, 
            height=500, 
            bg='black').place(x=377, y=1)

        self.left_seller_Details()

        self.right_User_Frame()

        self.rightMainPagesFrame = tk.Frame(
            self.root, 
            height=900, 
            width=800,
            bg='pink')
        self.rightMainPagesFrame.pack(fill='both', expand=True, padx=10, pady=10)

        self.home_Panel(self.rightMainPagesFrame)

#===================SELLER DETAILS GUI===================
    def left_seller_Details(self):
        username = tk.Label(
            self.root, 
            text=f"{self.username_inseller}",
            fg='black', 
            font=('Microsoft YaHei UI Light', 14, 'bold'))
        username.place(x=143, y=130)

        storeNameLbl = tk.Label(
            self.root, 
            text="Store Name:", 
            fg='black', 
            font=('Microsoft YaHei UI Light', 14))
        storeNameLbl.place(x=10, y=170)

        self.storeNameEnt = tk.Entry(
            self.root, 
            width=35, 
            fg='black', 
            border=2, 
            font=('Microsoft YaHei UI Light', 11))
        self.storeNameEnt.place(x=130, y=170, width=235, height=30)

        storeMessage = tk.Label(
            self.root,
            text="Note: Once you enter your name, it will be final and cannot be changed.",
            fg='red',
            font=('Microsoft YaHei UI Light', 9),
            wraplength=300,
            justify='left')
        storeMessage.place(x=10, y=200)

        #doesnt do anything ang bio, para lang dli hawon tan-awon ang gui
        bioLbl = tk.Label(
            self.root,
            text="Bio:",
            fg='black',
            font=('Microsoft YaHei UI Light', 14))
        bioLbl.place(x=10, y=240)

        self.bioTb = tk.Text(
            self.root, 
            width=43, 
            height=10,
            bd=2)
        self.bioTb.place(x=10, y=270)

        self.load_seller_details()

        saveBtn = tk.Button(
            self.root,
            bg=mainColor,
            fg='#fff',
            bd=0,
            text="Save",
            activebackground="#ff4d4d",
            activeforeground="white",
            font=('Arial', 11),
            command=self.save_seller_details)
        saveBtn.place(x=250, y=450, width=100, height=30)

    def right_User_Frame(self):
        self.optionsFrame = tk.Frame(
            self.root,
            width=200, 
            height=35)
        self.optionsFrame.pack(fill='x', anchor='ne', pady=10)

        homeBtn = tk.Button(
            self.optionsFrame,
            text='Home',
            fg='black',
            bd=2,
            font=('Microsoft YaHei UI Light', 13, 'bold'),
            command= lambda: self.switch_Page(indicatorLb=homeBtnInd, page=self.home_Panel))
        homeBtn.place(x=0, y=0, width=125)

        homeBtnInd = tk.Label(
            self.optionsFrame,
            bg=mainColor)
        homeBtnInd.place(x=22, y=30, width=80, height=2)

        #COMMENTED OUT, FOR FUTURE PURPOSES
        '''
        orders= to notify the seller nga naa nay nag-buy sa ilahang product/s
        wallet= dra maadto ang ilahang earnings (naay tax)
        '''
        '''ordersBtn = tk.Button(
            self.optionsFrame,
            text='Orders',
            fg='black',
            bd=2,
            font=('Microsoft YaHei UI Light', 13, 'bold'),
            command= lambda: self.switch_Page(indicatorLb=ordersBtnInd, page=self.orders_Panel))
        ordersBtn.place(x=130, y=0, width=125)

        ordersBtnInd = tk.Label(
            self.optionsFrame)
        ordersBtnInd.place(x=152, y=30, width=80, height=2)

        walletBtn = tk.Button(
            self.optionsFrame,
            text='Wallet',
            fg='black',
            bd=2,
            font=('Microsoft YaHei UI Light', 13, 'bold'),
            command= lambda: self.switch_Page(indicatorLb=walletBtnInd, page=self.wallet_Panel))
        walletBtn.place(x=260, y=0, width=125)

        walletBtnInd = tk.Label(
            self.optionsFrame)
        walletBtnInd.place(x=282, y=30, width=80, height=2)'''

    def save_seller_details(self):
        # Retrieve the entered values
        store_name = self.storeNameEnt.get()
        bio_seller = self.bioTb.get("1.0", tk.END).strip()  # Get the text and strip any trailing newlines

        # Load the database
        db_path = "database.json"
        if not os.path.exists(db_path):
            messagebox.showerror("Error", "Database not found.")
            return

        with open(db_path, "r") as db_file:
            data = json.load(db_file)

        # Find the current user
        for user in data.get("users", []):
            if user["username"] == self.username_inseller:  # Assuming `self.current_user` holds the logged-in user info
                # Update the user's seller details
                user["shop_name"] = store_name
                user["bio_seller"] = bio_seller
                break

        # Save the updated data back to the file
        with open(db_path, "w") as db_file:
            json.dump(data, db_file, indent=4)

        messagebox.showinfo("Success", "Seller details saved successfully!")

    #para ang mga gi-save na ni user nga bio ug store name kay mupakita sa entries
    def load_seller_details(self):
        db_path = "database.json"
        
        if not os.path.exists(db_path):
            messagebox.showerror("Error", "Database not found.")
            return
        
        with open(db_path, "r") as db_file:
            data = json.load(db_file)
        
        for user in data.get("users", []):
            if user["username"] == self.username_inseller:  
                # Set the store name and bio if they exist
                self.storeNameEnt.insert(0, user.get("shop_name", ""))  #store name
                self.bioTb.insert("1.0", user.get("bio_seller", ""))  #bio
                break

    #to switch from home, orders, ug wallet   
    def switch_Page(self, indicatorLb, page):
        for child in self.optionsFrame.winfo_children():
            if isinstance(child, tk.Label):
                child['bg'] = '#f0f0f0'

        indicatorLb['bg'] = mainColor

        for fn in self.rightMainPagesFrame.winfo_children():
            fn.destroy()
            self.root.update()

        page(self.rightMainPagesFrame)

    def home_Panel(self, rightMainPagesFrame):
        homePageframe = tk.Frame(
            rightMainPagesFrame)
        homePageframe.pack(fill='both', expand=True)

        addProductBtn = tk.Button(
            homePageframe,
            text="Add Product",
            font=('Arial', 13),
            fg='white',
            bd=0,
            bg=mainColor,
            command=self.add_product_dialog)
        addProductBtn.pack(padx=5, pady=5)

        scrollable_frame = self.create_scrollable_frame(homePageframe)

        self.product_display_frame = tk.Frame(scrollable_frame)
        self.product_display_frame.pack(fill="both", expand=True)

        self.refresh_product_boxes()

    #not implemented, for future purposes
    def orders_Panel(self, rightMainPagesFrame):
        ordersPageframe = tk.Frame(
            rightMainPagesFrame,
            bg='gray')
        ordersPageframe.pack(fill='both', expand=True)

        lbl = tk.Label(
            ordersPageframe,
            text="Orders",
            font=('Microsoft YaHei UI Light', 20, 'bold'),
            fg='black')
        lbl.pack(padx=10, pady=10)

        scrollable_frame = self.create_scrollable_frame(ordersPageframe)

    def wallet_Panel(self, rightMainPagesFrame):
        walletPageframe = tk.Frame(
            rightMainPagesFrame)
        walletPageframe.pack(fill='both', expand=True)
        
        earningsLbl = tk.Label(
            walletPageframe,
            text="Earnings:",
            font=('Microsoft YaHei UI Light', 20, 'bold'),
            fg='black')
        earningsLbl.pack(padx=100, pady=20)

        pesosLbl = tk.Label(
            walletPageframe,
            text="P0.00",
            font=('Microsoft YaHei UI Light', 20, 'bold'),
            fg='black')
        pesosLbl.pack(padx=100, pady=20)

        withdrawBtn = tk.Button(
            walletPageframe,
            text="Withdraw",
            bg=mainColor,
            fg='white',
            activebackground="#ff4d4d",
            activeforeground="white",
            bd=0,
            font=('Arial', 15),
            command=self.withdraw_from_wallet)
        withdrawBtn.place(x=200, y=300, width=200, height=40)

#===================SELLER PRODUCTS===================
    '''
    for adding products
    pero dli ka pwede mag-add product if wla ka ka-enter sa shop name
    to avoid the "unknown seller" bug
    '''
    def add_product_dialog(self):
        store_name_seller = self.storeNameEnt.get()
        if not store_name_seller:
            messagebox.showerror("Error", "You must enter a shop name before adding products.")
            return

        name = simpledialog.askstring("Add Product", "Enter product name:")
        if not name:
            return

        colors = simpledialog.askstring("Add Product", "Enter available colors (comma-separated):")
        if not colors:
            return

        sizes = simpledialog.askstring("Add Product", "Enter available sizes (comma-separated):")
        if not sizes:
            return

        categories = simpledialog.askstring("Add Product", "Enter product categories (comma-separated):")
        if not categories:
            return

        stock_info = {}
        for color in colors.split(","):
            stock_info[color.strip()] = {}
            for size in sizes.split(","):
                stock = simpledialog.askinteger("Stock", f"Enter stock for {color.strip()} - {size.strip()}:")
                if stock is None:
                    return
                stock_info[color.strip()][size.strip()] = stock

        price = simpledialog.askfloat("Add Product", "Enter price:")
        if price is None:
            return

        voucher = simpledialog.askfloat("Add Product", "Enter discount voucher percentage (0-100, optional):", initialvalue=0.0)
        if voucher is None:
            voucher = 0.0

        images = []
        for _ in range(3):
            image_path = filedialog.askopenfilename(title="Select Product Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
            if image_path:
                images.append(image_path)
            else:
                break

        if not images:
            messagebox.showerror("Error", "At least one image is required.")
            return

        store_name_seller = self.storeNameEnt.get()

        '''
        mabutangan ang product sa database, separate sya sa users aron tanan users makakita sa tanan products nga na-add
        pero para dli masaag ang product ug kinsay seller niya, naa ang shop_names
        so, need jud nga naay shop name
        '''
        product = {
            "name": name,
            "colors": [color.strip() for color in colors.split(",")],
            "sizes": [size.strip() for size in sizes.split(",")],
            "categories": [category.strip() for category in categories.split(",")],
            "price": price,
            "stock_info": stock_info,
            "voucher": voucher,
            "shop_name": store_name_seller,  
            "purchases": [],
            "image": images,  
            "reviews": [],
            "purchases": [],
            "rating": 0, #not implemented, future purposes
            "sold": 0 #not implemented, future purposes
        }

        #add product to database.json
        db_path = "database.json"
        try:
            with open(db_path, "r") as db_file:
                data = json.load(db_file)

            if "products" not in data:
                data["products"] = []

            data["products"].append(product)

            with open(db_path, "w") as db_file:
                json.dump(data, db_file, indent=4)

            messagebox.showinfo("Success", f"Product '{name}' added successfully!")

            self.refresh_product_boxes()

        except FileNotFoundError:
            messagebox.showerror("Error", "Database file not found!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Database file is corrupted!")

    #aron ma-view ni seller ang iyahang products
    def refresh_product_boxes(self):
        store_name_seller = self.storeNameEnt.get()

        db_path = "database.json"
        try:
            with open(db_path, "r") as db_file:
                data = json.load(db_file)

            # Filter products for the current seller
            self.products = [product for product in data.get("products", []) if product["shop_name"] == store_name_seller]

        except FileNotFoundError:
            messagebox.showerror("Error", "Database file not found!")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Database file is corrupted!")
            return

        for widget in self.product_display_frame.winfo_children():
            widget.destroy()

        for index, product in enumerate(self.products):
            frame = tk.Frame(self.product_display_frame, bd=2, relief="ridge", padx=10, pady=10)
            frame.pack(pady=5, fill="x", expand=True)

            tk.Label(frame, text=f"Name: {product['name']}").pack(anchor="w")
            tk.Label(frame, text=f"Colors: {', '.join(product['colors'])}").pack(anchor="w")
            tk.Label(frame, text=f"Sizes: {', '.join(product['sizes'])}").pack(anchor="w")
            tk.Label(frame, text=f"Categories: {', '.join(product['categories'])}").pack(anchor="w")
            tk.Label(frame, text=f"Price: ₱{product['price']} | Discount: {product['voucher']}%").pack(anchor="w")
            tk.Label(frame, text=f"Images: {len(product['image'])} added").pack(anchor="w")

            stock_info = "Available Stocks:\n"
            for color, sizes in product["stock_info"].items():
                for size, stock in sizes.items():
                    stock_info += f"  {color} - {size}: {stock} left\n"
            tk.Label(frame, text=stock_info).pack(anchor="w")

            tk.Label(frame, text="________________________________________________________________________________________________________").pack(anchor="w")

            tk.Button(frame, text="Edit", command=lambda idx=index: self.edit_product(idx)).pack(side="left", padx=5)
            tk.Button(frame, text="Delete", command=lambda idx=index: self.delete_product(idx)).pack(side="right", padx=5)

    def edit_product(self, index):
        product = self.products[index]

        name = simpledialog.askstring("Edit Product", "Enter new product name:", initialvalue=product["name"])
        if name:
            product["name"] = name

        colors = simpledialog.askstring("Edit Product", "Enter new available colors (comma-separated):", initialvalue=",".join(product["colors"]))
        if colors:
            product["colors"] = [color.strip() for color in colors.split(",")]

        sizes = simpledialog.askstring("Edit Product", "Enter new available sizes (comma-separated):", initialvalue=",".join(product["sizes"]))
        if sizes:
            product["sizes"] = [size.strip() for size in sizes.split(",")]

        price = simpledialog.askfloat("Edit Product", "Enter new price:", initialvalue=product["price"])
        if price is not None:
            product["price"] = price

        voucher = simpledialog.askfloat("Edit Product", "Enter new discount voucher percentage (0-100):", initialvalue=product["voucher"])
        if voucher is not None:
            product["voucher"] = voucher

        stock_info = {}
        for color in product["colors"]:
            stock_info[color] = {}
            for size in product["sizes"]:
                stock_info[color][size] = simpledialog.askinteger("Stock", f"Enter stock for {color} - {size}:", initialvalue=product["stock_info"].get(color, {}).get(size, 0))
        product["stock_info"] = stock_info

        self.save_products_to_db()

        self.refresh_product_boxes()

    def save_products_to_db(self):
        db_path = "database.json"
        try:
            with open(db_path, "r") as db_file:
                data = json.load(db_file)

            if "products" not in data:
                data["products"] = []

            data["products"] = self.products  

            with open(db_path, "w") as db_file:
                json.dump(data, db_file, indent=4)

        except FileNotFoundError:
            messagebox.showerror("Error", "Database file not found!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Database file is corrupted!")

    def delete_product(self, index):
        if messagebox.askyesno("Delete Product", "Are you sure you want to delete this product?"):
            del self.products[index]

            self.save_products_to_db()

            self.refresh_product_boxes()

            messagebox.showinfo("Success", "Product deleted successfully!")

#===================OTHERS===================
    #naka-prepare nga frame nga pwede ma scroll
    def create_scrollable_frame(self, parent):
        frame = tk.Frame(parent)
        frame.pack_propagate(False)
        frame.configure(height=700)
        frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(self.canvas)
        scrollable_frame.pack(padx=5, pady=5)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        return scrollable_frame

    #para pwede m-scroll gamit ang mousewheel
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    #not implemented, for future purposes
    def withdraw_from_wallet(self):
        amount_to_withdraw = simpledialog.askinteger("Withdraw", "How much do you want to withdraw?", minvalue=1)
        
        if amount_to_withdraw is not None: 
            messagebox.showinfo("Withdrawal", f"{amount_to_withdraw} has been withdrawn from your seller wallet")
        else:
            messagebox.showinfo("Withdrawal", "No withdrawal was made.")

    #===================PROFILE PICTURE===================
    #para sa dp
    def dp(self, is_seller=False): 
        dpFrame = tk.Frame(self.root, width=200, height=200)
        dpFrame.pack(side='left', padx=140, pady=20, anchor="n")

        profile_button = tk.Button(
            dpFrame, 
            bd=0, 
            command=lambda: self.change_profile_picture(profile_button, is_seller))
        profile_button.pack()

        profile_key = "profileSeller" if is_seller else "profileUser"
        self.load_profile_image(profile_button, profile_key, size=(100, 100))

    def load_profile_image(self, button, profile_key, size=(100, 100)):
        user_data = self.get_current_user_data()  
        profile_image_path = user_data.get(profile_key)

        if profile_image_path and os.path.exists(profile_image_path):
            image = Image.open(profile_image_path)
        else:
            image = Image.new("RGB", size, color="grey")
            draw = ImageDraw.Draw(image)
            draw.ellipse((20, 20, size[0] - 20, size[1] - 20), fill="lightgrey")

        self.update_profile_button(button, image, size)

    def update_profile_button(self, button, image, size):
        #pang-update sa button ug naay mabag-o
        cropped_image = self.crop_to_circle(image, size)
        photo = ImageTk.PhotoImage(cropped_image)
        button.config(image=photo)
        button.image = photo  

    def crop_to_circle(self,image, size):
        #i-crop ang image to a circle
        image = image.resize(size, Image.Resampling.LANCZOS)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        result = ImageOps.fit(image, size, centering=(0.5, 0.5))
        result.putalpha(mask)
        return result

    def get_current_user_data(self):
        with open("database.json", "r") as file:
            database = json.load(file)
        
        users = database.get("users", [])
        
        for user in users:
            if user["username"] == self.username_inseller:
                return user  
        
        raise ValueError("User not found in the database.")