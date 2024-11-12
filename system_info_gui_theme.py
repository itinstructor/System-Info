#!/usr/bin/env python3
"""
    Name: system_info_gui_theme.py
    Author: William A Loring
    Created: 07/31/22
    Purpose: Display psutil info with Tkinter
"""
# pip install sv-ttk
import sv_ttk
# Import the tkinter module with tk standard widgets
import tkinter as tk
# Override tk widgets with themed ttk widgets if available
from tkinter import ttk
import psutil


class SystemInfo:

    def __init__(self):
        self.sent_1 = 0
        self.recv_1 = 0
        self.sent_2 = 0
        self.recv_2 = 0

        self.root = tk.Tk()
        # self.root.title("System Info")
        self.root.geometry("+100+100")
        self.root.iconbitmap("airplay.ico")
        self.root.resizable(False, False)
        # Create transparent window
        self.root.attributes('-alpha', 0.9)
        # Set the theme you want with the set_theme procedure
        sv_ttk.set_theme("dark")
        self.root.overrideredirect(True)

        # Call method to create all the widgets
        self.create_widgets()
        self.get_cpu_info()
        # Start GUI
        self.root.mainloop()

# --------------------------- GET CPU INFO --------------------------------#
    def get_cpu_info(self):
        # Get current network io statistics in Kbps
        self.sent_2 = self.sent_1
        self.recv_2 = self.recv_1
        self.sent_1, self.recv_1 = self.get_network_io()

        # Subtract first reading from second reading
        # gives us how many kilobits were sent/recv per second
        sent = self.sent_1 - self.sent_2
        recv = self.recv_1 - self.recv_2

        # Get information
        cpu_count = psutil.cpu_count(logical=False)
        logical_cpu_count = psutil.cpu_count()
        cpu_useage_pct = psutil.cpu_percent(interval=None)
        # CPU frequence in Mhz, convert to Ghz
        cpu_frequency = psutil.cpu_freq().current / 1024
        # RAM total in bytes, convert to GB
        ram_total = psutil.virtual_memory().total / 1024 / 1024 / 1024
        # RAM useage in bytes, convert to GB
        ram_useage = int(
            psutil.virtual_memory().total -
            psutil.virtual_memory().available) / 1024 / 1024 / 1024
        ram_useage_pct = psutil.virtual_memory().percent

        # Display CPU info
        self.cpu_label_value.configure(text=f" {cpu_count}")
        self.logical_cpu_label_value.configure(text=f" {logical_cpu_count}")
        self.cpu_percent_label_value.configure(text=f" {cpu_useage_pct} %")
        self.cpu_frequency_label_value.configure(
            text=f" {cpu_frequency:,.2f} Ghz")

        # Display RAM info
        self.ram_total_label_value.configure(
            text=f" {ram_total:,.2f} GB")
        self.ram_useage_label_value.configure(
            text=f" {ram_useage:,.2f} GB")
        self.ram_useage_pct_label_value.configure(
            text=f" {ram_useage_pct} %")

        # Display Network IO
        self.net_sent_label_value.configure(
            text=f" {sent:,.1f} Kbps")
        self.net_recv_label_value.configure(
            text=f" {recv:,.1f} Kbps")

        # Schedule after in 1 second
        self.root.after(1000, self.get_cpu_info)

# ------------------------- GET NETWORK IO --------------------------------#
    def get_network_io(self):
        """Get current net io counters statistics in bytes
            convert to bits, then kb
        """
        sent = psutil.net_io_counters().bytes_sent
        recv = psutil.net_io_counters().bytes_recv
        # Convert bytes to bits *8, convert bits to kilobits / 1024
        sent = (sent * 8) / 1024
        recv = (recv * 8) / 1024

        return sent, recv

