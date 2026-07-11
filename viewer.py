# Youtube Link: https://www.youtube.com/watch?v=PgLjwl6Br0k

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import calendar

import pandas as pd
from jsd import jsd

class viewer():
    """
    A Tkinter GUI application for browsing and filtering crop variety data.

    This class builds a window with dropdown menus for various filters (crop,
    maturity, type, brand, weather tolerance, month) and a Treeview widget to
    display the filtered data from an Excel/CSV file. It relies on the `jsd`
    class to handle data loading and querying.

    Attributes:
        db (jsd): The underlying data manager instance.
        crop_name (str): Current filter value for crop.
        maturity_day (str): Current filter value for maturity days.
        crop_type (str): Current filter value for type (Hybrid/OP).
        brand_name (str): Current filter value for brand.
        weather_tolerance (str): Current filter value for weather tolerance.
        month (str): Current filter value for cultivation month.
        root (tk.Tk): The main Tkinter window.
        tv1 (ttk.Treeview): The treeview widget displaying the data.
        label_file (ttk.Label): Label showing the selected file path.
        current_var_1..6 (tk.StringVar): Variables linked to each combobox.
    """
    def __init__(self, source=None):
        """
        Initialize the GUI and set up all widgets.

        Args:
            source (optional): Not used; kept for compatibility.
        """
        # initialize jsd
        self.db = jsd()
        self.crop_name = 'All'
        self.maturity_day = 'All'
        self.crop_type = 'All'
        self.brand_name = 'All'
        self.weather_tolerance = 'All'
        # self.transport_property = 'All'
        self.month = 'All'

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
        # transport_properties = ['All', 'Good']
        months = calendar.month_name[1:]
        months.insert(0, 'All')

        # initalise the tkinter GUI
        self.root = tk.Tk()

        self.root.geometry("1080x720") # set the root dimensions
        self.root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
        self.root.resizable(True, True)  # makes the root window resizible.
        # self.root.resizable(0, 0) # makes the root window fixed in size.

        # Frame for Dropdown
        dropdown_frame = tk.LabelFrame(self.root, text="Select", height=80, width=1070)

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

        label_6 = tk.Label(dropdown_frame, text="Month")
        label_6.place(rely=0.25, relx=0.765)
        self.current_var_6 = tk.StringVar()
        combobox_6 = ttk.Combobox(dropdown_frame, values=months, textvariable=self.current_var_6)
        combobox_6.place(rely=0.25, relx=0.82, width=110)
        combobox_6.set('All')

        # Buttons
        button_1 = tk.Button(dropdown_frame, text="Refresh", command=lambda: self.Refresh())
        button_1.place(rely=0.00, relx=0.95, width=50)

        button_2 = tk.Button(dropdown_frame, text="Reset", command=lambda: self.Reset())
        button_2.place(rely=0.52, relx=0.95, width=50)

        # Frame for TreeView
        frame1 = tk.LabelFrame(self.root, text="Excel Data", height=540, width=1070)

        ## Treeview Widget
        self.tv1 = ttk.Treeview(frame1)
        self.tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(frame1, orient="vertical", command=self.tv1.yview) # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=self.tv1.xview) # command means update the xaxis view of the widget
        self.tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

        # Frame for open file dialog
        file_frame = tk.LabelFrame(self.root, text="Open File", height=80, width=400)

        # The file/file path text
        self.label_file = ttk.Label(file_frame, text="No File Selected")
        self.label_file.place(rely=0, relx=0)

        # Buttons
        button1 = tk.Button(file_frame, text="Browse A File", command=lambda: self.File_dialog())
        button1.place(rely=0.4, relx=0.40)

        dropdown_frame.pack(expand=False, padx=10, pady=10, anchor=tk.NW)
        frame1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        file_frame.pack(expand=False, padx=10, pady=10, anchor=tk.SW)


    def File_dialog(self):
        """
        Open a file dialog to select an Excel or CSV file.

        Updates the label with the chosen file path and then loads the data.
        """
        filename = filedialog.askopenfilename(initialdir="/",
                                            title="Select A File",
                                            filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
        self.label_file["text"] = filename
        self.Load_excel_data()
        return None

    def Show_data(self, df):
        """
        Display a pandas DataFrame in the treeview widget.

        The method clears any existing data, sets up the columns, and inserts
        each row with alternating row colors for readability.

        Args:
            df (pd.DataFrame): The data to display.
        """
        self.clear_data()
        self.tv1["column"] = list(df.columns)
        self.tv1["show"] = "headings"
        for column in self.tv1["columns"]:
            self.tv1.heading(column, text=column) # let the column heading = column name

        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
        tags = ['even', 'odd']
        idx = -1
        for row in df_rows:
            idx += 1
            self.tv1.insert("", "end", values=row, tags=(tags[idx%2],)) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

        self.tv1.tag_configure('even', foreground='black', background='white')
        self.tv1.tag_configure('odd', foreground='black', background='gray75')
        return None

    def Load_excel_data(self):
        """
        Load the selected file into the jsd data manager.

        If the file is valid (Excel or CSV), it sets the DataFrame in `self.db`
        and displays it. Shows an error message on failure.
        """
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
        """
        Reset all filter comboboxes to 'All' and refresh the display.
        """
        self.current_var_1.set('All')
        self.current_var_2.set('All')
        self.current_var_3.set('All')
        self.current_var_4.set('All')
        self.current_var_5.set('All')
        self.current_var_6.set('All')
        self.Refresh()

    def Refresh(self):
        """
        Apply the current filter selections and update the treeview.

        Retrieves the values from the comboboxes, calls `generate_list` on the
        jsd object to get a boolean mask, filters the DataFrame, and displays
        the result. Shows an error if no file is loaded or if something goes wrong.
        """
        try:
            self.crop_name = self.current_var_1.get()
            self.maturity_day = self.current_var_2.get()
            self.crop_type = self.current_var_3.get()
            self.brand_name = self.current_var_4.get()
            self.weather_tolerance = self.current_var_5.get()
            self.month = self.current_var_6.get()

            variety_list = self.db.generate_list(self.crop_name, self.maturity_day, self.crop_type, self.brand_name, self.weather_tolerance, self.month)
            df = pd.DataFrame(self.db.dataframe[variety_list])
            self.Show_data(df)
        except:
            tk.messagebox.showerror("Information", "File not selected")
            return None
        return None

    def clear_data(self):
        """
        Remove all rows from the treeview.
        """
        self.tv1.delete(*self.tv1.get_children())
        return None

    def run(self):
        """
        Start the Tkinter main event loop.
        """
        self.root.mainloop()