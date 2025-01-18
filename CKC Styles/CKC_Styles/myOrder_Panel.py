import tkinter as tk
from tkinter import ttk
import json
import threading

'''
tanan mga nakabutang dri:
1. about sa Order Panel sa sidebar Menu sa Home Panel
2. ang gi place order nimo sa cart panel kay mupadulong diri
3. naay different status:
    To pay: pislit kag pay cod or pay online, if pislit na, proceed to second status
    To Ship: 5s ang shipping simulation
    To Receive: naay button nga "mark as received", if pislit
    Completed: complete na ang order
'''

mainColor = "#d1101a"
msyulfont = 'Microsoft YaHei UI Light'

class myOrder_Window:
    def __init__ (self, mainFrame, username):
        self.myOrderPageFrame = tk.Frame(mainFrame)

        self.create_order_item(self.myOrderPageFrame)

        self.username = username #current user

        self.load_orders()
        self.create_header()
        self.content()
        self.options()

        self.switch_Indicator(
            optionsFrameSI=self.optionsFrame,
            indicatorLb=self.homeBtnIndicator,
            page=self.all_Page
        )

        self.myOrderPageFrame.pack(fill=tk.BOTH, expand=True)

#===================HEADERS===================
    def create_header(self):
        header_frame = tk.Frame(self.myOrderPageFrame, bg=mainColor, height=60)
        header_frame.pack(side="top", fill="x")
        
    def content(self):
        myOrderLabel = tk.Label(
            self.myOrderPageFrame,
            text="My Orders",
            fg='black',
            font=(msyulfont, 23, 'bold'))
        myOrderLabel.place(x=70, y=80)

        search_frame = tk.Frame(self.myOrderPageFrame)
        search_frame.pack(anchor='ne', padx=10, pady=20)

        self.search_entry = tk.Entry(
            search_frame,
            width=40,
            bd=3,
            fg='black',
            font=(msyulfont, 14))
        self.search_entry.pack(side="right", padx=40, pady=10)
        self.search_entry.insert(0, "🔍Search Products...")
        self.search_entry.bind('<FocusIn>', self.on_enter_search)
        self.search_entry.bind('<FocusOut>', self.on_leave_search)
        self.search_entry.bind('<KeyRelease>', self.search_orders)  #dli na mag-enter, while ga-type, ga-search na sad

    #===================SEARCH FUNCTIONS===================
    def search_orders(self, event=None):
        query = self.search_entry.get().strip().lower()

        current_page_orders = []
        if hasattr(self, 'current_page_orders'):
            current_page_orders = self.current_page_orders
        else:
            current_page_orders = self.all_orders 

        if query in ["", "🔍search products..."]:
            filtered_orders = current_page_orders
        else:
            filtered_orders = [
                order for order in current_page_orders
                if query in order['product_name'].lower() or
                query in order['color'].lower() or
                query in order['size'].lower()
            ]

        for child in self.mainPageFrame.winfo_children():
            child.destroy()

        scrollable_frame = self.create_scrollable_frame(self.mainPageFrame)
        self.display_orders(scrollable_frame, filtered_orders)

    def on_enter_search(self, event):
        if self.search_entry.get() == "🔍Search Products...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def on_leave_search(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "🔍Search Products...")
            self.search_entry.config(fg="black")