# ------------------------- CREATE WIDGETS --------------------------------#
    def create_widgets(self):
        self.main_frame = ttk.LabelFrame(
            self.root,
            text="System Info",
            relief=tk.GROOVE
        )

        # Fill the frame to the width of the window
        self.main_frame.pack(fill=tk.X)

        # Keep the frame size regardless of the widget sizes
        self.main_frame.pack_propagate(False)

        self.cpu_label = tk.Label(
            self.main_frame,
            text="CPU:"
        )
        self.cpu_label_value = tk.Label(
            self.main_frame,
            anchor=tk.W,
            width=15,
            relief=tk.GROOVE
        )

        self.logical_cpu_label = tk.Label(
            self.main_frame,
            text="Logical CPU:"
        )
        self.logical_cpu_label_value = tk.Label(
            self.main_frame,
            anchor=tk.W,
            width=15,
            relief=tk.GROOVE
        )

        self.cpu_percent_label = tk.Label(
            self.main_frame,
            text="CPU useage:"
        )
        self.cpu_percent_label_value = tk.Label(
            self.main_frame,
            anchor=tk.W,
            width=15,
            relief=tk.GROOVE
        )

        self.cpu_frequency_label = tk.Label(
            self.main_frame,
            text="CPU frequency:"
        )
        self.cpu_frequency_label_value = tk.Label(
            self.main_frame,
            anchor=tk.W,
            width=15,
            relief=tk.GROOVE
        )

        self.ram_total_label = tk.Label(
            self.main_frame,
            text="RAM total:"
        )
        self.ram_total_label_value = tk.Label(
            self.main_frame,
            anchor=tk.W,
            width=15,
            relief=tk.GROOVE
        )

        self.ram_useage_label = tk.Label(
            self.main_frame,
            text="RAM useage:"
        )
        self.ram_useage_label_value = tk.Label(
            self.main_frame,
            anchor=tk.W,
            width=15,
            relief=tk.GROOVE
        )

        self.ram_useage_pct_label = tk.Label(
            self.main_frame,
            text="RAM useage pct:"
        )
        self.ram_useage_pct_label_value = tk.Label(
            self.main_frame,
            anchor=tk.W,
            width=15,
            relief=tk.GROOVE
        )

        self.net_sent_label = tk.Label(
            self.main_frame,
            text="Net IO sent:"
        )
        self.net_sent_label_value = tk.Label(
            self.main_frame,
            anchor=tk.W,
            width=15,
            relief=tk.GROOVE
        )

        self.net_recv_label = tk.Label(
            self.main_frame,
            text="Net IO recv:"
        )
        self.net_recv_label_value = tk.Label(
            self.main_frame,
            anchor=tk.W,
            width=15,
            relief=tk.GROOVE
        )

        # Grid Spin labelframe
        self.cpu_label.grid(row=0, column=0, sticky=tk.E)
        self.cpu_label_value.grid(row=0, column=1)
        self.logical_cpu_label.grid(row=1, column=0, sticky=tk.E)
        self.logical_cpu_label_value.grid(row=1, column=1)
        self.cpu_percent_label.grid(row=2, column=0, sticky=tk.E)
        self.cpu_percent_label_value.grid(row=2, column=1)
        self.cpu_frequency_label.grid(row=3, column=0, sticky=tk.E)
        self.cpu_frequency_label_value.grid(row=3, column=1)
        self.ram_total_label.grid(row=4, column=0, sticky=tk.E)
        self.ram_total_label_value.grid(row=4, column=1)
        self.ram_useage_label.grid(row=5, column=0, sticky=tk.E)
        self.ram_useage_label_value.grid(row=5, column=1)
        self.ram_useage_pct_label.grid(row=6, column=0, sticky=tk.E)
        self.ram_useage_pct_label_value.grid(row=6, column=1)

        self.net_sent_label.grid(row=7, column=0, sticky=tk.E)
        self.net_sent_label_value.grid(row=7, column=1)
        self.net_recv_label.grid(row=8, column=0, sticky=tk.E)
        self.net_recv_label_value.grid(row=8, column=1)

        # Set padding between frame and window
        self.main_frame.pack_configure(padx=20, pady=20)

        # Set padding for all widgets
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Set keyboard and mouse actions
        self.root.bind('<Escape>', self.quit)
        self.root.bind('<Button-1>', self.save_click_pos)
        self.root.bind('<B1-Motion>', self.drag_window)

# --------------------- SAVE MOUSE CLICK POSITION -------------------------#
    def save_click_pos(self, event):
        self.last_click_x = event.x
        self.last_click_y = event.y

# ----------------------------- DRAG WINDOW -------------------------------#
    def drag_window(self, event):
        x = event.x - self.last_click_x + self.root.winfo_x()
        y = event.y - self.last_click_y + self.root.winfo_y()
        # Set geometry, move window
        self.root.geometry(f"+{x}+{y}")

# ----------------------------- QUIT PROGRAM ------------------------------#
    def quit(self, *args):
        self.root.destroy()


# -------------------------- RUN PROGRAM ----------------------------------#
"""Create program object to start the program"""
system_info = SystemInfo()
