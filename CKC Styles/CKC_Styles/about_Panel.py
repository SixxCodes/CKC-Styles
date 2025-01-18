import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import webbrowser

'''
tanan mga nakabutang dri:
1. about sa About Panel sa sidebar Menu sa Home Panel
2. about sa amoang application
3. about sa mag developers and their contributions
4. acknowledgement para kang maam zoida
5. para ug pisliton ang amoang mga profile pictures kay muderetso sa amoang fb accounts
'''

mainColor = "#d1101a"
msyulfont = 'Microsoft YaHei UI Light'

class about_Window:
    def __init__(self, mainFrame):
        self.aboutPageFrame = tk.Frame(mainFrame)
        
        self.create_header()

        self.aboutPageFrame.pack(fill=tk.BOTH, expand=True)

        self.content_frame = ttk.Frame(self.aboutPageFrame)
        self.content_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.content_frame)
        self.canvas.pack(side="left", fill ="both", expand=True)
                
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
                    
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.content()

    def create_header(self):
        header_frame = tk.Frame(self.aboutPageFrame, bg=mainColor, height=60)
        header_frame.pack(side="top", fill="x")

    def content(self):
        topAboutUsFrame = tk.Frame(self.scrollable_frame)
        topAboutUsFrame.pack()

        about_us_label = tk.Label(
            topAboutUsFrame, 
            text="About Us", 
            font=(msyulfont, 30, 'bold'))
        about_us_label.pack(side="left", anchor='n', padx=130, pady=280)

        store_info = tk.Label(
            topAboutUsFrame, 
            text="At CKC Styles, founded by Charles, Kenny, and Chiedyusof, we are committed to providing an exceptional shopping experience. Our focus is on quality products, outstanding customer support, and reliable, fast delivery. We aim to create a welcoming community and offer a wide range of fashion choices to suit every style.",
            wraplength=600, 
            font=(msyulfont, 16),
            justify="left",
            width=70)
        store_info.pack(anchor='n', side="right", padx=50, pady=250)

        space_for_profiles = tk.Label(
            self.scrollable_frame,
            height=8)  
        space_for_profiles.pack(pady=5)

        title = tk.Label(
            self.scrollable_frame, 
            text="Meet the Developers", 
            font=(msyulfont, 20, 'bold'),
            height=3)  
        title.pack(pady=5)

        #====================DEVELOPERS====================

        developer_frame = tk.Frame(self.scrollable_frame)
        developer_frame.pack()

        #====================CHIED====================

        chiedFrame = tk.Frame(developer_frame)
        chiedFrame.pack(side="left", padx=60)

        self.add_profile(
            chiedFrame,
            "C:/Users/USER/Documents/Python/CKC Styles/product_images/chied.jpg",
            "https://www.facebook.com/chiedyusof.2005"
        )

        chied = tk.Label(
            chiedFrame, 
            text="Chiedyusof Mapuro", 
            font=(msyulfont, 20, 'bold'))
        chied.pack()

        chiedDesc = tk.Label(
            chiedFrame, 
            text="Responsible for conceptualizing ideas, designing user interfaces, and creating the overall layout.",
            font=(msyulfont, 14),
            wraplength=200)
        chiedDesc.pack()

        #====================KENNY====================

        kennyFrame = ttk.Frame(developer_frame)
        kennyFrame.pack(side="left", padx=20)

        self.add_profile(
            kennyFrame, 
            "C:/Users/USER/Documents/Python/CKC Styles/product_images/ken.jpg",
            "https://www.facebook.com/kenneth.crisostomo.45654"
        )

        kenny = tk.Label(
            kennyFrame, 
            text="Kenny Madayag", 
            font=(msyulfont, 20, 'bold'))
        kenny.pack()

        kennyDesc = tk.Label(
            kennyFrame, 
            text="Focused on design, enhancing visual appeal, and handling back-end development to ensure reliability and efficiency.",
            font=(msyulfont, 14),
            wraplength=200)
        kennyDesc.pack()

        #====================CHARLES====================

        charlesFrame = ttk.Frame(developer_frame)
        charlesFrame.pack(side="left", padx=90)
        
        self.add_profile(
            charlesFrame, 
            "C:/Users/USER/Documents/Python/CKC Styles/product_images/charles.jpg",
            "https://www.facebook.com/dennis.jay.710"
        )
        
        charles = tk.Label(
            charlesFrame, 
            text="Charles Entrina", 
            font=(msyulfont, 20, 'bold'))
        charles.pack()

        charlesDesc = tk.Label(
            charlesFrame, 
            text="Contributed to conceptualizing ideas, designing the user interface, and crafting the application layout.",
            font=(msyulfont, 14),
            wraplength=200)
        charlesDesc.pack()

        #====================MA'AM ZOIDA====================
        
        space2 = tk.Label(
            self.scrollable_frame,
            height=8)  
        space2.pack(pady=5)

        ackLbl = tk.Label(
            self.scrollable_frame, 
            text="Acknowledgement", 
            font=(msyulfont, 20, 'bold'),
            height=3)  
        ackLbl.pack(pady=5)

        maamFrame = ttk.Frame(self.scrollable_frame)
        maamFrame.pack(pady=20)
    
        self.add_profile(
            maamFrame, 
            "C:/Users/USER/Documents/Python/CKC Styles/product_images/maam.jpg",
            "https://www.facebook.com/zcyamba"
        )
        
        maam = tk.Label(
            maamFrame, 
            text="Zoida Clara L. Yamba", 
            font=(msyulfont, 20, 'bold'))
        maam.pack()

        maamDesc = tk.Label(
            maamFrame, 
            text="We extend our heartfelt gratitude to our professor for guiding us in learning Python and providing us with the foundational skills to bring this project to life.",
            font=(msyulfont, 14),
            wraplength=200)
        maamDesc.pack()

        space3 = tk.Label(
            self.scrollable_frame,
            height=8)  
        space3.pack(pady=5)

        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    #para ma-scroll gamit mousewheel
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def add_profile(self, parent_frame, image_path, profile_url):
        profile_frame = tk.Frame(parent_frame, width=15, height=10)
        profile_frame.pack()

        try:
            image = Image.open(image_path).resize((180, 180), Image.Resampling.LANCZOS)
            circular_image = self.create_circular_image(image)
            tk_image = ImageTk.PhotoImage(circular_image)
        except Exception as e:
            print(f"Error loading image!")
            tk_image = None

        if tk_image:
            profile_button = tk.Button(
                profile_frame, 
                image=tk_image, 
                command=lambda: self.open_profile(profile_url), 
                bd=0
            )
            profile_button.image = tk_image
        else:
            profile_button = tk.Button(
                profile_frame, 
                command=lambda: self.open_profile(profile_url)
            )

        profile_button.pack()

    #para circle ang pictures
    def create_circular_image(self, img):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
        result = Image.new("RGBA", img.size)
        result.paste(img, (0, 0), mask)
        return result

    #the logic here is para pagpindot sa profile is mudretso sa fb accounts sa mga profiles
    def open_profile(self, url):
        webbrowser.open(url) 