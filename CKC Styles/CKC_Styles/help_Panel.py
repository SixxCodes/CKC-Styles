import tkinter as tk
from tkinter import ttk

'''
tanan mga nakabutang dri:
1. about sa help Panel sa sidebar Menu sa Home Panel
'''

mainColor = "#d1101a"

class help_Window:
    def __init__ (self, mainFrame):
        self.helpPageFrame = tk.Frame(mainFrame)

        self.create_header()
        self.content()
        self.helpPageFrame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.helpPageFrame, width=600, height=400)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.scrollbar = ttk.Scrollbar(self.helpPageFrame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", pady=60, expand=True)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.add_faqs()
    
    def create_header(self):
        header_frame = tk.Frame(self.helpPageFrame, bg=mainColor, height=60)
        header_frame.pack(side="top", fill="x")

    def content(self):
        helpLabel = tk.Label(
            self.helpPageFrame,
            text="Help",
            font=('Microsoft YaHei UI Light', 20, 'bold'))
        helpLabel.place(x=650, y=80)

        tk.Frame(
            self.helpPageFrame, 
            width=1150, 
            height=1, 
            bg='black').place(x=120, y=685)

        bottomLbl = tk.Label(
            self.helpPageFrame,
            text="If you don’t find the answers you’re looking for here, please reach out to our developers for assistance.",
            font=('Microsoft YaHei UI Light', 15, 'bold'))
        bottomLbl.place(x=170, y=696)

    #ang mga mismong questions
    def add_faqs(self):
        sections = {
            "1. Account Management": [
                ("Q1: How do I create an account?", "Click on the \"Sign Up\" button on the start screen. Fill out the required details like username and password, and then click \"Sign Up.\""),
                ("Q2: How do I delete my account?", "Go to the \"Account Settings\" section in the menu and click \"Delete Account.\" Re-enter your password to confirm deletion."),
                ("Q3: Can I switch between buyer and seller modes?", "Yes. Once logged in, navigate to the settings or profile page and toggle the \"Seller Mode\" option."),
            ],
            "2. Shopping and Cart": [
                ("Q1: How do I add items to my cart?", "Browse products, and when you find one you like, select it and click the \"Add to Cart\" button."),
                ("Q2: Can I remove items from my cart?", "Yes. Go to your cart, select the item you want to remove, and click the \"Remove\" button."),
                ("Q3: What happens to my cart if I log out?", "Your cart is saved and will be available when you log back in."),
            ],
            "3. Orders and Payments": [
                ("Q1: How do I place an order?", "After adding items to your cart, go to the cart section and click \"Checkout.\" Follow the prompts to confirm your order."),
                ("Q2: Can I view my previous orders?", "Yes. Go to the \"My Orders\" section in the sidebar menu to see past orders."),
            ],
            "4. Selling Mode": [
                ("Q1: How do I list a product for sale?", "In Seller Mode, navigate to \"Add Product.\" Enter details like product name, color, size, price, and description. Save to list it for sale."),
                ("Q2: How do I manage my listed products?", "In Seller Mode, go to \"Manage Products\" to edit or delete your listings."),
                ("Q3: Can I see feedback on my products?", "Yes. Feedback left by buyers will appear in the \"Product Reviews\" section."),
            ],
            "5. Technical Issues": [
                ("Q1: Why am I unable to log in?", "Ensure your username and password are correct. If the problem persists, restart the app or check if your account still exists."),
                ("Q2: What should I do if the app crashes or freezes?", "Restart the application. If the issue continues, check for corrupted data files in your app folder. If problem persists, contact the developers. You can check the “About” on the sidebar menu to see the developers, click on the pictures and it will direct you to their facebook accounts."),
            ],
            "6. Miscellaneous": [
                ("Q1: How is my data saved?", "Your data is stored locally on your device to ensure it is persistent even if the app is closed."),
                ("Q2: Can I leave reviews on products I’ve purchased?", "Yes. Go to your \"My Orders\", select the product, and leave a review in the \"Feedback\" section."),
                ("Q3: Where can I see all available products?", "On the \"Home\", you can see random listings of products. You can also search for products you want. You can also click on the categories to filter products."),
            ]
        }

        for section_title, faqs in sections.items():
            self.create_section_title(section_title)
            for question, answer in faqs:
                self.create_faq_section(question, answer)

    #QUESTION TITLES
    def create_section_title(self, title):
        title_label = ttk.Label(
            self.scrollable_frame, 
            text=title, 
            font=('Microsoft YaHei UI Light', 18, 'bold'), 
            anchor="w")
        title_label.pack(fill="x", padx=100, pady=10)

    #questions and answers
    def create_faq_section(self, question, answer):
        section_frame = ttk.Frame(self.scrollable_frame)
        section_frame.pack(fill="x", padx=150, pady=5, anchor="w")

        question_button = ttk.Button(
            section_frame, 
            text=question, 
            style="FAQ.TButton", 
            command=lambda: self.toggle_answer(answer_label))
        question_button.pack(side="left", anchor="w", padx=5)

        answer_label = ttk.Label(section_frame, text=answer, wraplength=700, justify="left")
        answer_label.pack(fill="x", anchor="w", padx=20)
        answer_label.pack_forget()

    #pagpindot sa question button, mupakita ang answer
    def toggle_answer(self, label):
        if label.winfo_ismapped():
            label.pack_forget()
        else:
            label.pack(fill="x", anchor="w", padx=20)

    #ma-scroll gamit mousewheel
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")     