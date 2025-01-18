import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import time
from tkinter import TclError
from PIL import Image, ImageTk
import json
import os
import tkinter.messagebox as messagebox
'''
different imports ni sya nga okay ra gud isahon ang uban 
pero i need this to be like this para lang timailhan sa code nako
'''

'''
tanan mga nakabutang dri:
1. about sa HomePage Panel sa sidebar Menu sa Home Panel
2. ang mismong pilianan ug products sa buyers
3. pwede mag-search ug products
4. ang products kay naka-sort into categories, depende sa gibutang ni seller nga categories
5. pagpislit sa product kay naay product details na mupakita
    *maximum of 3 images sa product
    *name sa product
    *price with discount na dapat ang program na ang mag-compute (discount, depende sa gibutang ni seller)
    *variations: sizes, colors (depende sa gibutang ni seller)
    *quantity spinner ug pila imoha kabuok
    *add to cart button
    *name sa seller
'''

mainColor = "#d1101a"
DATA_FILE = "data.json"
msyulfont = 'Microsoft YaHei UI Light'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"users": {}, "products": [], "orders": []} 
    #if wla ni nag-exist nga structure, mag-return ug ani nga structure kay ing-anion mn ang database dapat

class homePage_Window:
    def __init__ (self, mainFrame, username):
        self.homePageFrame = tk.Frame(mainFrame)

        self.username = username

        self.create_header()
        self.create_left_sideBar()
        self.data = load_data()
        self.products = self.data["products"]

        for product in self.products:
            print(product["name"], product["price"])

        #default page na mupakita kay kumbaga, ang "home" is ang all categories
        self.switch_Page(
            page=self.home_Panel
        )

        self.homePageFrame.pack(fill=tk.BOTH, expand=True)

    #gui sa header
    def create_header(self):
        header_frame = tk.Frame(self.homePageFrame, bg=mainColor, height=60)
        header_frame.pack(side="top", fill="x")

        homeTopBtn = tk.Button(
            header_frame,
            text="HOME",
            font=(msyulfont, 20,'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            activebackground=mainColor,
            cursor="hand2",
            command=lambda: self.switch_Page(self.home_Panel))
        homeTopBtn.place(x=220)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            header_frame,
            textvariable=self.search_var,
            width=40,
            fg='black',
            font=(msyulfont, 14))
        self.search_entry.pack(side="right", padx=40, pady=10)
        self.search_entry.insert(0, "🔍Search for Products...")
        self.search_entry.bind('<FocusIn>', self.on_enter_search)
        self.search_entry.bind('<FocusOut>', self.on_leave_search)
        self.search_entry.bind("<Return>", self.perform_search) #dapat i-press pa ni user ang enter para mu-proceed ug search

    #placeholders sa search
    def on_enter_search(self, event):
        if self.search_entry.get() == "🔍Search for Products...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def on_leave_search(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "🔍Search for Products...")
            self.search_entry.config(fg="black")

    #tanan buttons sa categories
    def create_left_sideBar(self):
        left_sidebar = tk.Frame(self.homePageFrame, bg=mainColor)
        left_sidebar.pack(side='left', fill='y')
        left_sidebar.pack_propagate(False)
        left_sidebar.configure(width=220, height=400)

        categoriesLbl = tk.Label(
            left_sidebar, 
            text="Categories", 
            font=(msyulfont, 17, 'bold'),
            bg=mainColor,
            fg='#fff')
        categoriesLbl.place(x=55, y=40)

        womenBtn = tk.Button(
            left_sidebar,
            text="Women",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.womenPanel, self.womenOrders))
        womenBtn.place(x=60, y=80)

        menBtn = tk.Button(
            left_sidebar,
            text="Men",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.menPanel, self.menOrders))

        menBtn.place(x=60, y=115)

        kidsBtn = tk.Button(
            left_sidebar,
            text="Kids",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.kidsPanel, self.kidsOrders))
        kidsBtn.place(x=60, y=150)

        topsBtn = tk.Button(
            left_sidebar,
            text="Top",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.topsPanel, self.topOrders))
        topsBtn.place(x=60, y=230)

        bottomBtn = tk.Button(
            left_sidebar,
            text="Bottom",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.bottomPanel, self.bottomOrders))
        bottomBtn.place(x=60, y=265)

        dressBtn = tk.Button(
            left_sidebar,
            text="Dress",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.dressPanel, self.dressOrders))
        dressBtn.place(x=60, y=300)

        accessoriesBtn = tk.Button(
            left_sidebar,
            text="Accessories",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.accessoriesPanel, self.accessoriesOrders))
        accessoriesBtn.place(x=60, y=335)

        footwearBtn = tk.Button(
            left_sidebar,
            text="Footwear",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.footwearPanel, self.footwearOrders))
        footwearBtn.place(x=60, y=370)

        bagsBtn = tk.Button(
            left_sidebar,
            text="Bags",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.bagsPanel, self.bagsOrders))
        bagsBtn.place(x=60, y=405)

        beachwearBtn = tk.Button(
            left_sidebar,
            text="Beachwear",
            font=(msyulfont, 17, 'bold'),
            fg='#fff',
            bg=mainColor,
            bd=0,
            cursor="hand2",
            activebackground=mainColor,
            command=lambda: self.switch_Page(self.beachwearPanel, self.beachwearOrders))
        beachwearBtn.place(x=60, y=444)

        self.mainPageFrame = tk.Frame(
            self.homePageFrame)
        self.mainPageFrame.pack_propagate(False)
        self.mainPageFrame.configure(height=700)
        self.mainPageFrame.pack(fill='x', padx=5, pady=5)
        
        self.products = self.create_products()

    #prepare scrollbar frame para sa tanan pages
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
    
    #para ma-scroll gamit ang mousewheel
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

