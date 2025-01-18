import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, PhotoImage, Toplevel

#=============== DATA MANAGEMENT ===============
DATA_FILE = "data.json"
CURRENT_USER_FILE = "current_user.txt"

def load_data():#
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"users": {}, "products": [], "orders": []}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def save_current_user():
    with open(CURRENT_USER_FILE, "w") as file:
        file.write(current_user if current_user else "")

def load_current_user():
    if os.path.exists(CURRENT_USER_FILE):
        with open(CURRENT_USER_FILE, "r") as file:
            return file.read().strip()
    return None

#=============== GLOBAL DATA ===============
data = load_data()
current_user = load_current_user()

#=============== ACCOUNT MANAGEMENT ===============
def signup():
    username = simpledialog.askstring("Signup", "Enter username:")
    if not username or username.strip() == "":
        messagebox.showerror("Error", "Username cannot be empty.")
        return

    if username in data["users"]:
        messagebox.showerror("Error", "Username already exists.")
        return

    password = simpledialog.askstring("Signup", "Enter password:")
    if not password or password.strip() == "":
        messagebox.showerror("Error", "Password cannot be empty.")
        return

    data["users"][username] = {
        "password": password,
        "is_seller": False,
        "shop_name": "",
        "cart": [],
        "orders": []
    }
    save_data(data)
    messagebox.showinfo("Success", "Signup successful!")


def login():
    global current_user
    username = simpledialog.askstring("Login", "Enter username:")
    password = simpledialog.askstring("Login", "Enter password:")

    if username in data["users"] and data["users"][username]["password"] == password:
        current_user = username
        save_current_user()
        messagebox.showinfo("Success", f"Welcome, {username}!")
    else:
        messagebox.showerror("Error", "Invalid credentials.")

def logout():
    global current_user
    current_user = None
    save_current_user()
    messagebox.showinfo("Logout", "Logged out.")
    main_menu()

def delete_account():
    global current_user
    if not current_user:
        return

    # Confirm user wants to delete account
    if not messagebox.askyesno("Confirm", "Are you sure you want to delete your account?"):
        return

    # Re-enter password to confirm
    password = simpledialog.askstring("Confirm Password", "Re-enter your password:")
    if password != data["users"][current_user]["password"]:
        messagebox.showerror("Error", "Incorrect password. Account deletion canceled.")
        return

    # Proceed with account deletion
    del data["users"][current_user]
    data["products"] = [p for p in data["products"] if p["seller"] != current_user]
    save_data(data)

    current_user = None
    save_current_user()
    messagebox.showinfo("Success", "Account and associated products deleted.")
    main_menu()


def my_account():
    global current_user
    user_data = data["users"][current_user]
    if not user_data["is_seller"]:
        if messagebox.askyesno("Seller Mode", "Do you want to become a seller?"):
            shop_name = simpledialog.askstring("Shop Name", "Enter your shop name:")
            if shop_name:
                user_data["is_seller"] = True
                user_data["shop_name"] = shop_name
                save_data(data)
                messagebox.showinfo("Success", f"You are now a seller with shop name: {shop_name}")
    else:
        messagebox.showinfo("Account Info", f"You are a seller. Shop name: {user_data['shop_name']}")

