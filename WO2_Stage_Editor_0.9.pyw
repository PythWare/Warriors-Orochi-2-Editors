import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
import shutil
import os

# list used for files the stage editor and mod manager will use
wo2_files = ["WO2.iso", ".RefS", ".DataS", ".ModS"]
wo2_folders = ["Backups_For_Mod_Disabling", "icons", "WO2_Stages"]
# unit slot count for each stage in wo2_snames which will have 68 items listed in wo2_counts
wo2_counts = [54, 55, 82, 81, 72, 65, 65, 105, 48, 55, 80, 60, 57, 107, 81,
              106, 83, 89, 61, 86, 72, 61, 73, 109, 59, 44, 69, 90, 71, 83,
              96, 109, 74, 51, 65, 96, 92, 97, 88, 107, 98, 107, 83, 61, 59,
              84, 81, 91, 97, 73, 49, 85, 96, 58, 70, 72, 85, 76, 98, 62, 101,
              105, 68, 103, 78, 57, 103, 73]
# offsets for stage data sections with a total of 68 offsets
wo2_soffsets = [0x6CEC2024, 0x6CEC6824, 0x6CECC024, 0x6CED3024, 0x6CED9824, 0x6CEE1024, 0x6CEE9824, 0x6CEF0824,
                0x6CEF9824, 0x6CEFE024, 0x6CF05024, 0x6CF0B024, 0x6CF10024, 0x6CF16024, 0x6CF1D024, 0x6CF25024,
                0x6CF2E024, 0x6CF34024, 0x6CF39824, 0x6CF41824, 0x6CF48024, 0x6CF4F024, 0x6CF54024, 0x6CF5C024,
                0x6CF63824, 0x6CF69824, 0x6CF70824, 0x6CF77024, 0x6CF7E024, 0x6CF84824, 0x6CF8B824, 0x6CF92824,
                0x6CF9B024, 0x6CFA2024, 0x6CFA7824, 0x6CFAD824, 0x6CFB5824, 0x6CFBD024, 0x6CFC5024, 0x6CFCD024,
                0x6CFD5824, 0x6CFDA024, 0x6CFE0824, 0x6CFEA824, 0x6CFF0024, 0x6CFF5824, 0x6CFFB024, 0x6D002024,
                0x6D007824, 0x6D00E824, 0x6D013024, 0x6D018824, 0x6D01F024, 0x6D025824, 0x6D02B024, 0x6D02F824,
                0x6D036024, 0x6D03C824, 0x6D042024, 0x6D049024, 0x6D04E024, 0x6D056024, 0x6D05D024, 0x6D062824,
                0x6D06A824, 0x6D070824, 0x6D074824, 0x6D079824]
# wo2_names holds the 68 stages the user will be able to select
wo2_snames = ["Battle of Shi Ting.RefS", "Battle of Saika.RefS", "Battle of Nagashino battle.RefS",
            "Battle of Wuhang Mountains.RefS", "Battle of Jia Meng Gate.RefS", "Battle of Odani Castle.RefS",
            "Battle of Koshi Castle.RefS", "Battle of Wu Zhang Plains.RefS", "The battle of Si Province.RefS",
            "Battle of Si Shui Gate.RefS", "Battle of Shizugatake.RefS", "Battle of Ji Castle.RefS", "Battle of Komaki-Nagakute.RefS",
            "Battle of Yamatai.RefS", "Battle of Tong Gate.RefS", "Battle of Guan Du.RefS", "The battle of Ru Xu Kou.RefS",
            "Battle of Kanegasaki.RefS", "Battle of Nan Zhong.RefS", "Battle of Itsukushima.RefS", "Battle of Okehazama.RefS", "Battle of Yang Ping Gate.RefS",
            "Battle of Yamazaki.RefS", "Battle of Chi Bi.RefS", "Battle of Lou Sang Village.RefS", "Battle of Ji Province.RefS",
            "Rescue at Hasedo.RefS", "Battle of Chang Ban.RefS", "Battle of Liang Province.RefS", "Battle of Hu Lao Gate.RefS",
            "Battle of Bai Di Castle.RefS", "Battle of Sekigahara.RefS", "Battle of Odawara Castle.RefS", "Battle of Cheng Du.RefS",
            "Battle of Kawanakajima.RefS", "Battle of He Fei.RefS", "Battle of Edo Castle.RefS", "Battle of Yi Ling.RefS", "Battle of Mikatagahara.RefS",
            "Battle of Hinokawa.RefS", "Osaka Castle.RefS", "Fan Castle.RefS", "He Fei Castle.RefS", "Escape from Itsukushima.RefS",
            "Mount Qi.RefS", "Showdown at Odawara Castle.RefS", "Battle of the Wu Territory.RefS", "Showdown in Yamatai.RefS",
            "Jing Province.RefS", "Xin Castle.RefS", "Rescue at Nan Zhong.RefS", "Struggle at Nan Zhong.RefS", "Encounter in Ji Province.RefS", "Battle at Osaka Bay.RefS", "Han Sui.RefS",
            "Ueda Castle.RefS", "Kyushu.RefS", "Honnoji.RefS", "Showdown at Hinokawa.RefS", "Mai Castle.RefS", "Shikoku.RefS", "Xia Pi.RefS", "Chen Cang.RefS",
            "Lu Shan.RefS", "Chang Sha.RefS", "Encounter at Nan Zhong.RefS", "Yan Province.RefS", "Battle of Hasedo.RefS"]