#===================ALL CATEGORY PAGES================
    def home_Panel(self, mainOptionFrameAP):
        middle_panel = tk.Frame(mainOptionFrameAP)
        middle_panel.pack(fill="both", expand=True)

        #naay sariling scrollbar frame ang HOME
        canvas = tk.Canvas(middle_panel)
        scrollbar = tk.Scrollbar(middle_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta / 120), "units"))

        #===================IMAGE CAROUSEL SECTION===================
        adsFrame = tk.Frame(scrollable_frame, height=100)
        adsFrame.pack(fill="x", padx=5, pady=5)

        self.forCarousel = tk.Frame(adsFrame, height=100)
        self.forCarousel.pack(side="left", padx=5, pady=5)
        carousel = self.image_carousel()

        self.image = tk.PhotoImage(file="C:/Users/USER/Documents/Python/CKC Styles/images/sampleCar4.png")
        self.image_label = tk.Label(
            adsFrame, 
            image=self.image, 
            bg="white"
        )
        self.image_label.pack(side="left", padx=1)

        self.next_button.bind("<Button-1>", lambda e: self.slide_image(1))
        self.prev_button.bind("<Button-1>", lambda e: self.slide_image(-1))

        #===================PRODCUTS SECTION===================
        self.productsFrame = tk.Frame(scrollable_frame, height=500)
        self.productsFrame.pack(fill="both", padx=5, pady=5)

        self.current_category_orders = self.all_orders

        self.add_products(self.productsFrame, self.current_category_orders)

    def womenPanel(self, mainOptionFrameAP):
        womenFrame = tk.Frame(mainOptionFrameAP)
        womenFrame.pack_propagate(False)
        womenFrame.configure(height=700)
        womenFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(womenFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Women's Clothing", 
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500)
        self.productsFrame.pack(fill="both", padx=5, pady=5)
        
        self.current_category_orders = self.womenOrders

        self.add_products(self.productsFrame, self.current_category_orders)

    def menPanel(self, mainOptionFrameAP):
        menFrame = tk.Frame(mainOptionFrameAP)
        menFrame.pack_propagate(False)
        menFrame.configure(height=700)
        menFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(menFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Men's Clothing", 
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500)
        self.productsFrame.pack(fill="both", padx=5, pady=5)

        self.current_category_orders = self.menOrders

        self.add_products(self.productsFrame, self.current_category_orders)

    def kidsPanel(self, mainOptionFrameAP):
        kidsFrame = tk.Frame(mainOptionFrameAP)
        kidsFrame.pack_propagate(False)
        kidsFrame.configure(height=700)
        kidsFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(kidsFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Kids' Clothing", 
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500)
        self.productsFrame.pack(fill="both", padx=5, pady=5)
        
        self.current_category_orders = self.kidsOrders

        self.add_products(self.productsFrame, self.current_category_orders)

    def topsPanel(self, mainOptionFrameAP):
        topsFrame = tk.Frame(mainOptionFrameAP)
        topsFrame.pack_propagate(False)
        topsFrame.configure(height=700)
        topsFrame.pack(fill='x')
        
        scrollable_frame = self.create_scrollable_frame(topsFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Tops", 
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500 )
        self.productsFrame.pack(fill="both", padx=5, pady=5)

        self.current_category_orders = self.topOrders

        self.add_products(self.productsFrame, self.current_category_orders)

    def bottomPanel(self, mainOptionFrameAP):
        bottomFrame = tk.Frame(mainOptionFrameAP)
        bottomFrame.pack_propagate(False)
        bottomFrame.configure(height=700)
        bottomFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(bottomFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Bottoms",             
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500 )
        self.productsFrame.pack(fill="both", padx=5, pady=5)

        self.current_category_orders = self.bottomOrders

        self.add_products(self.productsFrame, self.current_category_orders)

    def dressPanel(self, mainOptionFrameAP):
        dressFrame = tk.Frame(mainOptionFrameAP)
        dressFrame.pack_propagate(False)
        dressFrame.configure(height=700)
        dressFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(dressFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Dresses", 
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500 )
        self.productsFrame.pack(fill="both", padx=5, pady=5)

        self.current_category_orders = self.dressOrders

        self.add_products(self.productsFrame, self.current_category_orders)

    def accessoriesPanel(self, mainOptionFrameAP):
        accessoriesFrame = tk.Frame(mainOptionFrameAP)
        accessoriesFrame.pack_propagate(False)
        accessoriesFrame.configure(height=700)
        accessoriesFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(accessoriesFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Accessories", 
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500 )
        self.productsFrame.pack(fill="both", padx=5, pady=5)
        
        self.current_category_orders = self.accessoriesOrders

        self.add_products(self.productsFrame, self.current_category_orders)

    def footwearPanel(self, mainOptionFrameAP):
        footwearFrame = tk.Frame(mainOptionFrameAP)
        footwearFrame.pack_propagate(False)
        footwearFrame.configure(height=700)
        footwearFrame.pack(fill='x')
        
        scrollable_frame = self.create_scrollable_frame(footwearFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Footwear",             
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500 )
        self.productsFrame.pack(fill="both", padx=5, pady=5)

        self.current_category_orders = self.footwearOrders

        self.add_products(self.productsFrame, self.current_category_orders)

    def bagsPanel(self, mainOptionFrameAP):
        bagsFrame = tk.Frame(mainOptionFrameAP)
        bagsFrame.pack_propagate(False)
        bagsFrame.configure(height=700)
        bagsFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(bagsFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Bags",             
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500 )
        self.productsFrame.pack(fill="both", padx=5, pady=5)
        
        self.current_category_orders = self.bagsOrders

        self.add_products(self.productsFrame, self.current_category_orders)

    def beachwearPanel(self, mainOptionFrameAP):
        beachwearFrame = tk.Frame(mainOptionFrameAP)
        beachwearFrame.pack_propagate(False)
        beachwearFrame.configure(height=700)
        beachwearFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(beachwearFrame)

        frameLbls = tk.Frame(scrollable_frame)
        frameLbls.pack(fill='x')

        lbl1 = tk.Label(
            frameLbls, 
            text="Beachwear",             
            font=(msyulfont, 20, 'bold'))
        lbl1.pack(side='left', padx=5)

        self.productsFrame = tk.Frame(scrollable_frame, height=500 )
        self.productsFrame.pack(fill="both", padx=5, pady=5)
        
        self.current_category_orders = self.beachwearOrders

        self.add_products(self.productsFrame, self.current_category_orders)