#===================OPTIONS===================
    '''
    options:
    to pay
    to ship
    to receive
    completed
    cancelled (not implemented, future purposes)
    refund and return (not implemented, future purposes)
    '''
    def options(self):
        self.optionsFrame = tk.Frame(self.myOrderPageFrame)
        self.optionsFrame.pack_propagate(False)
        self.optionsFrame.configure(width=500, height=70)
        self.optionsFrame.pack(fill='x')

        allBtn = tk.Button(
            self.optionsFrame,
            text="All",
            font=(msyulfont, 14, 'bold'),
            bd=0,
            fg='black',
            command=lambda: self.switch_Indicator(
                optionsFrameSI=self.optionsFrame, 
                indicatorLb=self.homeBtnIndicator, 
                page=self.all_Page))
        allBtn.place(x=50, y=0, width=180, height=60)

        self.homeBtnIndicator = tk.Label(
            self.optionsFrame,
            bg=mainColor)
        self.homeBtnIndicator.place(x=50, y=60, width=180, height=3)

        toPayBtn = tk.Button(
            self.optionsFrame,
            text="To Pay",
            font=(msyulfont, 14, 'bold'),
            bd=0,
            fg='black',
            command=lambda: self.switch_Indicator(
                optionsFrameSI=self.optionsFrame, 
                indicatorLb=toPayBtnIndicator, 
                page=self.toPay_Page))
        toPayBtn.place(x=240, y=0, width=180, height=60)

        toPayBtnIndicator = tk.Label(
            self.optionsFrame)
        toPayBtnIndicator.place(x=240, y=60, width=180, height=3)

        toShipBtn = tk.Button(
            self.optionsFrame,
            text="To Ship",
            font=(msyulfont, 14, 'bold'),
            bd=0,
            fg='black',
            command=lambda: self.switch_Indicator(
                optionsFrameSI=self.optionsFrame, 
                indicatorLb=toShipBtnIndicator, 
                page=self.toShip_Page))
        toShipBtn.place(x=430, y=0, width=180, height=60)
        
        toShipBtnIndicator = tk.Label(
            self.optionsFrame)
        toShipBtnIndicator.place(x=430, y=60, width=180, height=3)

        toRecieveBtn = tk.Button(
            self.optionsFrame,
            text="To Receive",
            font=(msyulfont, 14, 'bold'),
            bd=0,
            fg='black',
            command=lambda: self.switch_Indicator(
                optionsFrameSI=self.optionsFrame, 
                indicatorLb=toRecieveBtnIndicator, 
                page=self.toRecieve_Page))
        toRecieveBtn.place(x=620, y=0, width=180, height=60)
        
        toRecieveBtnIndicator = tk.Label(
            self.optionsFrame)
        toRecieveBtnIndicator.place(x=620, y=60, width=180, height=3)

        completedBtn = tk.Button(
            self.optionsFrame,
            text="Completed",
            font=(msyulfont, 14, 'bold'),
            bd=0,
            fg='black',
            command=lambda: self.switch_Indicator(
                optionsFrameSI=self.optionsFrame, 
                indicatorLb=completedBtnIndicator, 
                page=self.completed_Page))
        completedBtn.place(x=810, y=0, width=180, height=60)

        completedBtnIndicator = tk.Label(
            self.optionsFrame)
        completedBtnIndicator.place(x=810, y=60, width=180, height=3)

        #COMMENTED, FUTURE PURPOSES
        '''cancelledBtn = tk.Button(
            self.optionsFrame,
            text="Cancelled",
            font=(msyulfont, 14, 'bold'),
            bd=0,
            fg='black',
            command=lambda: self.switch_Indicator(
                optionsFrameSI=self.optionsFrame, 
                indicatorLb=cancelledBtnIndicator, 
                page=self.cancelled_Page))
        cancelledBtn.place(x=1000, y=0, width=180, height=60)

        cancelledBtnIndicator = tk.Label(
            self.optionsFrame)
        cancelledBtnIndicator.place(x=1000, y=60, width=180, height=3)

        returnNRefundBtn = tk.Button(
            self.optionsFrame,
            text="Return & Refund",
            font=(msyulfont, 14, 'bold'),
            bd=0,
            fg='black',
            command=lambda: self.switch_Indicator(
                optionsFrameSI=self.optionsFrame, 
                indicatorLb=returnNRefundBtnIndicator, 
                page=self.returnNRefund_Page))
        returnNRefundBtn.place(x=1190, y=0, width=170, height=60)

        returnNRefundBtnIndicator = tk.Label(
            self.optionsFrame)
        returnNRefundBtnIndicator.place(x=1190, y=60, width=180, height=3)'''

        tk.Frame(
            self.optionsFrame, 
            width=1500, 
            height=1, 
            bg='black').place(x=0, y=69)

        self.mainPageFrame = tk.Frame(
            self.myOrderPageFrame)
        self.mainPageFrame.pack_propagate(False)
        self.mainPageFrame.configure(height=700)
        self.mainPageFrame.pack(fill='x')

    #para mubalhin ug laing frame ug madestroy anf previous frame for switching pages
    def switch_Indicator(self, optionsFrameSI, indicatorLb, page):
        for child in optionsFrameSI.winfo_children():
            if isinstance(child, tk.Label):
                child['bg'] = '#f0f0f0'

        #highlight ang nakapislit
        indicatorLb['bg'] = mainColor

        for fn in self.mainPageFrame.winfo_children():
            fn.destroy()

        if page == self.all_Page:
            self.current_page_orders = self.all_orders
        elif page == self.toPay_Page:
            self.current_page_orders = self.to_pay_orders
        elif page == self.toShip_Page:
            self.current_page_orders = self.to_ship_orders
        elif page == self.toRecieve_Page:
            self.current_page_orders = self.to_receive_orders
        elif page == self.completed_Page:
            self.current_page_orders = self.completed_orders
        elif page == self.cancelled_Page: #(not implemented, future purposes)
            self.current_page_orders = self.cancelled_orders #(not implemented, future purposes)
        elif page == self.returnNRefund_Page: #(not implemented, future purposes)
            self.current_page_orders = self.return_and_refund_orders #(not implemented, future purposes)

        page(self.mainPageFrame)