datafiles = [filename.replace(wo2_files[1], wo2_files[2]) for filename in wo2_snames]
# Used for entry error prevention
class TheCheck:
    @staticmethod
    def validate_numeric_input(new_value):
        return new_value == "" or (new_value.replace(".", "", 1).isdigit() and '.' not in new_value and float(new_value) >= 0)
def rem(files1, files2):
    for a in files1:
        filepath1 = os.path.join(wo2_folders[2], a)
        if os.path.isfile(filepath1):
            os.remove(filepath1)
    for b in files2:
        filepath2 = os.path.join(wo2_folders[2], b)
        if os.path.isfile(filepath2):
            os.remove(filepath2)
class StageEditor(TheCheck):
    def __init__(self, root):
        self.files = wo2_files
        self.sreffiles = wo2_snames # for RefS files
        self.sdatafiles = wo2_snames # for DataS files
        self.folders = wo2_folders
        self.stagenames = wo2_snames
        self.root = root
        self.root.title("Warriors Orochi 2 Stage Editor")
        self.root.iconbitmap(os.path.join(self.folders[1], "icon3.ico"))
        self.root.minsize(1160, 500)
        self.root.resizable(False, False)
        self.stage_data_create()
        self.stage_data_ref()
        
        # unit slots are each 32 bytes worth of data
        self.leaderid = tk.IntVar() # 2 bytes
        self.xcord = tk.IntVar() # 2 bytes
        self.ycord = tk.IntVar() # 2 bytes
        self.morale = tk.IntVar() # 2 bytes
        self.side = tk.IntVar() # 2 bytes
        self.performance = tk.IntVar() # 2 bytes
        self.role = tk.IntVar() # 1 byte
        self.direction = tk.IntVar() # 1 byte
        self.squads = tk.IntVar() # 1 byte
        self.target = tk.IntVar() # 1
        self.orders = tk.IntVar() # 1 byte
        self.hide = tk.IntVar() # 1 byte
        self.modname = tk.StringVar()
        tk.Button(self.root, text = "Submit values to DATA file", command = self.submit_stage_values, height=5, width=20).place(x=950,y=200)
        self.mod_manager = tk.Button(self.root, text = "WO2 Mod Manager", command = self.open_mod_manager, height = 5, width = 20)
        self.mod_manager.place(x=950, y=300)
        tk.Button(self.root, text = "Create Stage Mod", command = self.create_stage_mod, width=15).place(x=320,y=10)
        mm1 = tk.Entry(self.root, textvariable = self.modname).place(x=175,y=10)
        mm2 = tk.Label(self.root, text = f"Enter a mod name").place(x=60,y=10)
        self.gui_misc()
        self.stage_labels()
        self.stage_entries()
    def stage_search(self, selected_file, selected_slot): # search the data for unit slots in the .DataS files, this handles unit reading that entries display
        global unknown3
        file_index = wo2_snames.index(selected_file)
        new_select = os.path.join(self.folders[2], selected_file) # RefS file
        new_read = os.path.join(self.folders[2], datafiles[file_index]) # DataS file
        with open(new_select, "rb") as r1: # .ref file
            useroffset = selected_slot
            uservalue = selected_slot * 8
            r1.seek(uservalue)
            getoffset = int.from_bytes(r1.read(8), "little")
            with open(new_read, "rb") as f1: # .data file
                f1.seek(getoffset)
                slotoffset = f1.tell()
                unitleaderid = int.from_bytes(f1.read(2), "little")
                x = int.from_bytes(f1.read(2), "little")
                y = int.from_bytes(f1.read(2), "little")
                unitmorale = int.from_bytes(f1.read(2), "little")
                unitside = int.from_bytes(f1.read(2), "little")
                unitperformance = int.from_bytes(f1.read(2), "little")
                unitgroup = int.from_bytes(f1.read(1), "little")
                self.unk2 = f1.read(1)
                unitdirection = int.from_bytes(f1.read(1), "little")
                squadcount = int.from_bytes(f1.read(1), "little")
                unittarget = int.from_bytes(f1.read(1), "little")
                unitorder = int.from_bytes(f1.read(1), "little")
                hiding = int.from_bytes(f1.read(1), "little")
                self.unknown3 = f1.read(1)
                self.unknown4 = f1.read(12)
                
                self.leaderid.set(unitleaderid)
                self.xcord.set(x)
                self.ycord.set(y)
                self.morale.set(unitmorale)
                self.side.set(unitside)
                self.performance.set(unitperformance)
                self.role.set(unitgroup)
                self.direction.set(unitdirection)
                self.squads.set(squadcount)
                self.target.set(unittarget)
                self.orders.set(unitorder)
                self.hide.set(hiding)
                
    def stage_data_create(self): # make the .DataS files to store 32 byte unit slot data
        with open(self.files[0], "rb") as f1: # the main file to obtain references from
            for i in range(len(wo2_snames)):
                if not os.path.isfile(os.path.join(self.folders[2], datafiles[i])):
                    with open(os.path.join(self.folders[2], datafiles[i]), "ab") as f2: # create the filename
                        f1.seek(wo2_soffsets[i]) # seek each offset
                        keep_offset = f1.tell()
                        for j in range(0, wo2_counts[i]): # read 32 chunks of data
                            offset = f1.tell()
                            sdata = f1.read(32)
                            f2.write(sdata)
                        f2.write(keep_offset.to_bytes(4, "little"))
                else:
                    pass
        self.check_backup1()
    def stage_data_ref(self): # make the .RefS files store offsets for each slot in the .DataS files
        for i in range(len(wo2_snames)):
            with open(os.path.join(self.folders[2], datafiles[i]), "rb") as f_data:  # Open the .DataS file for reading
                if not os.path.isfile(os.path.join(self.folders[2], wo2_snames[i])):
                    with open(os.path.join(self.folders[2], wo2_snames[i]), "ab") as f_ref:  # Open the corresponding .ref file for writing
                        offset = 0  # Initialize offset counter
                        while True:
                            data_chunk = f_data.read(32)  # Read a 32-byte chunk from .data file
                            if not data_chunk:  # Break loop if end of file is reached
                                break
                            f_ref.write(offset.to_bytes(8, "little"))  # Write the offset to the .ref file
                            offset += 32  # Move offset to the next chunk
                else:
                    pass
        self.check_backup2()
    def stage_labels(self):
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.place(x=400, y=400)
        self.info_label = tk.Label(self.root, text="""This Editor allows you to mod the units in the Stage data. More features will be added. For Unit role the value 0 is commander, 2 is playable officer, 3 is NPC officer, and 5 is troop role.""").place(x=20, y=450)
        tk.Label(self.root, text="Unit Leader ID").place(x=60, y=100)
        tk.Label(self.root, text="X Coordinate(for spawning)").place(x=60, y=180)
        tk.Label(self.root, text="Y Coordinate(for spawning)").place(x=280, y=100)
        tk.Label(self.root, text="Unit Morale").place(x=280, y=180)
        tk.Label(self.root, text="The side the unit fights for").place(x=500, y=100)
        tk.Label(self.root, text="AI Performance(affects aggressiveness)").place(x=500, y=180)
        tk.Label(self.root, text="Unit Role").place(x=720, y=100)
        tk.Label(self.root, text="The direction the unit is facing").place(x=720, y=180)
        tk.Label(self.root, text="Squads spawned with the unit").place(x=60, y=260)
        tk.Label(self.root, text="Unit Target").place(x=280, y=260)
        tk.Label(self.root, text="Unit Orders").place(x=500, y=260)
        tk.Label(self.root, text="Hide(1 for hide and 0 for unhide)").place(x=720, y=260)
    def stage_entries(self):
        tk.Entry(self.root, textvariable=self.leaderid, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=60, y=140)
        tk.Entry(self.root, textvariable=self.xcord, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=60, y=220)
        tk.Entry(self.root, textvariable=self.ycord, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=280, y=140)
        tk.Entry(self.root, textvariable=self.morale, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=280, y=220)
        tk.Entry(self.root, textvariable=self.side, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=500, y=140)
        tk.Entry(self.root, textvariable=self.performance, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=500, y=220)
        tk.Entry(self.root, textvariable=self.role, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=720, y=140)
        tk.Entry(self.root, textvariable=self.direction, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=720, y=220)
        tk.Entry(self.root, textvariable=self.squads, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=60, y=300)
        tk.Entry(self.root, textvariable=self.target, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=280, y=300)
        tk.Entry(self.root, textvariable=self.orders, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=500, y=300)
        tk.Entry(self.root, textvariable=self.hide, validate="key", validatecommand=(self.root.register(self.validate_numeric_input), "%P")).place(x=720, y=300)
    def gui_misc(self):
        # Create dropdown menu for selecting stage file
        self.selected_file = tk.StringVar(self.root)
        self.selected_file.set(self.stagenames[0])  # Default value
        file_combobox = ttk.Combobox(self.root, textvariable=self.selected_file, values=self.sreffiles, width = 30)
        file_combobox.bind("<<ComboboxSelected>>", self.stage_search_on_map_change)
        file_combobox.place(x=900, y=10)
        tk.Label(self.root, text="Stage to modify").place(x=780, y=10)
        # Create dropdown menu for selecting unit slot
        self.selected_slot = tk.IntVar(self.root)
        self.selected_slot.set(0)  # Default value
        self.slot_combobox = ttk.Combobox(self.root, textvariable=self.selected_slot, values=list(range(54)))
        self.slot_combobox.bind("<<ComboboxSelected>>", self.slot_selected)
        self.slot_combobox.place(x=600, y=10)
        tk.Label(self.root, text="Unit Slot To Modify").place(x=480, y=10)
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.place(x=480, y=200)
    def submit_stage_values(self): # write the data on each click to the template files
        file_index = wo2_snames.index(self.selected_file.get())
        new_reader = os.path.join(wo2_folders[2], self.selected_file.get()) # for the RefS files
        new_writer = os.path.join(wo2_folders[2], datafiles[file_index]) # for the DataS files
        try:
            collectit = [self.leaderid.get().to_bytes(2, "little"), self.xcord.get().to_bytes(2, "little"), self.ycord.get().to_bytes(2, "little"),
                         self.morale.get().to_bytes(2, "little"), self.side.get().to_bytes(2, "little"), self.performance.get().to_bytes(2, "little"),
                         self.role.get().to_bytes(1, "little"), self.unk2, self.direction.get().to_bytes(1, "little"), self.squads.get().to_bytes(1, "little"),
                         self.target.get().to_bytes(1, "little"), self.orders.get().to_bytes(1, "little"), self.hide.get().to_bytes(1, "little"), self.unknown3,
                         self.unknown4]
            selected_slot = self.selected_slot.get()
            with open(new_reader, "r+b") as r1: # for obtaining the offset for a unit slot from the .RefS file
                useroffset = selected_slot
                uservalue = selected_slot * 8
                r1.seek(uservalue)
                getoffset = int.from_bytes(r1.read(8), "little")
                with open(new_writer, "r+b") as f1: # for updating the unit slot with the current values from collectit
                    f1.seek(getoffset)
                    for b in collectit:
                        f1.write(b)
            self.status_label.config(text=f"Values submitted without issues.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error with entries: {str(e)}", fg="red")
    def create_stage_mod(self): # for creating a mod file with custom extension
        sep = "." # to be used for correcting
        file_index = self.sreffiles.index(self.selected_file.get()) # get the current selected .RefS file
        new_reader = os.path.join(self.folders[2], datafiles[file_index]) # get the .DataS file that is in the same list position as the .RefS files
        try:
            usermodname = self.modname.get().split(sep, 1)[0] + self.files[3]
            with open(new_reader, "rb") as r1:
                data = r1.read()
                with open(usermodname, "wb") as w1:
                    w1.write(data)
            self.status_label.config(text=f"Mod file '{usermodname}' created successfully.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error creating mod file '{usermodname}': {str(e)}", fg="red")

    def check_backup1(self): # Create backups of the .DataS files
        for file in datafiles: # .DataS filename list
            try_file = os.path.join(self.folders[2], file)
            backup_file = os.path.join(self.folders[0], file)
            if not os.path.exists(backup_file):
                shutil.copy(try_file, backup_file)
            else:
                pass
    def check_backup2(self): # create backups of .RefS files
        for ofile in wo2_snames: # .RefS filename list
            otry_file = os.path.join(self.folders[2], ofile)
            obackup_file = os.path.join(self.folders[0], ofile)
            if not os.path.exists(obackup_file):
                shutil.copy(otry_file, obackup_file)
            else:
                pass
    def stage_search_on_map_change(self, event=None): # for when user chooses a map or slot
        selected_file_value = self.selected_file.get()
        selected_slot_value = self.selected_slot.get()
        self.index = wo2_snames.index(selected_file_value)
        self.rang = wo2_counts[self.index]
        self.slot_combobox.config(values = list(range(self.rang)))
        self.stage_search(selected_file_value, selected_slot_value)
    
    def slot_selected(self, event=None): # update display data
        selected_file_value = self.selected_file.get()
        selected_slot_value = self.selected_slot.get()
        self.stage_search(selected_file_value, selected_slot_value)
    def open_mod_manager(self):
        manager = WO2Manager(self.root)
        
