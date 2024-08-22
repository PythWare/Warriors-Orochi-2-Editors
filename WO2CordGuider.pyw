import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# folder used for storing map files, map files must be kept there.
folder1 = "maps"
maps_x = [600, 700, 800, 700, 600, 800, 700, 800, 700, 800, 700, 600, 600, 600, 700, 600, 800, 700, 800, 600, 600, 800, 800, 700, 700,
     800, 700, 800, 700, 800, 700, 600, 600, 600, 600, 800, 800, 600, 700, 800, 600, 600, 600, 600, 800, 600, 800, 800, 800, 600, 600,
     600, 700, 600, 600, 600, 800, 800, 800, 600, 600, 600, 800, 600, 700, 600, 800, 700]
maps_y = [600, 700, 800, 700, 600, 800, 700, 800, 700, 800, 700, 600, 600, 600, 700, 600, 800, 700, 800, 600, 600, 800, 800, 700, 700,
     800, 700, 800, 700, 800, 700, 600, 600, 600, 600, 800, 800, 600, 700, 800, 600, 600, 600, 600, 800, 600, 800, 800, 800, 600, 600,
     600, 700, 600, 600, 600, 800, 800, 800, 600, 600, 600, 800, 600, 700, 600, 800, 700]
maps = ['Shi_Ting.png', 'Ru_Xu_Kou.png', 'Bai_Di_Castle.png', 'Chang_Ban.png', 'Cheng_Du.png',
        'Chi_Bi.png', 'Edo_Castle.png', 'Guan_Du.png', 'He_Fei.png', 'Hinokawa.png',
        'Hu_Lao_Gate.png', 'Itsukushima.png', 'Jia_Meng_Gate.png',
        'Ji_Castle.png', 'Ji_Province.png', 'Kanegasake.png',
        'Kawanakajima.png', 'Komaki_Nagakute.png', 'Koshi_Castle.png',
        'Liang_Province.png', 'Lou_Sang_Village.png', 'Mikatagahara.png',
        'Nagashino.png', 'Nan_Zhong.png', 'Odani_Castle.png',
        'Odawara_Castle.png', 'Okehazama.png', 'Rescue_at_Hasedo.png',
        'Saika.png', 'Sekigahara.png', 'Shizugatake.png',
        'Si_Province.png', 'Si_Shui_Gate.png', 'Tong_Gate.png',
        'Wuhang_Mountains.png', 'Wu_Zhang_Plains.png', 'Yamatai.png',
        'Yamazaki.png', 'Yang_Ping_Gate.png', 'Yi_Ling.png', 'Dream_Chang_Sha.png',
        'Dream_Chen_Cang.png', 'Dream_Encounter_Nan_Zhong.png', 'Dream_Escape_Itsukushima.png', 'Dream_Fan_Castle.png',
        'Dream_Han_Sui.png', 'Dream_Hasedo.png', 'Dream_He_Fei.png', 'Dream_Hinokawa.png', 'Dream_Honnoji.png',
        'Dream_Jing_Province.png', 'Dream_Ji_Province.png', 'Dream_Kyushu.png', 'Dream_Lu_Shan.png', 'Dream_Mai_Castle.png',
        'Dream_Mount_Qi.png', 'Dream_Odawara_Castle.png', 'Dream_Osaka_Bay.png', 'Dream_Osaka_Castle.png',
        'Dream_Rescue_Nan_Zhong.png', 'Dream_Shikoku.png', 'Dream_Struggle_Nan_Zhong.png', 'Dream_Ueda_Castle.png',
        'Dream_Wu_Territory.png', 'Dream_Xia_Pi.png', 'Dream_Xin_Castle.png', 'Dream_Yamatai.png', 'Dream_Yan_Province.png']
class ImageMarkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warriors Orochi 2 Coordinate Guider")


        # Create a canvas to display the image
        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        # Entry widgets for x and y coordinates
        vcmd = (self.root.register(self.validate_int), '%S', '%P')
        
        self.x_entry = tk.Entry(root, width=10, validate='key', validatecommand=vcmd)
        self.x_entry.pack(side=tk.LEFT, padx=5)
        
        self.y_entry = tk.Entry(root, width=10, validate='key', validatecommand=vcmd)
        self.y_entry.pack(side=tk.LEFT, padx=5)

        # Button to mark the image
        self.mark_button = tk.Button(root, text="Mark", command=self.mark_image)
        self.mark_button.pack(pady=5)

        # Combobox for selecting images
        self.image_selector = ttk.Combobox(root, values= maps, state="readonly", width = 32)
        self.image_selector.current(0)  # Select the first image by default
        self.image_selector.pack(pady=5)
        self.image_selector.bind("<<ComboboxSelected>>", self.update_image)

        # Button to clear markers on the image
        self.clear_button = tk.Button(root, text="Clear Markers", command=self.clear_markers)
        self.clear_button.pack(pady=5)

        # Initialize variables
        self.image = None
        self.markers = []

        # Bind mouse click to mark image
        self.canvas.bind("<Button-1>", self.mark_image_with_click)

    def validate_int(self, new_value, current_value):
        # Validate if the input value is an integer
        if new_value.isdigit() or new_value == "":
            return True
        else:
            return False

    def load_image(self, image_path):
        # Clear previous image and markers
        self.canvas.delete("all")
        self.markers = []

        # Load image using tkinter's PhotoImage
        self.image = tk.PhotoImage(file=os.path.join(folder1,image_path))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

    # Used to update the image being displayed based on the selected file
    def update_image(self, event=None):
        selected_image = self.image_selector.get()
        if selected_image in maps:
            self.index = maps.index(selected_image)
            self.width = maps_x[self.index]
            self.height = maps_y[self.index]
            self.canvas.config(width = self.width, height = self.height)
        self.load_image(selected_image)

    # used for marking positions on the map
    def mark_image(self):
        # Get x and y coordinates from entry widgets
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            
            # Validate x and y coordinates within the range 0 to 800
            if 0 <= x <= 800 and 0 <= y <= 800:
                # Adjust y-coordinate to match upward-increasing coordinate system
                adjusted_y = self.height - y
                
                # Draw a red dot at the specified coordinates
                marker = self.canvas.create_oval(x-5, adjusted_y-5, x+5, adjusted_y+5, outline="red", width=3)
                self.markers.append(marker)
            else:
                # Display an error message or handle out-of-range coordinates
                messagebox.showerror("Error", "Coordinates must be within the range 0 to 800.")
        except ValueError:
            # Handle cases where x or y is not a valid integer
            messagebox.showerror("Error", "Invalid input. Please enter valid integer coordinates.")

    # used for marking the image based on where the user clicks
    def mark_image_with_click(self, event):
        # Get coordinates of mouse click
        x = event.x
        y = event.y

        # Adjust y-coordinate to match upward-increasing coordinate system
        adjusted_y = self.height - y

        # Display current coordinates
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(x))
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, str(adjusted_y))

        # Draw a red dot at the clicked coordinates
        marker = self.canvas.create_oval(x-5, y-5, x+5, y+5, outline="red", width=3)
        self.markers.append(marker)
    # used to remove markers on the image
    def clear_markers(self):
        for marker in self.markers:
            self.canvas.delete(marker)
        self.markers = []

if __name__ == "__main__":
    os.makedirs(folder1, exist_ok= True)
    root = tk.Tk()
    app = ImageMarkerApp(root)
    root.mainloop()