#=============== PRODUCT MANAGEMENT ===============
def add_product():
    if not data["users"][current_user]["is_seller"]:
        messagebox.showerror("Error", "Only sellers can add products.")
        return

    name = simpledialog.askstring("Add Product", "Enter product name:")
    colors = simpledialog.askstring("Add Product", "Enter available colors (comma-separated):")
    sizes = simpledialog.askstring("Add Product", "Enter available sizes (comma-separated):")
    categories = simpledialog.askstring("Add Product", "Enter product categories (comma-separated):")

    stock_info = {}
    for color in colors.split(","):
        stock_info[color] = {}
        for size in sizes.split(","):
            stock_info[color][size] = simpledialog.askinteger("Stock", f"Enter stock for {color} - {size}:")

    price = simpledialog.askfloat("Add Product", "Enter price:")
    voucher = simpledialog.askfloat("Add Product", "Enter discount voucher percentage (0-100, optional):", initialvalue=0.0)

    image_path = filedialog.askopenfilename(title="Select Product Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if not image_path:
        messagebox.showerror("Error", "No image selected.")
        return

    product = {
        "name": name,
        "colors": colors.split(","),
        "sizes": sizes.split(","),
        "categories": categories.split(","),
        "price": price,
        "stock_info": stock_info,
        "voucher": voucher,
        "seller": current_user,
        "purchases": [],
        "image": image_path
    }
    data["products"].append(product)
    save_data(data)
    messagebox.showinfo("Success", "Product added successfully!")

def view_products():
    if not data["products"]:
        messagebox.showinfo("Products", "No products available.")
        return

    def show_product_details(product):
        details_window = Toplevel()
        details_window.title(product["name"])

        try:
            img = PhotoImage(file=product["image"])
            img_label = tk.Label(details_window, image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack()
        except Exception as e:
            tk.Label(details_window, text="Image not available.").pack()

        details = f"Name: {product['name']}\nPrice: ${product['price']}\nSeller: {product['seller']}\nVoucher: {product['voucher']}%\n"
        details += "Stock Info:\n"
        for color, sizes in product["stock_info"].items():
            for size, stock in sizes.items():
                details += f"  {color} - {size}: {stock} left\n"
        tk.Label(details_window, text=details).pack()

        # Display reviews
        reviews = product.get("reviews", [])
        if reviews:
            tk.Label(details_window, text="Reviews:").pack()
            review_frame = tk.Frame(details_window)
            review_frame.pack(fill=tk.BOTH, expand=True)
            for review in reviews:
                review_text = f"Name: {review['buyer']}\nSize: {review['size']}\nColor: {review['color']}\nStars: {review['stars']}\nComment: {review['comment']}\n"
                tk.Label(review_frame, text=review_text, justify=tk.LEFT).pack(anchor="w")
        else:
            tk.Label(details_window, text="No reviews yet.").pack()

        # Add review button
        tk.Button(details_window, text="Add Review", command=lambda: add_review(product)).pack()

        def add_review(product):
            user_orders = data["users"][current_user]["orders"]

            # Filter user's purchases for this product
            eligible_purchases = [
                order for order in user_orders
                if order["product"] == product
            ]

            if not eligible_purchases:
                messagebox.showerror("Error", "You must purchase this product to leave a review.")
                return

            # Check if all eligible purchases have already been reviewed
            unreviewed_purchases = [
                purchase for purchase in eligible_purchases
                if not any(
                    review["buyer"] == current_user and 
                    review["color"] == purchase["color"] and 
                    review["size"] == purchase["size"]
                    for review in product.get("reviews", [])
                )
            ]

            if not unreviewed_purchases:
                messagebox.showerror("Error", "You have already reviewed all your purchases of this product.")
                return

            # Let user select which purchase they are reviewing
            purchase = unreviewed_purchases[0]  # Use the first unreviewed purchase

            # Gather review details
            stars = simpledialog.askinteger("Review", "Rate the product (1–5 stars):", minvalue=1, maxvalue=5)
            comment = simpledialog.askstring("Review", "Leave a comment (optional):")

            if not stars:
                messagebox.showerror("Error", "Rating is required.")
                return

            # Confirm review submission
            if not messagebox.askyesno("Confirm", "Are you sure you want to submit this review?"):
                return

            review = {
                "buyer": current_user,
                "color": purchase["color"],
                "size": purchase["size"],
                "stars": stars,
                "comment": comment or "No comment",
            }

            product.setdefault("reviews", []).append(review)
            save_data(data)
            messagebox.showinfo("Success", "Your review has been added.")


        #tk.Button(details_window, text="Add Review", command=add_review).pack()

    product_window = Toplevel()
    product_window.title("Products")

    for product in data["products"]:
        tk.Button(
            product_window,
            text=f"{product['name']} - ${product['price']}",
            command=lambda p=product: show_product_details(p)
        ).pack()


# =============== CART AND ORDERS ===============
def add_to_cart():
    if not data["products"]:
        messagebox.showinfo("Products", "No products available.")
        return

    def select_product(product):
        color = simpledialog.askstring("Choose Color", f"Available colors: {', '.join(product['colors'])}")
        size = simpledialog.askstring("Choose Size", f"Available sizes: {', '.join(product['sizes'])}")

        if color not in product["colors"] or size not in product["sizes"]:
            messagebox.showerror("Error", "Invalid color or size selection.")
            return

        if product["stock_info"].get(color, {}).get(size, 0) <= 0:
            messagebox.showerror("Error", "This product is out of stock.")
            return

        product["stock_info"][color][size] -= 1
        data["users"][current_user]["cart"].append({"product": product, "color": color, "size": size})
        save_data(data)
        messagebox.showinfo("Success", "Product added to cart!")

    cart_window = Toplevel()
    cart_window.title("Add to Cart")

    for product in data["products"]:
        tk.Button(cart_window, text=product["name"], command=lambda p=product: select_product(p)).pack()

def view_cart():
    cart = data["users"][current_user]["cart"]
    if not cart:
        messagebox.showinfo("Cart", "Cart is empty.")
        return

    cart_list = "\n".join([
        f"{i+1}. {item['product']['name']} - ${item['product']['price']}\n   Color: {item['color']}, Size: {item['size']}"
        for i, item in enumerate(cart)
    ])
    messagebox.showinfo("Cart", cart_list)

def checkout():
    cart = data["users"][current_user]["cart"]
    if not cart:
        messagebox.showinfo("Checkout", "Cart is empty.")
        return

    for item in cart:
        product = item["product"]
        product["purchases"].append(current_user)

    data["users"][current_user]["orders"].extend(cart)
    data["users"][current_user]["cart"] = []
    save_data(data)
    messagebox.showinfo("Success", "Checkout complete! Orders saved.")

def view_orders():
    orders = data["users"][current_user]["orders"]
    if not orders:
        messagebox.showinfo("Orders", "No orders found.")
        return

    order_list = "\n".join([
        f"{i+1}. {order['product']['name']} - ${order['product']['price']}\n   Color: {order['color']}, Size: {order['size']}"
        for i, order in enumerate(orders)
    ])
    messagebox.showinfo("Orders", order_list)

def seller_notifications():
    if not data["users"][current_user]["is_seller"]:
        messagebox.showerror("Error", "Only sellers can view notifications.")
        return

    purchases = [
        f"{p['name']} bought by {', '.join(p['purchases'])}" \
        for p in data["products"] if p["seller"] == current_user and p.get("purchases")
    ]

    if not purchases:
        messagebox.showinfo("Notifications", "No purchases yet.")
        return

    messagebox.showinfo("Notifications", "\n".join(purchases))

# =============== MAIN MENU ===============
def main_menu():
    if current_user:
        menu = tk.Tk()
        menu.title(f"E-Commerce - {current_user}")

        tk.Label(menu, text=f"Welcome, {current_user}").pack()

        tk.Button(menu, text="My Account", command=my_account).pack()
        tk.Button(menu, text="Add Product", command=add_product).pack()
        tk.Button(menu, text="View Products", command=view_products).pack()
        tk.Button(menu, text="Add to Cart", command=add_to_cart).pack()
        tk.Button(menu, text="View Cart", command=view_cart).pack()
        tk.Button(menu, text="Checkout", command=checkout).pack()
        tk.Button(menu, text="View Orders", command=view_orders).pack()
        tk.Button(menu, text="Seller Notifications", command=seller_notifications).pack()
        tk.Button(menu, text="Logout", command=lambda: [menu.destroy(), logout()]).pack()
        tk.Button(menu, text="Delete Account", command=lambda: [menu.destroy(), delete_account()]).pack()

        menu.mainloop()
    else:
        root = tk.Tk()
        root.title("E-Commerce")

        tk.Label(root, text="Welcome to E-Commerce System").pack()

        tk.Button(root, text="Signup", command=signup).pack()
        tk.Button(root, text="Login", command=lambda: [login(), root.destroy(), main_menu()]).pack()

        root.mainloop()

if __name__ == "__main__":
    main_menu()
