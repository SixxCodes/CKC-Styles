import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

'''
tanan mga nakabutang dri:
1. about sa Cart Panel sa sidebar Menu sa Home Panel
2. maka-search ug products sa cart
2. tapok ang products sa isa ka store
3. naa dri ang place order sad 
(pero ang confirmed or placed na nga orders, naa sa order panel na)
'''

mainColor = "#d1101a" #maincolor
msyulfont = 'Microsoft YaHei UI Light' #main font

class myCart_Window:
    def __init__ (self, mainFrame, username):
        self.myCartPageFrame = tk.Frame(mainFrame)
        
        self.currentUser = username

        #storage sa items sa cart
        self.cart_items = {}
        self.product_widgets = []

        self.create_header()
        self.top_Content()
        self.product_header()
        self.scrollable_frame()
        self.read_from_cart(self.currentUser)
        #self.create_order() #commented, back up code
        self.bottom_Content()
        
        self.myCartPageFrame.pack(fill=tk.BOTH, expand=True)

#===================HEADERS GUI===================
    def create_header(self):
        header_frame = tk.Frame(self.myCartPageFrame, bg=mainColor, height=60)
        header_frame.pack(side="top", fill="x")

    def top_Content(self):
        myOrderLabel = tk.Label(
            self.myCartPageFrame,
            text="My Cart",
            fg='black',
            font=(msyulfont, 23, 'bold'))
        myOrderLabel.place(x=70, y=80)

        search_frame = tk.Frame(self.myCartPageFrame)
        search_frame.pack(anchor='ne', padx=10, pady=20)

        searchLbl = tk.Label(  # Search Label
            search_frame,
            text="🔍Search Products:",
            font=(msyulfont, 16))
        searchLbl.pack(side="left", padx=1, pady=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            width=40,
            bd=3,
            fg='black',
            textvariable=self.search_var, 
            font=(msyulfont, 14))
        self.search_entry.pack(side="right", padx=40, pady=10)
        self.myCartPageFrame.after(100, self.search_entry.focus)  #naka-focus na daan sa search entry
        self.search_entry.bind('<FocusIn>') #while gapindot kag letter, mag-search na sya, dli kay mag-press enter pa

        self.search_var.trace_add("write", self.filter_products)

    #labels lang
    def product_header(self):
        self.optionsFrame = tk.Frame(self.myCartPageFrame)
        self.optionsFrame.pack_propagate(False)
        self.optionsFrame.configure(width=500, height=50)
        self.optionsFrame.pack(fill='x')

        productLbl = tk.Label(
            self.optionsFrame,
            text="Product",
            fg=mainColor,
            font=(msyulfont, 16, 'bold'))
        productLbl.place(x=120, y=10)

        unitPriceLbl = tk.Label(
            self.optionsFrame,
            text="Unit Price",
            fg=mainColor,
            font=(msyulfont, 16, 'bold'))
        unitPriceLbl.place(x=550, y=10)

        quantityLbl = tk.Label(
            self.optionsFrame,
            text="Quantity",
            fg=mainColor,
            font=(msyulfont, 16, 'bold'))
        quantityLbl.place(x=800, y=10)

        totalPriceLbl = tk.Label(
            self.optionsFrame,
            text="Total Price",
            fg=mainColor,
            font=(msyulfont, 16, 'bold'))
        totalPriceLbl.place(x=1000, y=10)

        actionsLbl = tk.Label(
            self.optionsFrame,
            text="Actions",
            fg=mainColor,
            font=(msyulfont, 16, 'bold'))
        actionsLbl.place(x=1200, y=10)

        tk.Frame(
            self.optionsFrame, 
            width=1500, 
            height=1, 
            bg='black').place(x=0, y=49)

    #frame para pwede i-scroll ang frame
    def scrollable_frame(self):
        frame = tk.Frame(self.myCartPageFrame)
        frame.pack_propagate(False)
        frame.configure(height=455)
        frame.pack(fill='x')

        self.canvas = tk.Canvas(frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(self.canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.scrollable_frame = scrollable_frame

        return scrollable_frame

#===================BACK===================
    '''
    basahon niya ang mga products nga gi-add to cart ni user sa json
    para ma-display sya sa gui
    '''
    def read_from_cart(self, username):
        db_path = "database.json"
        try:
            with open(db_path, "r") as db_file:
                data = json.load(db_file)

            #pangitaon sa ang user aron makuha iyahang cart
            user = next((user for user in data["users"] if user["username"] == username), None)

            if not user:
                messagebox.showerror("Error", "User not found!")
                return

            #for loop para ma-check tanan naa sa cart
            for item in user["cart"]:
                store_name = item["shop_name"]
                product_name = item["product_name"]
                variation = f"Size: {item['size']}, Color: {item['color']}"
                price = item["price"]
                quantity = item["quantity"]
                image_path = item["image"]

                #ang image sa product with debugging print statement para mabaw-an if nag-error and para ma-catch lang
                if image_path:
                    try:
                        img = Image.open(image_path).resize((50, 50))
                        picture = ImageTk.PhotoImage(img)
                    except Exception as e:
                        picture = None
                        print(f"Error loading image: {e}")
                else:
                    picture = None

                if store_name not in self.cart_items:
                    store_frame = tk.Frame(self.scrollable_frame, bd=2, relief="ridge", padx=79, pady=10)
                    store_label = tk.Label(store_frame, text=f"Store: {store_name}", font=("Arial", 14))
                    store_label.pack(padx=10, pady=5)
                    store_frame.pack(fill="x", padx=10, pady=10)
                    self.cart_items[store_name] = {"frame": store_frame, "products": []}

                self.product = {
                    "store": store_name,
                    "name": product_name,
                    "variation": variation,
                    "price": price,
                    "quantity": quantity,
                    "selected_var": tk.IntVar(),  
                    "quantity_var": tk.IntVar(value=quantity),  
                }

                order_frame = tk.Frame(
                    self.cart_items[store_name]["frame"],
                    padx=10, 
                    pady=10)
                order_frame.pack(fill="x", padx=10, pady=5)

                checkbox = tk.Checkbutton(
                    order_frame, 
                    variable=self.product["selected_var"], 
                    command=self.update_total_price)
                checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="w")

                if picture:
                    pic_label = tk.Label(order_frame, image=picture)
                    pic_label.image = picture
                    pic_label.grid(row=0, column=1, padx=5, pady=5)
                else:
                    tk.Label(order_frame, text="No Image").grid(row=0, column=1, padx=5, pady=5)

                details_frame = tk.Frame(order_frame)
                details_frame.grid(row=0, column=2, padx=5, pady=5, sticky="w")

                tk.Label(
                    details_frame, 
                    text=f"Product: {product_name}", 
                    font=("Arial", 10)).pack(anchor="w")
                tk.Label(details_frame, text=f"Variation: {variation}", font=("Arial", 10)).pack(anchor="w")

                tk.Label(
                    order_frame, 
                    text=f"Price: ₱{price:.2f}", 
                    font=("Arial", 10)).grid(row=0, column=3, padx=150, pady=5)

                quantity_label = tk.Label(
                    order_frame, 
                    textvariable=self.product["quantity_var"]
                )
                quantity_label.grid(row=0, column=4, padx=30, pady=5)

                #COMMENTED, FOR FUTURE PURPOSES
                '''quantity_spinner = tk.Spinbox(
                    order_frame, 
                    from_=1, 
                    to=99, 
                    textvariable=product["quantity_var"], 
                    width=5, 
                    command=lambda p=self.product: self.update_total(order_frame, p))
                quantity_spinner.grid(row=0, column=4, padx=30, pady=5)'''

                total_price_label = tk.Label(
                    order_frame, 
                    text=f"Total: ₱{price * quantity:.2f}", 
                    font=("Arial", 10))
                total_price_label.grid(row=0, column=5, padx=120, pady=5)

                delete_button = tk.Button(
                    order_frame, 
                    text="Delete", 
                    command=lambda p=self.product: self.delete_item(order_frame, p))
                delete_button.grid(row=0, column=6, padx=5, pady=5)

                self.product.update({"frame": order_frame, "total_label": total_price_label})

                self.cart_items[store_name]["products"].append(self.product)
                self.product_widgets.append(order_frame)

        except FileNotFoundError:
            messagebox.showerror("Error", "Database file not found!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Database file is corrupted!")

    def update_total(self, order_frame, product):
        #update ang total base sa quantity spinner
        quantity = product["quantity_var"].get()
        total_price = product["price"] * quantity
        product["total_label"].config(text=f"Total: ₱{total_price:.2f}")
        
        #update apil ang grand total price (totalNumLbl)
        self.update_total_price()  

    def delete_item(self, order_frame, product):
        """
        Deletes the selected product from the cart, updates the GUI, and removes it from the database.
        """
        # Remove the frame of the specific product from the GUI
        order_frame.destroy()

        # Identify the store name
        store_name = self.product["store"]

        # Update GUI product list for the store
        product_to_remove = next(
            (p for p in self.cart_items[store_name]["products"] if p["name"] == product["name"]),
            None
        )

        if product_to_remove:
            self.cart_items[store_name]["products"].remove(product_to_remove)

        # If the store has no more products, remove its frame
        if not self.cart_items[store_name]["products"]:
            self.cart_items[store_name]["frame"].destroy()
            del self.cart_items[store_name]

        # Update the JSON database
        db_path = "database.json"
        try:
            with open(db_path, "r") as db_file:
                data = json.load(db_file)

            # Find the current user
            current_username = self.currentUser
            user = next((user for user in data["users"] if user["username"] == current_username), None)

            if not user:
                messagebox.showerror("Error", "User not found!")
                return

            # Remove the product from the user's cart in the database
            user["cart"] = [
                item for item in user["cart"]
                if not (item["product_name"] == product["name"] and item["shop_name"] == store_name)
            ]

            # Save the updated database
            with open(db_path, "w") as db_file:
                json.dump(data, db_file, indent=4)

            # Reload only the current store's products to update the GUI
            self.reload_store_gui(store_name, user["cart"])

            messagebox.showinfo("Success", f"Deleted {product['name']} from the cart!")

        except FileNotFoundError:
            messagebox.showerror("Error", "Database file not found!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Database file is corrupted!")

    def reload_store_gui(self, store_name, cart):
        if store_name in self.cart_items:
            for product in self.cart_items[store_name]["products"]:
                product["frame"].destroy()

            store_products = [item for item in cart if item["shop_name"] == store_name]
            for item in store_products:
                self.add_product_to_store_gui(store_name, item)

    def add_product_to_store_gui(self, store_name, product_data):
        product_name = product_data["product_name"]
        variation = f"Size: {product_data['size']}, Color: {product_data['color']}"
        price = product_data["price"]
        quantity = product_data["quantity"]
        image_path = product_data["image"]

        #Load the image if available
        if image_path:
            try:
                img = Image.open(image_path).resize((50, 50))
                picture = ImageTk.PhotoImage(img)
            except Exception as e:
                picture = None
                print(f"Error loading image: {e}")
        else:
            picture = None

        # Add the product to the GUI under the correct store frame
        if store_name not in self.cart_items:
            store_frame = tk.Frame(self.scrollable_frame, bd=2, relief="ridge", padx=79, pady=10)
            store_label = tk.Label(store_frame, text=f"Store: {store_name}", font=("Arial", 14))
            store_label.pack(padx=10, pady=5)
            store_frame.pack(fill="x", padx=10, pady=10)
            self.cart_items[store_name] = {"frame": store_frame, "products": []}

        order_frame = tk.Frame(self.cart_items[store_name]["frame"], padx=10, pady=10)
        order_frame.pack(fill="x", padx=10, pady=5)

        checkbox = tk.Checkbutton(order_frame, variable=tk.IntVar(), command=self.update_total_price)
        checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        if picture:
            pic_label = tk.Label(order_frame, image=picture)
            pic_label.image = picture
            pic_label.grid(row=0, column=1, padx=5, pady=5)
        else:
            tk.Label(order_frame, text="No Image").grid(row=0, column=1, padx=5, pady=5)

        details_frame = tk.Frame(order_frame)
        details_frame.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        tk.Label(details_frame, text=f"Product: {product_name}", font=("Arial", 10)).pack(anchor="w")
        tk.Label(details_frame, text=f"Variation: {variation}", font=("Arial", 10)).pack(anchor="w")

        tk.Label(order_frame, text=f"Price: ₱{price:.2f}", font=("Arial", 10)).grid(row=0, column=3, padx=150, pady=5)

        #COMMENTED, FOR FUTURE PURPOSES
        '''quantity_spinner = tk.Spinbox(
            order_frame, 
            from_=1, 
            to=99, 
            textvariable=tk.IntVar(value=quantity), width=5,
            command=lambda: self.update_total(order_frame, product_data))
        quantity_spinner.grid(row=0, column=4, padx=30, pady=5)'''

        quantity_label = tk.Label(
            order_frame, 
            textvariable=self.product["quantity_var"]
        )
        quantity_label.grid(row=0, column=4, padx=30, pady=5)

        total_price_label = tk.Label(order_frame, text=f"Total: ₱{price * quantity:.2f}", font=("Arial", 10))
        total_price_label.grid(row=0, column=5, padx=120, pady=5)

        delete_button = tk.Button(
            order_frame, text="Delete",
            command=lambda: self.delete_item(order_frame, product_data))
        delete_button.grid(row=0, column=6, padx=5, pady=5)

        #add to cart_items for tracking
        self.cart_items[store_name]["products"].append({"frame": order_frame, "name": product_name})

#===================ALL ABOUT SA BABA===================
    #===================GUI SA BABA===================
    def bottom_Content(self):
        bottomFrame = tk.Frame(self.myCartPageFrame, width=800, height=90)
        bottomFrame.pack(side="bottom", anchor='s', fill="x")
        
        tk.Frame(
            bottomFrame, 
            width=1500, 
            height=1, 
            bg='black').place(x=0, y=1)
        
        self.select_all_var = tk.IntVar()
        self.selectAllChkbtn = tk.Checkbutton(
            bottomFrame,
            text="Select All",
            variable=self.select_all_var, 
            border=1,
            font=(msyulfont, 16, 'bold'),
            command=self.select_all_products)
        self.selectAllChkbtn.place(x=120, y=28)

        deleteBtn = tk.Button(
            bottomFrame,
            text="Delete",
            bd=0,
            font=(msyulfont, 16, 'bold'),
            command=self.delete_selected_products)
        deleteBtn.place(x=250, y=24)

        self.totalNumLbl = tk.Label(
            bottomFrame,
            text="Total Price: ₱0.00",
            font=(msyulfont, 25, 'bold'),
            fg=mainColor)
        self.totalNumLbl.place(x=550, y=20)

        checkoutBtn = tk.Button(
            bottomFrame,
            text="CHECKOUT",
            bg=mainColor,
            bd=0,
            fg="white",
            font=(msyulfont, 16),
            command=self.checkout)
        checkoutBtn.place(x=1050, y=24, width=300)

    #===================FUNCTIONS SA BABA===================
    def delete_selected_products(self):
        for store_name in list(self.cart_items.keys()):
            store_products = self.cart_items[store_name]["products"]
            for item in store_products[:]:
                if item["selected_var"].get() == 1:
                    self.delete_item(item["frame"], item)
        self.update_total_price()

    def select_all_products(self):
        #mu-update tanan checkboxes base sa select all
        for store in self.cart_items: 
            for item in self.cart_items[store]["products"]:
                item["selected_var"].set(self.select_all_var.get())  #select/deselect tanan checkboxes base sa select all

        #total tanan naka-select
        self.update_total_price()

    def update_total_price(self):
        total_price = 0
        search_query = self.search_var.get().strip().lower()

        for store in self.cart_items:
            for item in self.cart_items[store]["products"]:
                if (not search_query or search_query in item["name"].lower()) and item["selected_var"].get() == 1:
                    quantity = item["quantity_var"].get()
                    total_price += item["price"] * quantity  #add to the total price based sa quantity

        self.totalNumLbl.config(text=f"Total Price: ₱{total_price:.2f}")  #update ang mismong label

    def checkout(self):
        selected_items = [
            item for store in self.cart_items.values()
            for item in store["products"]
            if item["quantity"] > 0  #check for non-zero quantities
        ]
        #commented, for future purposes
        #selected_items = [item for store in self.cart_items.values() for item in store["products"] if item["selected_var"].get() == 1]
        if not selected_items:
            messagebox.showinfo("Error", "No items selected for checkout!")
        else:
            #open Place Order window
            checkout_window = tk.Toplevel(self.myCartPageFrame)
            PlaceOrderPage(checkout_window, selected_items, self, self.currentUser)
    
#===================OTHERS===================
    #para sa search
    def filter_products(self, *args):
        search_query = self.search_var.get().lower().strip()

        if search_query == "🔍search products...":
            search_query = ""

        for store_name, store_data in self.cart_items.items():
            store_frame = store_data["frame"]
            store_products = store_data["products"]

            #track ug ang store has any matching products
            store_matches = False

            for product in store_products:
                product_widget = product["frame"]
                if search_query in product["name"].lower():
                    product_widget.pack(fill="x", padx=10, pady=5)  #pakita ang gi-search ni user
                    store_matches = True
                else:
                    product_widget.pack_forget()  #hide non-matching products

            if store_matches:
                store_frame.pack(fill="x", padx=10, pady=10)  #ug naay ni-match, pakita ang store
            else:
                store_frame.pack_forget()  #ug wla, i-hide ang store

    #para ma-scroll gamit ang mousewheel
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

#===================PLACE ORDER WINDOW (SEPARATE CLASS FOR READABILITY)===================
class PlaceOrderPage:
    SHIPPING_FEE_PER_STORE = 50  #constant shipping fee per store, meaning, PERMI NA 50

    def __init__(self, root, selected_items, cart_page, username):
        self.root = root
        self.root.title("Checkout")
        self.root.geometry('980x500+280+120')
        self.root.resizable(False, False)
        self.cart_page = cart_page  #ang cart page
        self.username = username

        #main frame para sa place order guis
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        #for scrolling
        self.canvas = tk.Canvas(main_frame)
        self.scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        #configure canvas para connect scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #bind scrollable frame sa canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        cart_data = self.load_cart_data()
        self.display_cart_summary(cart_data)

    def load_cart_data(self):
        #i-read sa ang json
        with open("database.json", "r") as file:
            data = json.load(file)

        #extract the cart of the first user
        user_cart = data["users"][0]["cart"]
        grouped_cart = {}

        #group products by same store
        for item in user_cart:
            store_name = item["shop_name"]
            if store_name not in grouped_cart:
                grouped_cart[store_name] = []
            grouped_cart[store_name].append(item)

        return grouped_cart

    #ang mismong cart summary with calculations
    def display_cart_summary(self, grouped_cart):
        """
        Display cart items nga naka-grouped by store.
        """
        self.grouped_items = grouped_cart
        merchandise_total = 0
        total_shipping_fee = 0

        for store_name, products in grouped_cart.items():
            #Store frame
            store_frame = tk.Frame(self.scrollable_frame, bd=2, relief="solid", padx=10, pady=10)
            store_frame.pack(fill="x", padx=20, pady=10)

            #Store name
            tk.Label(store_frame, text=store_name, font=("Arial", 14, "bold")).pack(anchor="w")

            #Table header
            header_frame = tk.Frame(store_frame)
            header_frame.pack(fill="x", pady=5)

            headers = [
                "Products Ordered",
                "Unit Price",
                "Discount",
                "Discounted Price",
                "Quantity",
                "Total Price",
            ]
            column_widths = [20, 10, 10, 15, 10, 15]

            for i, header in enumerate(headers):
                tk.Label(
                    header_frame, text=header, font=("Arial", 12, "bold"), width=column_widths[i], anchor="w"
                ).grid(row=0, column=i, padx=5, pady=5)

            #Product details
            store_total = 0
            for product in products:
                product_frame = tk.Frame(store_frame)
                product_frame.pack(fill="x")

                tk.Label(product_frame, text=product["product_name"], font=("Arial", 10), width=30, anchor="w").grid(
                    row=0, column=0, padx=5, pady=5
                )
                tk.Label(product_frame, text=f"₱{product['price']:.2f}", font=("Arial", 10), width=10).grid(
                    row=0, column=1, padx=5, pady=5
                )
                tk.Label(product_frame, text=f"{product['discount']:.2f}%", font=("Arial", 10), width=10).grid(
                    row=0, column=2, padx=5, pady=5
                )
                tk.Label(product_frame, text=f"₱{product['discounted_price']:.2f}", font=("Arial", 10), width=15).grid(
                    row=0, column=3, padx=5, pady=5
                )
                tk.Label(product_frame, text=f"{product['quantity']}", font=("Arial", 10), width=10).grid(
                    row=0, column=4, padx=5, pady=5
                )
                tk.Label(product_frame, text=f"₱{product['total_price']:.2f}", font=("Arial", 10), width=15).grid(
                    row=0, column=5, padx=5, pady=5
                )

                store_total += product["total_price"]

            #Store total
            tk.Label(store_frame, text=f"Merchandise Total: ₱{store_total:.2f}", font=("Arial", 12, "bold")).pack(
                anchor="e", pady=5
            )

            shipping_fee = self.SHIPPING_FEE_PER_STORE
            total_shipping_fee += shipping_fee
            tk.Label(store_frame, text=f"Shipping Fee: ₱{shipping_fee:.2f}", font=("Arial", 12)).pack(
                anchor="e", pady=5
            )

            merchandise_total += store_total

        #Summary totals
        tax = merchandise_total * 0.03  #3% tax
        final_total = merchandise_total + total_shipping_fee + tax

        summary_frame = tk.Frame(self.scrollable_frame, pady=10)
        summary_frame.pack(fill="x", padx=20)

        tk.Label(summary_frame, text=f"Merchandise Subtotal: ₱{merchandise_total:.2f}", font=("Arial", 12)).pack(
        anchor="e", pady=5
        )
        tk.Label(summary_frame, text=f"Shipping Subtotal: ₱{total_shipping_fee:.2f}", font=("Arial", 12)).pack(
            anchor="e", pady=5
        )
        tk.Label(summary_frame, text=f"Tax (3%): ₱{tax:.2f}", font=("Arial", 12)).pack(
            anchor="e", pady=5
        )
        tk.Label(summary_frame, text=f"Final Total: ₱{final_total:.2f}", font=("Arial", 14, "bold")).pack(
            anchor="e", pady=10
        )

        #place order Button
        placeOrder_button = tk.Button(
            summary_frame,
            text="Place Order",
            fg="#fff",
            bg=mainColor,
            bd=0,
            width=20,
            height=1,
            font=(msyulfont, 16, "bold"),
            command=self.confirm_order,
        )
        placeOrder_button.pack(anchor="e", pady=10)

    def confirm_order(self):
        """
        Handle the confirmation of the order and update the cart and orders in the database.
        """
        #load the database
        with open("database.json", "r") as file:
            data = json.load(file)

        #get the current user by their username
        username = self.username  #ang current user
        user_data = next(user for user in data["users"] if user["username"] == username)
        
        #retrieve the user's cart and orders
        user_cart = user_data["cart"]
        user_orders = user_data["orders"]

        #loop para sa grouped items (cart items) to move them to orders
        for store, products in self.grouped_items.items():
            for product in products:
                # Create an order object from the cart product
                order = {
                    "product_name": product["product_name"],
                    "image": product["image"],
                    "size": product["size"],
                    "color": product["color"],
                    "discounted_price": product["discounted_price"],
                    "total_price": product["total_price"],
                    "store_name": product["shop_name"],
                    "status": "to pay",  
                    "purchasedBy": username  #Set the current user's name
                }

                #Add the new order to the user's orders list
                user_orders.append(order)

                #Remove the item from the user's cart
                user_cart = [item for item in user_cart if item["product_name"] != product["product_name"]]

        #Update the cart and orders in the database for the user
        user_data["cart"] = user_cart
        user_data["orders"] = user_orders

        #Save the updated data back to the database
        with open("database.json", "w") as file:
            json.dump(data, file, indent=4)

        #Refresh the UI
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()  # Clear all widgets from the frame

        #Reload and display updated cart
        cart_data = self.load_cart_data()
        self.display_cart_summary(cart_data)

        #Display confirmation message
        messagebox.showinfo("Order Confirmed", "Your order has been placed successfully!")

    #para ma scroll sa mousewheel
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")