class WO2Manager: # mod manager for unit mods
    def __init__(self, root):
        self.root = tk.Toplevel()
        self.root.title("WO2 Mod Manager")
        self.root.iconbitmap(os.path.join(wo2_folders[1], "icon2.ico"))
        self.root.minsize(400, 400)
        self.root.resizable(False, False)
        self.mod_status = tk.Label(self.root, text="", fg="green")
        self.mod_status.place(x=10, y=170)
        tk.Button(self.root, text="Enable Mod", command=self.ask_open_file, height=10, width=50).place(x=10, y=10) # button for enabling mods
        tk.Button(self.root, text="Disable Mod", command=self.ask_open_ofile, height=10, width=50).place(x=10, y=210) # button for disabling mods
    def ask_open_file(self): # This is for enabling the user selected mod
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select mod file",
            filetypes=(
                ("Supported Files", "*.ModS;"),
            ))
        try:
            if file_path:
                check_size1 = os.path.getsize(file_path)
                offset_size1 = check_size1 - 4
                # Apply the mod to the iso file
                with open(wo2_files[0], "r+b") as f1: # open iso file for reading and writing
                    with open(file_path, "rb") as f2: # open the mod file for reading
                        f2.seek(offset_size1)
                        offset = int.from_bytes(f2.read(4), "little")
                        f1.seek(offset) # seek the offset in the iso file
                        f2.seek(0)
                        sdata = f2.read(offset_size1) # read the mod file's data
                        f1.write(sdata) # write the mod file's data to the iso file
                self.mod_status.config(text=f"Mod file '{os.path.basename(file_path)}' enabled successfully.", fg="green")
        except Exception as e:
            self.mod_status.config(text=f"Error: {str(e)}", fg="red")
    def ask_open_ofile(self): # For disabling mods
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select mod file",
            filetypes=(
                ("Supported Files", "*.DataS;"),
            ))
        try:
            if file_path:
                check_size2 = os.path.getsize(file_path)
                offset_size2 = check_size2 - 4
                # apply the disabling file to the iso file
                with open(wo2_files[0], "r+b") as f1: # open the iso file for reading and writing
                    with open(file_path, "rb") as f2: # open the mod disabling file
                        f2.seek(offset_size2)
                        offset = int.from_bytes(f2.read(4), "little")
                        f1.seek(offset) # seek offset for stage data in the iso file
                        f2.seek(0)
                        sdata = f2.read(offset_size2) # read the data for disabling stage mods
                        f1.write(sdata) # write the data
                self.mod_status.config(text=f"The mod that used the '{os.path.basename(file_path)}' template was disabled.", fg="green")
        except Exception as e:
            self.mod_status.config(text=f"Error: {str(e)}", fg="red")
def runner():
    root = tk.Tk()
    stage = StageEditor(root)
    root.mainloop()
if __name__=="__main__":
    for f in wo2_folders:
        os.makedirs(f, exist_ok = True)
    rem(wo2_snames, datafiles)
    runner()
