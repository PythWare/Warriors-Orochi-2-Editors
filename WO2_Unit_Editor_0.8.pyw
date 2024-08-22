import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
import shutil
import os
file1 = "WO2.iso" # main file
wo2_unitfiles = ["Unit.WO2unit", "Unit.WO2ref", ".WO2unitmod"] # files used for the editor
folds = ["WO2_Stages", "WO2_Units", "Backups_For_Mod_Disabling", "icons"]
wo2_unitdata = [832, 36, 29952]
class TheCheck:
    @staticmethod
    def validate_numeric_input(new_value):
        return new_value == "" or (new_value.replace(".", "", 1).isdigit() and '.' not in new_value and float(new_value) >= 0)
    
def rem(files1, files2): # everytime the script is ran delete the old files to create fresh unmodified versions
    filepath1 = os.path.join(folds[1], files1)
    if os.path.isfile(filepath1):
            os.remove(filepath1)
    filepath2 = os.path.join(folds[1], files2)
    if os.path.isfile(filepath2):
        os.remove(filepath2)
class Orochi2(TheCheck):
    def __init__(self, root):
        self.root = root
        self.root.title("Warriors Orochi 2 Unit Editor")
        self.root.iconbitmap(os.path.join(folds[3], "icon1.ico"))
        self.root.minsize(1300, 700)
        self.root.resizable(False, False)
        self.modname = tk.StringVar()
        self.unit_path = os.path.join(folds[1], wo2_unitfiles[0])
        self.bunit_path = os.path.join(folds[2], wo2_unitfiles[0])
        self.unit_ref_data = os.path.join(folds[1], wo2_unitfiles[1])

        self.name1 = tk.IntVar() # 2 bytes
        self.name2 = tk.IntVar() # 2 bytes
        self.rank = tk.IntVar() # 1 byte
        self.voice = tk.IntVar() # 1 byte
        self.model = tk.IntVar() # 1 byte
        self.motion = tk.IntVar() # 1 byte
        self.horse = tk.IntVar() # 1 byte
        self.unk1 = tk.IntVar() # 1 byte
        self.weapon1 = tk.IntVar() # 1 bytes
        self.weapon2 = tk.IntVar() # 1 bytes
        self.life = tk.IntVar() # 2 bytes
        self.musou = tk.IntVar() # 2 bytes
        self.attack = tk.IntVar() # 2 bytes
        self.defense = tk.IntVar() # 2 bytes
        self.mounted = tk.IntVar() # # 2 bytes
        self.speed = tk.IntVar() # 2 bytes
        self.colors = tk.IntVar() # 1 byte
        self.aitype = tk.IntVar() # 1 byte
        self.ailevel = tk.IntVar() # 1 byte
        self.multiunit = tk.IntVar() # 1 byte
        self.guardid = tk.IntVar() # 2 bytes
        self.leaderid = tk.IntVar() # 2 bytes
        self.unittypemaybe = tk.IntVar() # 1 byte
        self.unk2 = tk.IntVar() # 1 byte
        self.unk3 = tk.IntVar() # 1 byte
        self.unk4 = tk.IntVar() # 1 byte

        self.gui_misc()
        self.gui_labels()
        self.gui_entries()
        self.unit_reading()
        self.unit_ref()
    # Function to handle selection change
    def on_select(self, event):
        selected_unit = self.combo.get()
    def slot_selected(self, event=None): # update display data
        self.selected_slot_value = self.selected_slot.get()
        self.unit_display(self.selected_slot_value)
    def unit_reading(self):
        global getoffset
        aob_pattern = b'\x7B\x76\x40\x03\x00\x00' # chunk to find that starts before unit data
        chunk_size = 4096
        with open(file1, "rb") as f1:
            offset = 0
            found = False
            
            while not found:
                chunk = f1.read(chunk_size)
                if not chunk:
                    break  # End of file
                
                # Search for the pattern in the current chunk
                pattern_offset = chunk.find(aob_pattern)
                
                if pattern_offset != -1:
                    # Calculate the absolute offset in the ISO file
                    getoffset = offset + pattern_offset + 6
                    with open(self.unit_path, "ab") as f2:
                        # Seek to the calculated offset in the ISO file
                        f1.seek(getoffset)
                        
                        # Read and write the data to self.unit_path
                        for i in range(wo2_unitdata[0]):
                            unitdata1 = f1.read(wo2_unitdata[1])
                            f2.write(unitdata1)
                        f2.write(getoffset.to_bytes(4, "little"))
                    found = True  # Exit loop since pattern is found
                
                offset += chunk_size
        
        if not found:
            print("AOB pattern not found in ISO file.")

        if not os.path.exists(self.bunit_path):
            shutil.copy(self.unit_path, self.bunit_path)
    def unit_ref(self):
        with open(self.unit_path, "rb") as r1:  # Open the corresponding .ref file for writing
            with open(self.unit_ref_data, "ab") as r2:
                offset = 0  # Initialize offset counter
                while True:
                    data_chunk = r1.read(wo2_unitdata[1])  # Read a 36-byte chunk from .data file
                    if not data_chunk:  # Break loop if end of file is reached
                        break
                    r2.write(offset.to_bytes(8, "little"))  # Write the offset to the .ref file
                    offset += wo2_unitdata[1]  # Move offset to the next chunk
    def submit_unit(self):
        try:
            col = [self.name1.get().to_bytes(2, "little"), self.name2.get().to_bytes(2, "little"), self.rank.get().to_bytes(1, "little"), self.voice.get().to_bytes(1, "little"),
                         self.model.get().to_bytes(1, "little"), self.motion.get().to_bytes(1, "little"), self.horse.get().to_bytes(1, "little"),
                         self.unk1.get().to_bytes(1, "little"), self.weapon1.get().to_bytes(1, "little"), self.weapon2.get().to_bytes(1, "little"), self.life.get().to_bytes(2, "little"),
                         self.musou.get().to_bytes(2, "little"), self.attack.get().to_bytes(2, "little"), self.defense.get().to_bytes(2, "little"),
                         self.mounted.get().to_bytes(2, "little"), self.speed.get().to_bytes(2, "little"), self.colors.get().to_bytes(1, "little"),
                         self.aitype.get().to_bytes(1, "little"), self.ailevel.get().to_bytes(1, "little"), self.multiunit.get().to_bytes(1, "little"),
                         self.guardid.get().to_bytes(2, "little"), self.leaderid.get().to_bytes(2, "little"), self.unittypemaybe.get().to_bytes(1, "little"),
                   self.unk2.get().to_bytes(1, "little"), self.unk3.get().to_bytes(1, "little"), self.unk4.get().to_bytes(1, "little")]
                   
            unit_slot = self.selected_slot.get()
            with open(self.unit_ref_data, "rb") as r1: # for obtaining the offset for a unit slot from the .ref file
                uservalue = unit_slot * 8
                r1.seek(uservalue)
                getoffset = int.from_bytes(r1.read(8), "little")
                with open(self.unit_path, "r+b") as f1: # for updating the unit slot with the current values from collectit
                    f1.seek(getoffset)
                    for b in col:
                        f1.write(b)                       
            self.status_label.config(text=f"Values submitted successfully.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
            
    def create_unit_mod(self): # for creating a mod file with custom extension
        global getoffset
        sep = "." # to be used for correcting possible user filenames that have their own extension
        try:
            usermodname = self.modname.get().split(sep, 1)[0] + wo2_unitfiles[2] # Create modname with the user entered name and stage extension based on the .ref file selected
            with open(self.unit_path, "rb") as r1:
                data = r1.read()
                offset = r1.tell()
                with open(usermodname, "wb") as w1:
                    w1.write(data)
            self.status_label.config(text=f"Mod file '{usermodname}' created successfully.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error creating mod file '{usermodname}': {str(e)}", fg="red")

    def unit_display(self, selected_slot_value):
        with open(self.unit_ref_data, "rb") as r1: # .ref file
            useroffset = self.selected_slot_value
            uservalue = self.selected_slot_value * 8
            r1.seek(uservalue)
            getoffset = int.from_bytes(r1.read(8), "little")
            with open(self.unit_path, "r+b") as r2:
                r2.seek(getoffset)
                unitname1 = int.from_bytes(r2.read(2), "little")
                unitname2 = int.from_bytes(r2.read(2), "little")
                unitrank = int.from_bytes(r2.read(1), "little")
                unitvoice = int.from_bytes(r2.read(1), "little")
                unitmodel = int.from_bytes(r2.read(1), "little")
                unitmotion = int.from_bytes(r2.read(1), "little")
                unithorse = int.from_bytes(r2.read(1), "little")
                unitunk1 = int.from_bytes(r2.read(1), "little")
                unitweapon1 = int.from_bytes(r2.read(1), "little")
                unitweapon2 = int.from_bytes(r2.read(1), "little")
                unitlife = int.from_bytes(r2.read(2), "little")
                unitmusou = int.from_bytes(r2.read(2), "little")
                unitattack = int.from_bytes(r2.read(2), "little")
                unitdefense = int.from_bytes(r2.read(2), "little")
                unitmounted = int.from_bytes(r2.read(2), "little")
                unitspeed = int.from_bytes(r2.read(2), "little")
                unitcolors = int.from_bytes(r2.read(1), "little")
                unitaitype = int.from_bytes(r2.read(1), "little")
                unitailevel = int.from_bytes(r2.read(1), "little")
                unitmultiunit = int.from_bytes(r2.read(1), "little")
                unitguardid = int.from_bytes(r2.read(2), "little")
                unitleaderid = int.from_bytes(r2.read(2), "little")
                unittypemay = int.from_bytes(r2.read(1), "little")
                unitunk2 = int.from_bytes(r2.read(1), "little")
                unitunk3 = int.from_bytes(r2.read(1), "little")
                unitunk4 = int.from_bytes(r2.read(1), "little")

                self.name1.set(unitname1)
                self.name2.set(unitname2)
                self.rank.set(unitrank)
                self.voice.set(unitvoice)
                self.model.set(unitmodel)
                self.motion.set(unitmotion)
                self.horse.set(unithorse)
                self.unk1.set(unitunk1)
                self.weapon1.set(unitweapon1)
                self.weapon2.set(unitweapon2)
                self.life.set(unitlife)
                self.musou.set(unitmusou)
                self.attack.set(unitattack)
                self.defense.set(unitdefense)
                self.mounted.set(unitmounted)
                self.speed.set(unitspeed)
                self.colors.set(unitcolors)
                self.aitype.set(unitaitype)
                self.ailevel.set(unitailevel)
                self.multiunit.set(unitmultiunit)
                self.guardid.set(unitguardid)
                self.leaderid.set(unitleaderid)
                self.unittypemaybe.set(unittypemay)
                self.unk2.set(unitunk2)
                self.unk3.set(unitunk3)
                self.unk4.set(unitunk4)

    def gui_misc(self):
        hex_values = [hex(i) for i in range(832)]
        self.selected_slot = tk.IntVar(self.root)
        self.selected_slot.set(0)  # Default value
        slot_combobox = ttk.Combobox(self.root, textvariable=self.selected_slot, values=hex_values)
        slot_combobox.bind("<<ComboboxSelected>>", self.slot_selected)
        slot_combobox.place(x=1100, y=30)
        tk.Label(self.root, text="Select the Unit Slot to mod").place(x=1100, y=0)
        tk.Button(self.root, text = "Create Unit Mod", command=self.create_unit_mod, height = 5, width = 20).place(x=1100,y=330)
        mm1 = tk.Entry(self.root, textvariable = self.modname).place(x=1100,y=260)
        mm2 = tk.Label(self.root, text = f"Enter a mod name").place(x=1100,y=230)
        self.mod_manager = tk.Button(self.root, text = "WO2 Mod Manager", command = self.open_mod_manager, height = 10, width = 20)
        self.mod_manager.place(x=1100, y=530)
    def gui_labels(self):
        self.icons = ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", 
                      "img6.png", "img7.png", "img8.png", "img9.png", "img10.png", 
                      "img11.png", "img12.png", "img13.png", "img14.png"]
        # Create PhotoImage objects for each icon
        self.images = []
        for icon in self.icons:
            img_path = os.path.join(folds[3], icon)

            # Load the image using PhotoImage
            tk_img = tk.PhotoImage(file=img_path)
            self.images.append(tk_img)

        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.place(x=400, y=330)
        self.info_label = tk.Label(self.root, text="""Credit goes to Michael for documentation on Warriors Orochi 2. You can mod Units in this Editor.
        Some values are not fully known yet.""").place(x=300, y=400)
        # Create and place labels with corresponding images
        tk.Label(self.root, text="Unit Name", compound=tk.LEFT, image=self.images[1]).place(x=0, y=0)
        tk.Label(self.root, text="Unit Rank", compound=tk.LEFT, image=self.images[2]).place(x=0, y=80)
        tk.Label(self.root, text="Unit Voice", compound=tk.LEFT, image=self.images[3]).place(x=0, y=160)
        tk.Label(self.root, text="Unit Model", compound=tk.LEFT, image=self.images[4]).place(x=0, y=240)
        tk.Label(self.root, text="Unit Motion", compound=tk.LEFT, image=self.images[4]).place(x=200, y=0)
        tk.Label(self.root, text="Unit Horse", compound=tk.LEFT, image=self.images[5]).place(x=200, y=80)
        tk.Label(self.root, text="Unit Weapon", compound=tk.LEFT, image=self.images[9]).place(x=200, y=160)
        tk.Label(self.root, text="Unit Life", compound=tk.LEFT, image=self.images[0]).place(x=200, y=240)
        tk.Label(self.root, text="Unit Musou", compound=tk.LEFT, image=self.images[4]).place(x=400, y=0)
        tk.Label(self.root, text="Unit Attack", compound=tk.LEFT, image=self.images[6]).place(x=400, y=80)
        tk.Label(self.root, text="Unit Defense", compound=tk.LEFT, image=self.images[7]).place(x=400, y=160)
        tk.Label(self.root, text="Unit Mounted Value", compound=tk.LEFT, image=self.images[4]).place(x=400, y=240)
        tk.Label(self.root, text="Unit Speed", compound=tk.LEFT, image=self.images[8]).place(x=600, y=0)
        tk.Label(self.root, text="Unit Color", compound=tk.LEFT, image=self.images[10]).place(x=600, y=80)
        tk.Label(self.root, text="Unit AI Type", compound=tk.LEFT, image=self.images[13]).place(x=600, y=160)
        tk.Label(self.root, text="Unit AI Level", compound=tk.LEFT, image=self.images[0]).place(x=600, y=240)
        tk.Label(self.root, text="DW/SW/Orochi Unit?", compound=tk.LEFT, image=self.images[12]).place(x=800, y=0)
        tk.Label(self.root, text="Guard ID", compound=tk.LEFT, image=self.images[11]).place(x=800, y=80)
        tk.Label(self.root, text="Leader ID", compound=tk.LEFT, image=self.images[0]).place(x=800, y=160)
        tk.Label(self.root, text="Unit Type(idk)", compound=tk.LEFT, image=self.images[12]).place(x=800, y=240)

    def gui_entries(self):
        tk.Entry(self.root, textvariable=self.name1, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=0, y=40)
        tk.Entry(self.root, textvariable=self.rank, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=0, y=120)
        tk.Entry(self.root, textvariable=self.voice, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=0, y=200)
        tk.Entry(self.root, textvariable=self.model, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=0, y=280)
        tk.Entry(self.root, textvariable=self.motion, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=200, y=40)
        tk.Entry(self.root, textvariable=self.horse, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=200, y=120)
        tk.Entry(self.root, textvariable=self.weapon1, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=200, y=200)
        tk.Entry(self.root, textvariable=self.life, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=200, y=280)
        tk.Entry(self.root, textvariable=self.musou, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=400, y=40)
        tk.Entry(self.root, textvariable=self.attack, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=400, y=120)
        tk.Entry(self.root, textvariable=self.defense, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=400, y=200)
        tk.Entry(self.root, textvariable=self.mounted, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=400, y=280)
        tk.Entry(self.root, textvariable=self.speed, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=600, y=40)
        tk.Entry(self.root, textvariable=self.colors, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=600, y=120)
        tk.Entry(self.root, textvariable=self.aitype, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=600, y=200)
        tk.Entry(self.root, textvariable=self.ailevel, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=600, y=280)
        tk.Entry(self.root, textvariable=self.multiunit, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=800, y=40)
        tk.Entry(self.root, textvariable=self.guardid, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=800, y=120)
        tk.Entry(self.root, textvariable=self.leaderid, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=800, y=200)
        tk.Entry(self.root, textvariable=self.unittypemaybe, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=800, y=280)
        tk.Button(self.root, text="Submit values to .WO2unit file", command= self.submit_unit, height = 3, width = 30).place(x=30, y=330) # Runs the item writing function
    def open_mod_manager(self):
        manager = WO2Manager(self.root)