#===================FOR BACK SA PRODUCTS===================
    def create_products(self):
        '''
        the logic aron dali ang pa-separate sa products nga naka-category:
        1. maghimog list nga category-specific
        2. i-load ang mga products nga gikan sa database.json nga gipang-add sa sellers
        3. for loop nga if ang ang product is na-check niya nga naay ani nga category, i-append niya sa list
        4. for loop kay pwede sa isa ka product kay daghan ug category
        5. i-deliver ang list sa ilahang sari sariling pages or frames

        '''
        #Initialize category-specific lists
        self.all_orders = []
        self.womenOrders = []
        self.menOrders = []
        self.kidsOrders = []
        self.topOrders = []
        self.bottomOrders = []
        self.dressOrders = []
        self.accessoriesOrders = []
        self.footwearOrders = []
        self.bagsOrders = []
        self.beachwearOrders = []

        db_path = 'database.json'

        #for making sure lang nga dapat naa ni nga structure sa database
        if not os.path.exists(db_path): 
            default_data = {
                "users": [],
                "products": [],
                "orders": []
            }
            try:
                with open(db_path, 'w') as file:
                    json.dump(default_data, file, indent=4)
                print(f"{db_path} has been created with default structure.")
            except Exception as e:
                print(f"Error creating {db_path}: {e}")
                return []

        #Load products from the database
        try:
            with open(db_path, 'r') as file:
                data = json.load(file)
                self.products = data.get("products", [])
        except FileNotFoundError:
            print(f"Error: {db_path} file not found.")
            self.products = []
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {db_path}.")
            self.products = []

        # Categorize products
        for product in self.products:
            self.all_orders.append(product)  #para tanan products regardless sa category kay ma-sure nga ma-add sa all or HOME
            for category in product.get('categories', []):
                category = category.lower()  #i-lower para dli case sensitive
                if category == "women":
                    self.womenOrders.append(product)
                elif category == "men":
                    self.menOrders.append(product)
                elif category == "kids":
                    self.kidsOrders.append(product)
                elif category == "top":
                    self.topOrders.append(product)
                elif category == "bottom":
                    self.bottomOrders.append(product)
                elif category == "dress":
                    self.dressOrders.append(product)
                elif category == "accessories":
                    self.accessoriesOrders.append(product)
                elif category == "footwear":
                    self.footwearOrders.append(product)
                elif category == "bags":
                    self.bagsOrders.append(product)
                elif category == "beachwear":
                    self.beachwearOrders.append(product)

        return self.products

    def add_products(self, page, category_orders):
        '''
        pang-add ug product sa screen with complete with gui:
        1. image
        2. product name
        3. price (if naay discount, display discounted price)
        4. ang mismong discount in percentage (if wlay discount gibutang si seller (0.0), wlay mupakita)
        '''
        for widget in page.winfo_children():
            widget.destroy()

        #ug wlay products ana nga category, mupakita ang message
        if not category_orders:
            message_label = tk.Label(
                page,
                text="No products available yet!",
                font=("msyulfont", 16),
                fg="black"
            )
            message_label.pack(pady=200, padx=370)
        else:
            #display products in a grid layout aron naka-column and rows
            col_count = 5
            row_count = 0
            frame_width = 180
            frame_height = 250

            for i, product in enumerate(category_orders):
                product_frame = tk.Frame(
                    page,
                    borderwidth=1,
                    relief="solid",
                    padx=10,
                    pady=10,
                    width=frame_width,
                    height=frame_height
                )
                product_frame.grid(row=row_count, column=i % col_count, padx=10, pady=5)

                image_path = product.get("image", [None])[0]  #Get the first image, or None if no images
                if image_path:  #Ensure the path is not empty
                    try:
                        image = Image.open(image_path)
                        image = image.resize((150, 150), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)

                        img_label = tk.Label(product_frame, image=photo, width=150, height=150)
                        img_label.image = photo  
                        img_label.pack(pady=5)
                    except (FileNotFoundError, OSError):
                        #Handle missing or invalid image path
                        print(f"Error: Could not load image at path {image_path}")
                        img_label = tk.Label(product_frame, text="[Image Error]", width=15, height=8, bg="lightgray")
                        img_label.pack(pady=5)
                else:
                    img_label = tk.Label(product_frame, text="[Image Here]", width=15, height=8, bg="lightgray")
                    img_label.pack(pady=5)
                    
                #Product name (clickable)
                name_label = tk.Label(
                    product_frame,
                    text=product["name"],
                    font=("Helvetica", 12, "bold"),
                    fg=mainColor,
                    cursor="hand2",
                    wraplength=frame_width - 20
                )
                name_label.pack(pady=2)
                name_label.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))

                #Product price
                price_text = f"₱{product['price']:.2f}"
                if product.get("voucher"):
                    discounted_price = product['price'] - (product['price'] * product['voucher'] / 100)
                    price_text = f"₱{product['price']:.2f} → ₱{discounted_price:.2f}"
                price_label = tk.Label(product_frame, text=f"Price: {price_text}", font=("Helvetica", 10))
                price_label.pack(pady=2)

                #Discount (optional)
                if product.get("voucher"):
                    discount_label = tk.Label(product_frame, text=f"Discount: {product['voucher']}%", font=("Helvetica", 9, "italic"), fg="green")
                    discount_label.pack(pady=2)
                else:
                    discount_label = tk.Label(product_frame, text="", font=("Helvetica", 9, "italic"))
                    discount_label.pack(pady=2)

                #Rating
                rating_label = tk.Label(product_frame, text=f"Rating: {product['rating']}/5", font=("Helvetica", 10))
                rating_label.pack(pady=2)

                #Sold count
                sold_label = tk.Label(product_frame, text=f"Sold: {product['sold']}", font=("Helvetica", 10))
                sold_label.pack(pady=2)

                #Increment row after reaching the column limit
                if (i + 1) % col_count == 0:
                    row_count += 1

    #pag pisliton ang name sa product, mupakita ni
    def show_product_details(self, product):
        #hawaon ang naa sa product frame para kani sila ang iilis
        for widget in self.productsFrame.winfo_children():
            widget.destroy()

        #sudlanan sa tanan
        detail_container = tk.Frame(self.productsFrame)
        detail_container.pack(fill="both", expand=True)

        #back btn
        back_button = tk.Button(
            detail_container, 
            text=">", 
            bd=0,
            fg='white',
            bg=mainColor,
            font=('Arial', 20, 'bold'),
            command=self.back_to_main)
        back_button.pack(side="top", anchor='nw', pady=10, padx=30)

        if "image" in product:  #Ensure that the product has an "image" key
            # Load the first image
            try:
                image_path = product["image"][0]  #Start with the first image
                image = Image.open(image_path)
                image = image.resize((450, 500), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                #Create an image label and set the initial image
                img_label = tk.Label(detail_container, image=photo, width=450, height=500)
                img_label.image = photo  
                img_label.current_image_index = 0  
                img_label.pack(side="left", padx=40, pady=20)
            except (FileNotFoundError, OSError):
                #Handle missing or invalid image path
                print(f"Error: Could not load image at path {product['image'][0]}")
                img_label = tk.Label(detail_container, text="[Image Error]", width=15, height=8, bg="lightgray")
                img_label.pack(side="left", padx=40, pady=20)

            #Add navigation buttons
            button_frame = tk.Frame(detail_container)
            button_frame.pack(side="left", padx=10)

            previous_button = tk.Button(
                button_frame, 
                text="<", 
                bd=0,
                fg='white',
                bg=mainColor,
                font=('Arial', 20, 'bold'),
                command=lambda: self.show_previous_image(product, img_label))
            previous_button.pack(side="left", pady=5, padx=5)

            next_button = tk.Button(
                button_frame, 
                text=">", 
                bd=0,
                fg='white',
                bg=mainColor,
                font=('Arial', 20, 'bold'),
                command=lambda: self.show_next_image(product, img_label))
            next_button.pack(side="right", pady=5, padx=5)

        else:
            #for missing "image" key
            img_label = tk.Label(detail_container, text="[Image Here]", width=15, height=8, bg="lightgray")
            img_label.pack(side="left", padx=40, pady=20)

        #details sa right
        detail_frame = tk.Frame(detail_container)
        detail_frame.pack(side="right", fill="y", padx=100, pady=20)

        name_label = tk.Label(
            detail_frame, 
            text=product["name"], 
            font=(msyulfont, 20, "bold"))
        name_label.pack(anchor="w", pady=5)

        #COMMENTED, NOT IMPLEMENTED, FOR FUTURE PURPOSES
        '''rating_label = tk.Label(
            detail_frame, 
            text=f"Rating: {product['rating']}/5 | {product['sold']} sold",
            font=('Helvetica', 14, "bold"))
        rating_label.pack(anchor="w", pady=5)'''

        price_text = f"₱{product['price']}"
        if product.get("voucher"):
            #price_text = f"₱{product['price']} (₱{product['price'] - (product['price'] * product['voucher'] / 100):.2f} after discount)"
            price_text = f"₱{product['price']} → (₱{product['price'] - (product['price'] * product['voucher'] / 100):.2f})"

        price_label = tk.Label(
            detail_frame, 
            text=price_text, 
            font=("Helvetica", 20), fg="red")
        price_label.pack(anchor="w", pady=5)

        quantity_frame = tk.Frame(detail_frame)
        quantity_frame.pack(anchor="w", pady=5)
        
        def update_stock_label(selected_color, selected_size, stock_info, stock_label, quantity_spinner):
            '''
            Naka depende ni sya ug pila ka-stock ang gibutang ni seller
            naa ni sya kay different colors have different sizes, and naa sad silay different stocks
            ex: 
            colors: Pink, Blue
            Sizes: Small, Medium
            stock logic:
                Pink- Small: 10 stocks
                Pink- Medium: 20 stocks
                Blue- Small: 30 stocks
                Blue- Medium: 40 stocks
            '''
            stock = stock_info.get(selected_color, {}).get(selected_size, 0)
            stock_label.config(text=f"Available: {stock}")

            quantity_spinner.config(to=stock)

        stock_info = product["stock_info"]

        #frame to hold the dropdowns and labels
        variation_frame = tk.Frame(quantity_frame)
        variation_frame.pack(side="top", pady=10)

        #label and dropdown for Colors
        color_label = tk.Label(variation_frame, text="Colors:", font=("Helvetica", 10, "bold"))
        color_label.grid(row=0, column=0, sticky="w", pady=5)

        selected_color = tk.StringVar()
        color_dropdown = tk.OptionMenu(
            variation_frame, 
            selected_color, 
            *product["colors"], 
            command=lambda color: update_stock_label(color, selected_size.get(), stock_info, stock_label, quantity_spinner)
        )
        color_dropdown.grid(row=0, column=1, sticky="w", padx=5)

        #label and dropdown for Sizes
        size_label = tk.Label(variation_frame, text="Sizes:", font=("Helvetica", 10, "bold"))
        size_label.grid(row=1, column=0, sticky="w", pady=5)

        selected_size = tk.StringVar()
        size_dropdown = tk.OptionMenu(
            variation_frame, 
            selected_size, 
            *product["sizes"], 
            command=lambda size: update_stock_label(selected_color.get(), size, stock_info, stock_label, quantity_spinner)
        )
        size_dropdown.grid(row=1, column=1, sticky="w", padx=5)

        #label for stock availability
        stock_label = tk.Label(variation_frame, text="Available: N/A", font=("Helvetica", 10))
        stock_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=10)
        
        quantity_label = tk.Label(variation_frame, text="Quantity:", font=("Helvetica", 10, "bold"))
        quantity_label.grid(row=3, column=0, sticky="w", pady=5)

        quantity_spinner = tk.Spinbox(variation_frame, from_=1, to=1, width=5)
        quantity_spinner.grid(row=3, column=1, sticky="w", padx=5)

        #Initialize with the first color and size
        selected_color.set(product["colors"][0])
        selected_size.set(product["sizes"][0])
        update_stock_label(selected_color.get(), selected_size.get(), stock_info, stock_label, quantity_spinner)

        addToCartBtn = tk.Button(
            detail_frame, 
            text="Add to Cart", 
            bg=mainColor,
            bd=0, 
            fg="white",
            font=("Arial", 16, "bold"),
            width=20, 
            height=2,
            command=lambda: self.add_to_cart(product, selected_color.get(), selected_size.get(), int(quantity_spinner.get()))) 
        addToCartBtn.pack(pady=10)

        storeSellerFrame = tk.Frame(
            self.productsFrame)
        storeSellerFrame.pack(side='bottom', anchor='s', fill='x', pady=10)

        seller_name = product["shop_name"] if product.get("shop_name") else "Unknown Seller"

        store_label = tk.Label(
            storeSellerFrame, 
            text=f"Store: {seller_name}",  #seller's name here
            font=(msyulfont, 30, "bold"))
        store_label.pack(anchor="w", pady=10)

        #COMMENTED, NOT IMPLEMENTED
        #THIS IS SUPPOSED TO BE THE REVIEWS AND RATINGS SA BUYERS ANA NGA PRODUCT
        '''reviewFrame = tk.Frame(storeSellerFrame)
        reviewFrame.pack(side='bottom', fill='x', pady=10)

        review_label = tk.Label(
            reviewFrame, 
            text="Reviews & Ratings:", 
            font=(msyulfont, 20, "bold"))
        review_label.pack(anchor="w", pady=5)

        review_canvas = tk.Canvas(
            reviewFrame, 
            height=200, 
            width=1000)
        review_scrollbar = ttk.Scrollbar(
            reviewFrame, 
            orient="vertical", 
            command=review_canvas.yview)
        
        review_list_frame = tk.Frame(review_canvas)
        review_list_frame.bind(
            "<Configure>",
            lambda e: review_canvas.configure(scrollregion=review_canvas.bbox("all")),
        )

        review_canvas.create_window((0, 0), window=review_list_frame, anchor="nw")
        review_canvas.configure(yscrollcommand=review_scrollbar.set)

        review_canvas.pack(side="left", fill="y", expand=True)
        review_scrollbar.pack(side="right", fill="y")

        reviews = product.get("reviews", [])
        for i, review in enumerate(reviews):
            buyer_label = tk.Label(
                review_list_frame, 
                text=f"Buyer: {review['buyer']}", 
                font=("Helvetica", 15, "bold"))
            buyer_label.grid(row=i * 4, column=0, sticky="w", pady=2)

            rating_label = tk.Label(
                review_list_frame, 
                text=f"Rating: {review['rating']} stars",
                font=("Helvetica", 14))
            rating_label.grid(row=i * 4 + 1, column=0, sticky="w", pady=2)

            meta_label = tk.Label(
                review_list_frame,
                text=f"({review['date']}) | Variation: {review['variation']}",
                font=("Helvetica", 14, "italic"),
            )
            meta_label.grid(row=i * 4 + 2, column=0, sticky="w", pady=2)

            comment_label = tk.Label(
                review_list_frame, 
                text=f"Comment: {review['comment']}", 
                wraplength=500,
                font=("Helvetica", 12))
            comment_label.grid(row=i * 4 + 3, column=0, sticky="w", pady=5)'''

    def add_to_cart(self, product, selected_color, selected_size, quantity):
        # Get the current user's username (make sure to retrieve the logged-in user's username)
        current_username = self.username  # Assuming you have a variable that holds the current logged-in user

        # Get the user data from the database
        db_path = "database.json"
        try:
            with open(db_path, "r") as db_file:
                data = json.load(db_file)

            # Find the user with the current username
            user = next((user for user in data["users"] if user["username"] == current_username), None)

            if not user:
                messagebox.showerror("Error", "User not found!")
                return

            # Get the product's first image (ensure the product has images)
            first_image = product["image"][0] if product.get("image") else None

            # Calculate the discounted price
            discount = product.get("voucher", 0)  # Default to 0 if no voucher
            discounted_price = product["price"] * (1 - discount / 100)

            # Create a cart item with the product details, selected color, size, quantity, and shop name
            cart_item = {
                "product_name": product["name"],  # Product name
                "color": selected_color,          # Selected color
                "size": selected_size,            # Selected size
                "price": product["price"],        # Original price
                "discount": discount,             # Voucher/Discount
                "discounted_price": discounted_price,  # Price after discount
                "quantity": quantity,             # Quantity selected
                "total_price": discounted_price * quantity,  # Total price after discount
                "image": first_image,             # First image of the product
                "shop_name": product["shop_name"],   # Shop name (from the seller's info)
                "purchasedBy": "" # List to store purchase history
            }

            # Add the item to the user's cart
            user["cart"].append(cart_item)

            # Save the updated data back to the database
            with open(db_path, "w") as db_file:
                json.dump(data, db_file, indent=4)

            messagebox.showinfo("Success", f"Added {quantity} {product['name']} to your cart!")

        except FileNotFoundError:
            messagebox.showerror("Error", "Database file not found!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Database file is corrupted!")

