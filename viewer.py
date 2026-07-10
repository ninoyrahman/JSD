# Youtube Link: https://www.youtube.com/watch?v=PgLjwl6Br0k

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd
from jsd import jsd

class viewer():

    def __init__(self, source=None):

        # initialize jsd
        self.db = jsd()
        self.crop_name = 'All'
        self.maturity_day = 'All'
        self.crop_type = 'All'
        self.brand_name = 'All'
        self.weather_tolerance = 'All'
        self.transport_property = 'All'

        crop_names = ['All', 'Bitter Gourd', 'Bottle Gourd', 'Broccoli', 'Cabbage', 'Capsicum', 
                    'Carrot', 'Cauliflower', 'Chinese Cabbage', 'Chinese Radish', 'Cucumber', 
                    'Eggplant', 'Hot Pepper', 'Kohlrabi', 'Lettuce', 'Loofah', 'Marigold', 
                    'Melon', 'Okra', 'Pakchoi', 'Papaya', 'Pumpkin', 'Radish', 'Red Cabbage', 
                    'Ridge Gourd', 'Snake Gourd', 'Sponge Gourd', 'Sweet Corn', 'Tomato', 
                    'Watermelon', 'Wax Gourd', 'Yard Long Bean']
        maturity_days = ['All', 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
        crop_types = ['All', 'Hybrid', 'OP']
        brand_names = ['All', 'Zillion', 'Chia Tai']
        weather_tolerances = ['All', 'Rain', 'Heat', 'Rain & heat']
        transport_properties = ['All', 'Good']

        # initalise the tkinter GUI
        self.root = tk.Tk()

        self.root.geometry("1080x720") # set the root dimensions
        self.root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
        self.root.resizable(0, 0) # makes the root window fixed in size.

        # Frame for Dropdown
        dropdown_frame = tk.LabelFrame(self.root, text="Select")
        dropdown_frame.place(height=80, width=1070, rely=0.01, relx=0)

        # Combobox
        label_1 = tk.Label(dropdown_frame, text="Crop")
        label_1.place(rely=0.25, relx=0.005)
        self.current_var_1 = tk.StringVar()
        combobox_1 = ttk.Combobox(dropdown_frame, values=crop_names, textvariable=self.current_var_1)
        combobox_1.place(rely=0.25, relx=0.04, width=120)
        combobox_1.set('All')

        label_2 = tk.Label(dropdown_frame, text="Maturity")
        label_2.place(rely=0.25, relx=0.16)
        self.current_var_2 = tk.StringVar()
        combobox_2 = ttk.Combobox(dropdown_frame, values=maturity_days, textvariable=self.current_var_2)
        combobox_2.place(rely=0.25, relx=0.21, width=110)
        combobox_2.set('All')

        label_3 = tk.Label(dropdown_frame, text="Type")
        label_3.place(rely=0.25, relx=0.32)
        self.current_var_3 = tk.StringVar()
        combobox_3 = ttk.Combobox(dropdown_frame, values=crop_types, textvariable=self.current_var_3)
        combobox_3.place(rely=0.25, relx=0.35, width=110)
        combobox_3.set('All')

        label_4 = tk.Label(dropdown_frame, text="Brand")
        label_4.place(rely=0.25, relx=0.46)
        self.current_var_4 = tk.StringVar()
        combobox_4 = ttk.Combobox(dropdown_frame, values=brand_names, textvariable=self.current_var_4)
        combobox_4.place(rely=0.25, relx=0.495, width=110)
        combobox_4.set('All')

        label_5 = tk.Label(dropdown_frame, text="Weather")
        label_5.place(rely=0.25, relx=0.605)
        self.current_var_5 = tk.StringVar()
        combobox_5 = ttk.Combobox(dropdown_frame, values=weather_tolerances, textvariable=self.current_var_5)
        combobox_5.place(rely=0.25, relx=0.655, width=110)
        combobox_5.set('All')

        label_6 = tk.Label(dropdown_frame, text="Transport")
        label_6.place(rely=0.25, relx=0.765)
        self.current_var_6 = tk.StringVar()
        combobox_6 = ttk.Combobox(dropdown_frame, values=transport_properties, textvariable=self.current_var_6)
        combobox_6.place(rely=0.25, relx=0.82, width=110)
        combobox_6.set('All')

        # Buttons
        button_1 = tk.Button(dropdown_frame, text="Refresh", command=lambda: self.Refresh())
        button_1.place(rely=0.00, relx=0.95, width=50)

        button_2 = tk.Button(dropdown_frame, text="Reset", command=lambda: self.Reset())
        button_2.place(rely=0.52, relx=0.95, width=50)

        # Frame for open file dialog
        file_frame = tk.LabelFrame(self.root, text="Open File")
        file_frame.place(height=60, width=400, rely=0.9, relx=0)

        # Buttons
        button1 = tk.Button(file_frame, text="Browse A File", command=lambda: self.File_dialog())
        button1.place(rely=0.3, relx=0.40)

        # The file/file path text
        self.label_file = ttk.Label(file_frame, text="No File Selected")
        self.label_file.place(rely=0, relx=0)

        # Frame for TreeView
        frame1 = tk.LabelFrame(self.root, text="Excel Data")
        frame1.place(height=540, width=1070, rely=0.15, relx=0)

        ## Treeview Widget
        self.tv1 = ttk.Treeview(frame1)
        self.tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(frame1, orient="vertical", command=self.tv1.yview) # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=self.tv1.xview) # command means update the xaxis view of the widget
        self.tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget


    def File_dialog(self):
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        filename = filedialog.askopenfilename(initialdir="/",
                                            title="Select A File",
                                            filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
        self.label_file["text"] = filename
        self.Load_excel_data()
        return None

    def Show_data(self, df):
        self.clear_data()
        self.tv1["column"] = list(df.columns)
        self.tv1["show"] = "headings"
        for column in self.tv1["columns"]:
            self.tv1.heading(column, text=column) # let the column heading = column name

        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            self.tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        return None

    def Load_excel_data(self):
        """If the file selected is valid this will load the file into the Treeview"""
        file_path = self.label_file["text"]
        try:
            excel_filename = r"{}".format(file_path)
            if excel_filename[-4:] == ".csv":
                self.db.set_dataframe(excel_filename)
                df = self.db.dataframe
            else:
                self.db.set_dataframe(excel_filename)
                df = self.db.dataframe

        except ValueError:
            tk.messagebox.showerror("Information", "The file you have chosen is invalid")
            return None
        except FileNotFoundError:
            tk.messagebox.showerror("Information", f"No such file as {file_path}")
            return None

        self.Show_data(df)
        return None

    def Reset(self):
        self.current_var_1.set('All')
        self.current_var_2.set('All')
        self.current_var_3.set('All')
        self.current_var_4.set('All')
        self.current_var_5.set('All')
        self.current_var_6.set('All')
        self.Refresh()

    def Refresh(self):
        try:
            self.crop_name = self.current_var_1.get()
            self.maturity_day = self.current_var_2.get()
            self.crop_type = self.current_var_3.get()
            self.brand_name = self.current_var_4.get()
            self.weather_tolerance = self.current_var_5.get()
            self.transport_property = self.current_var_6.get()

            variety_list = self.db.generate_list(self.crop_name, self.maturity_day, self.crop_type, self.brand_name, self.weather_tolerance, self.transport_property)
            df = pd.DataFrame(self.db.dataframe[variety_list])
            self.Show_data(df)
        except:
            tk.messagebox.showerror("Information", "File not selected")
            return None
        return None

    def clear_data(self):
        self.tv1.delete(*self.tv1.get_children())
        return None

    def run(self):
        self.root.mainloop()