class WO2Manager: # mod manager for unit mods
    def __init__(self, root):
        self.root = tk.Toplevel()
        self.root.title("WO2 Mod Manager")
        self.root.iconbitmap(os.path.join(folds[3], "icon2.ico"))
        self.root.minsize(400, 400)
        self.root.resizable(False, False)
        self.mod_status = tk.Label(self.root, text="", fg="green")
        self.mod_status.place(x=10, y=170)
        tk.Button(self.root, text="Enable Mod", command=self.ask_open_file, height=10, width=50).place(x=10, y=10) # button for enabling mods
        tk.Button(self.root, text="Disable Mod", command=self.ask_open_ofile, height=10, width=50).place(x=10, y=210) # button for disabling mods
    def ask_open_file(self): # This is for enabling the user selected mod
        global getoffset
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select mod file",
            filetypes=(
                ("Supported Files", "*.WO2unitmod;"),
            ))
        try:
            if file_path:
                offset = getoffset # offset for unit data in the iso file
                # Apply the mod to the iso file
                with open(file1, "r+b") as f1: # open iso file for reading and writing
                    with open(file_path, "rb") as f2: # open the mod file for reading
                        f1.seek(offset) # seek the offset in the iso file
                        sdata = f2.read(wo2_unitdata[2]) # read the mod file's data
                        f1.write(sdata) # write the mod file's data to the iso file
                self.mod_status.config(text=f"Mod file '{os.path.basename(file_path)}' enabled successfully.", fg="green")
        except Exception as e:
            self.mod_status.config(text=f"Error: {str(e)}", fg="red")
    def ask_open_ofile(self): # For disabling mods
        global getoffset
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select mod file",
            filetypes=(
                ("Supported Files", "*.WO2unit;"),
            ))
        try:
            if file_path:
                offset = getoffset # offset for unit data in the iso file
                # apply the mod disabling file to the iso file
                with open(file1, "r+b") as f1: # open the iso file for reading and writing
                    with open(file_path, "rb") as f2: # open the mod disabling file
                        f1.seek(offset) # seek offset for unit data in the iso file
                        sdata = f2.read(wo2_unitdata[2]) # read the data for disabling unit mods
                        f1.write(sdata) # write the data
                self.mod_status.config(text=f"The mod that used the '{os.path.basename(file_path)}' template was disabled.", fg="green")
        except Exception as e:
            self.mod_status.config(text=f"Error: {str(e)}", fg="red")
            
def main():
    root = tk.Tk()
    orochi = Orochi2(root)
    root.mainloop()
if __name__ == "__main__":
    for f in folds:
        os.makedirs(f, exist_ok = True)
    rem(wo2_unitfiles[0], wo2_unitfiles[1])
    main()