#===================ABOUT ORDERS===================
    def create_order_item(self, pageFrame):
        with open("database.json", "r") as file:
            data = json.load(file)
        
        current_user = data['users'][0]  

        self.all_orders = []  #tana orders
        self.to_pay_orders = []
        self.to_ship_orders = []
        self.to_receive_orders = []
        self.completed_orders = []

        orders = current_user.get('orders', [])

        for order in orders:
            self.all_orders.append(order)
            if order['status'] == "To Pay":
                self.to_pay_orders.append(order)
            elif order['status'] == "To Ship":
                self.to_ship_orders.append(order)
            elif order['status'] == "To Receive":
                self.to_receive_orders.append(order)
            elif order['status'] == "Completed":
                self.completed_orders.append(order)

    '''
    this function is not used, commented ang naggamit ani
    wla gi-delete for back up
    '''
    def add_order_item(self, page, storeName, status, products):
        self._create_order_frame(page, storeName, status, products)

    #commented out, backup lang
    '''def display_orders(self, page, orders):
        with open("database.json", "r") as file:
            data = json.load(file)
        
        current_user = data['users'][0]  

        orders = current_user.get('orders', [])

        to_pay_orders = []
        to_ship_orders = []
        to_receive_orders = []
        completed_orders = []

        for order in orders:
            if order['status'] == "To Pay":
                to_pay_orders.append(order)
            elif order['status'] == "To Ship":
                to_ship_orders.append(order)
            elif order['status'] == "To Receive":
                to_receive_orders.append(order)
            elif order['status'] == "Completed":
                completed_orders.append(order)

        if not orders:
            no_orders_label = tk.Label(
                page, 
                text="Nothing to see here.", 
                font=(msyulfont, 16), 
                fg="black")
            no_orders_label.pack(padx=570, pady=200)
        else:
            if to_pay_orders:
                self.add_order_item(page, "To Pay", to_pay_orders)
            if to_ship_orders:
                self.add_order_item(page, "To Ship", to_ship_orders)
            if to_receive_orders:
                self.add_order_item(page, "To Receive", to_receive_orders)
            if completed_orders:
                self.add_order_item(page, "Completed", completed_orders)'''

    def load_orders(self):
        try:
            with open('database.json', 'r') as db_file:
                data = json.load(db_file)
                # Find the user by username
                for user in data['users']:
                    if user['username'] == self.username:
                        print(f"{self.username}")
                        return user['orders']
        except FileNotFoundError:
            print("Database file not found.")
        return []

    def display_orders(self, page, orders):
        user_orders = [order for order in orders if order['purchasedBy'] == self.username]
        print(f"Orders for {self.username}: {user_orders}")  # Debugging statement

        if not user_orders:
            no_orders_label = tk.Label(
                page, 
                text="Nothing to see here.", 
                font=(msyulfont, 16), 
                fg="black"
            )
            no_orders_label.pack(padx=570, pady=200)
        else:
            for order in user_orders:
                self._create_order_frame(page, order['store_name'], order['status'], order)

    #gui sa orders
    def _create_order_frame(self, parent, storeName, status, order):
        container_frame = tk.Frame(parent)
        container_frame.pack(padx=120, pady=10, fill="x")

        order_frame = tk.Frame(container_frame, bd=2, relief="solid", padx=10, pady=10)
        order_frame.pack(side="left", padx=10, pady=10, fill="x")

        store_label = tk.Label(order_frame, text=storeName, font=("Arial", 12), fg='black')
        store_label.pack()

        if status == "completed":
            order_status = tk.Label(order_frame, text=status, font=("Arial", 12), fg="green")
        else:
            order_status = tk.Label(order_frame, text=status, font=("Arial", 12), fg="red")
        order_status.pack(anchor="w")

        total_price = order['total_price']  

        product_frame = tk.Frame(order_frame)
        product_frame.pack(fill="x", pady=5)

        product_item_frame = tk.Frame(product_frame)
        product_item_frame.pack(fill="x", pady=5)

        product_image = tk.Canvas(product_item_frame, width=50, height=50, bg="gray")
        product_image.pack(side="left", padx=5)

        product_info = tk.Frame(product_item_frame)
        product_info.pack(side="left", padx=5, fill="x")

        product_title = tk.Label(product_info, text=order['product_name'], font=("Arial", 12, "bold"))
        product_title.pack(anchor="w")

        product_variation = tk.Label(product_info, text=f"Color: {order['color']}, Size: {order['size']}", font=("Arial", 10))
        product_variation.pack(anchor="w")

        product_price = tk.Label(product_info, text=f"P{order['discounted_price']}", font=("Arial", 12))
        product_price.pack(anchor="w")

        total_price_label = tk.Label(order_frame, text=f"Total Price: P{total_price}", font=("Arial", 12, "bold"), fg="blue")
        total_price_label.pack(anchor="e", pady=5)

        buttons_frame = tk.Frame(order_frame)
        buttons_frame.pack(fill="x", pady=5)

        if status == "completed":
            tk.Label(buttons_frame, text="", width=12).pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=12).pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=13).pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=80).pack(side="left", padx=5)
        elif status == "to pay":
            cod_button = tk.Button(buttons_frame, text="Pay COD", width=12, command=lambda: self.update_order_status(order, 'to ship'))
            cod_button.pack(side="left", padx=5)

            online_button = tk.Button(buttons_frame, text="Pay Online", width=12, command=lambda: self.update_order_status(order, 'to ship'))
            online_button.pack(side="left", padx=5)

            tk.Label(buttons_frame, text="", width=13).pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=80).pack(side="left", padx=5)
        elif status == "to receive":
            received_button = tk.Button(buttons_frame, text="Mark as Received", width=14, command=lambda: self.update_order_status(order, 'completed'))
            received_button.pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=12).pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=13).pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=80).pack(side="left", padx=5)
        else:
            tk.Label(buttons_frame, text="", width=12).pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=12).pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=13).pack(side="left", padx=5)
            tk.Label(buttons_frame, text="", width=80).pack(side="left", padx=5)

        store_info_box = tk.Frame(container_frame, padx=20, pady=10)
        store_info_box.pack(side="left", padx=10, pady=10, fill="x")

        store_info_frame = tk.Frame(store_info_box)
        store_info_frame.pack(fill="x")

        store_name_label = tk.Label(
            store_info_frame, 
            text=storeName, 
            font=(msyulfont, 20, 'bold'), 
            fg='black')
        store_name_label.pack(side="top", pady=5)

    def update_order_status(self, order, new_status):
        order['status'] = new_status  
        self.save_order_to_database(order)  

        if new_status == 'to ship':
            threading.Timer(15, self.auto_change_to_receive, [order]).start()  #300 seconds = 5 minutes, 15 for simulation lang
        self.refresh_order_page()  

    #auto change status to "to receive"
    def auto_change_to_receive(self, order):
        if order['status'] == 'to ship':  #dra ra mu-auto ug to ship ang status
            order['status'] = 'to receive'
            self.save_order_to_database(order)
            self.refresh_order_page()  

    #backup function, commented
    '''def save_order_to_database(self, order):
        # Open the database.json file and update the user's orders with the new status
        with open('database.json', 'r+') as f:
            data = json.load(f)
            for user in data['users']:
                if user['username'] == order['purchasedBy']:
                    for o in user['orders']:
                        if o['product_name'] == order['product_name']:
                            o['status'] = order['status']
                            # Save the updated order back to the file
                            f.seek(0)
                            json.dump(data, f, indent=4)
                            break'''

    def save_order_to_database(self, order):
        try:
            with open('database.json', 'r+') as f:
                data = json.load(f)  # Read the current data

                order_found = False
                for user in data['users']:
                    if user['username'] == order['purchasedBy']:
                        for o in user['orders']:
                            if o['product_name'] == order['product_name']:
                                o['status'] = order['status']
                                order_found = True
                                break

                if not order_found:
                    print("Order not found!")
                    return

                print(json.dumps(data, indent=4))  

                try:
                    json.dumps(data)  
                except json.JSONDecodeError as e:
                    print(f"Error in JSON format before writing: {e}")
                    return

                f.seek(0)
                json.dump(data, f, indent=4)  
                f.truncate() 

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def refresh_order_page(self):
        self.display_orders(self.myOrderPageFrame, self.all_orders)