#===================OTHERS===================
    #para sa 3 pictures sa product details frame
    def show_next_image(self, product, img_label):
        current_image_index = getattr(img_label, "current_image_index", 0)
        next_image_index = (current_image_index + 1) % len(product["image"])

        image_path = product["image"][next_image_index]
        image = Image.open(image_path)
        image = image.resize((450, 500), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        img_label.config(image=photo)
        img_label.image = photo  
        img_label.current_image_index = next_image_index 

    def show_previous_image(self, product, img_label):
        current_image_index = getattr(img_label, "current_image_index", 0)
        previous_image_index = (current_image_index - 1) % len(product["image"])

        image_path = product["image"][previous_image_index]
        image = Image.open(image_path)
        image = image.resize((450, 500), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        img_label.config(image=photo)
        img_label.image = photo  
        img_label.current_image_index = previous_image_index  
    
    #===================SWITCHING PAGE LOGICS===================
    def switch_to_category(self, category_orders):
        self.current_category_orders = category_orders
        self.add_products(self.productsFrame, self.current_category_orders)

    def switch_Page(self, page, filter_products=None):
        self.delete_Page()
        if filter_products:  
            self.products = filter_products
        else:
            self.products = self.all_orders  
        page(self.mainPageFrame)
    
    def delete_Page(self):
        '''
        aron dli magsapaw ang mga frames, 
        i-delete ang previous frame if magpislit ug button nga mag-create ug new frame para sya na pud ang magdisplay
        '''
        for frame in self.mainPageFrame.winfo_children():
            frame.destroy()

    def back_to_main(self):
        """
        Return to the main product view by clearing product details and displaying products
        """
        for widget in self.productsFrame.winfo_children():
            widget.destroy()

        self.add_products(self.productsFrame, self.current_category_orders)

    def perform_search(self, event=None):
        """
        Handle search confirmation on pressing Enter.
        Filters products by search term and updates the display.
        """
        search_term = self.search_var.get().strip().lower()

        if not self.current_category_orders:
            return

        filtered_products = [
            product for product in self.current_category_orders
            if search_term in product["name"].lower()
        ]

        self.add_products(self.productsFrame, filtered_products)

#===================IMAGE CAROUSEL LOGIC===================
    #katong mga pictures nga ads sa taas sa 
    def image_carousel(self):
        image_paths = [
            "C:/Users/USER/Documents/Python/CKC Styles/images/sampleCar1.png", 
            "C:/Users/USER/Documents/Python/CKC Styles/images/sampleCar2.png",
            "C:/Users/USER/Documents/Python/CKC Styles/images/sampleCar3.png"
        ]
        self.images = [PhotoImage(file=img) for img in image_paths]

        self.current_index = 0

        self.canvas = tk.Canvas(self.forCarousel, width=720, height=200, highlightthickness=0)
        self.canvas.pack()

        self.current_image = self.canvas.create_image(350, 100, image=self.images[self.current_index])

        #Frame for buttons and dots
        control_frame = tk.Frame(self.forCarousel)
        control_frame.pack(pady=0)

        #Previous button
        self.prev_button = tk.Button(
            control_frame, 
            text="<", 
            font=("Arial", 16),
            bd=0,
            command=lambda: self.slide_image(-1), 
            fg="black"
        )
        self.prev_button.pack(side=tk.LEFT, padx=10)

        #Dots (middle of buttons)
        self.dots = []
        self.dot_frame = tk.Frame(control_frame)
        self.dot_frame.pack(side=tk.LEFT)

        self.create_dots()

        #Next button
        self.next_button = tk.Button(
            control_frame, 
            text=">", 
            font=("Arial", 16), 
            command=lambda: self.slide_image(1),
            fg="black",
            bd=0
        )
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.auto_slide_delay = 3000  
        self.last_activity_time = time.time()
        self.start_auto_slide()

        return self

    def create_dots(self):
        for i in range(len(self.images)):
            dot = tk.Label(self.dot_frame, text="●", font=("Arial", 14), fg="gray")
            dot.grid(row=0, column=i, padx=5)
            self.dots.append(dot)
        self.update_dots()

    def update_dots(self):
        for i, dot in enumerate(self.dots):
            if i == self.current_index:
                dot.config(fg="black")  
            else:
                dot.config(fg="gray")   

    def slide_image(self, direction):
        if not self.canvas.winfo_exists():
            print("Canvas does not exist!")
            return

        outgoing_image = self.current_image  
        self.current_index = (self.current_index + direction) % len(self.images)
        next_image = self.images[self.current_index]

        x_start = 720 if direction == 1 else -720
        x_end = 350
        x_out_start = 350
        x_out_end = -720 if direction == 1 else 720

        try:
            incoming_image = self.canvas.create_image(x_start, 100, image=next_image)

            steps = 30  
            for step in range(steps):
                delta_x_in = (x_end - x_start) / steps
                delta_x_out = (x_out_end - x_out_start) / steps

                self.canvas.move(incoming_image, delta_x_in, 0)  
                self.canvas.move(outgoing_image, delta_x_out, 0)  
                self.canvas.update()
                self.canvas.after(5)  

            self.canvas.coords(incoming_image, 350, 100)
            self.canvas.delete(outgoing_image)
            self.current_image = incoming_image

            self.update_dots()

        except TclError as e:
            print(f"Canvas error: {e}")

    def next_image(self, event=None):
        self.slide_image(1)

    def prev_image(self, event=None):
        self.slide_image(-1)

    def start_auto_slide(self):
        if time.time() - self.last_activity_time > self.auto_slide_delay / 500:
            self.next_image()
        self.forCarousel.after(self.auto_slide_delay, self.start_auto_slide)