#===================THE PAGES===================
    #prepared scrollable frame para sa mga pages
    def create_scrollable_frame(self, parent):
        frame = tk.Frame(parent)
        frame.pack_propagate(False)
        frame.configure(height=700)
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

        return scrollable_frame

    def all_Page(self, mainOptionFrameAP):
        allpageFrame = tk.Frame(mainOptionFrameAP)
        allpageFrame.pack_propagate(False)
        allpageFrame.configure(height=700)
        allpageFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(allpageFrame)
        
        self.display_orders(scrollable_frame, self.all_orders)

    def toPay_Page(self, mainOptionFrameAP):
        self.load_orders()  # Reload orders from JSON
        toPaypageFrame = tk.Frame(mainOptionFrameAP)
        toPaypageFrame.pack_propagate(False)
        toPaypageFrame.configure(height=700)
        toPaypageFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(toPaypageFrame)

        # Filter orders for the logged-in user
        user_to_pay_orders = [order for order in self.all_orders if order['status'] == 'to pay' and order['purchasedBy'] == self.username]
        self.display_orders(scrollable_frame, user_to_pay_orders)
        
    def toShip_Page(self, mainOptionFrameAP):
        toShipPageFrame = tk.Frame(mainOptionFrameAP)
        toShipPageFrame.pack_propagate(False)
        toShipPageFrame.configure(height=700)
        toShipPageFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(toShipPageFrame)
        
        to_ship_orders = [order for order in self.all_orders if order['status'].lower() == 'to ship']

        self.display_orders(scrollable_frame, to_ship_orders)

    def toRecieve_Page(self, mainOptionFrameAP):
        toRecievePageFrame = tk.Frame(mainOptionFrameAP)
        toRecievePageFrame.pack_propagate(False)
        toRecievePageFrame.configure(height=700)
        toRecievePageFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(toRecievePageFrame)
        
        to_receive_orders = [order for order in self.all_orders if order['status'].lower() == 'to receive']

        self.display_orders(scrollable_frame, to_receive_orders)

    def completed_Page(self, mainOptionFrameAP):
        completedPageFrame = tk.Frame(mainOptionFrameAP)
        completedPageFrame.pack_propagate(False)
        completedPageFrame.configure(height=700)
        completedPageFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(completedPageFrame)

        completed_orders = [order for order in self.all_orders if order['status'].lower() == 'completed']

        self.display_orders(scrollable_frame, completed_orders)

    #===================PAGES NOT IMPLEMENTED, FOR FUTURE PURPOSES===================
    def cancelled_Page(self, mainOptionFrameAP):
        cancelledPageFrame = tk.Frame(mainOptionFrameAP)
        cancelledPageFrame.pack_propagate(False)
        cancelledPageFrame.configure(height=700)
        cancelledPageFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(cancelledPageFrame)

        self.display_orders(scrollable_frame, self.cancelled_orders)

    def returnNRefund_Page(self, mainOptionFrameAP):
        returnNRefundPageFrame = tk.Frame(mainOptionFrameAP)
        returnNRefundPageFrame.pack_propagate(False)
        returnNRefundPageFrame.configure(height=700)
        returnNRefundPageFrame.pack(fill='x')

        scrollable_frame = self.create_scrollable_frame(returnNRefundPageFrame)
        
        self.display_orders(scrollable_frame, self.return_and_refund_orders)
    
    #aron ma-scroll gamit ang mousehweel sa mouse
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")