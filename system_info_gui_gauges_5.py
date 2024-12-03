#!/usr/bin/env python3
"""
    Name: system_info_gauges_5.py
    Author: William A Loring
    Created: 09-18-21 Revised:
    Purpose: Test program with functions for monitoring CPU
    and RAM usage in Python with PsUtil.
"""
import psutil
import threading
import tkinter as tk
import tkinter.ttk as ttk


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x170")
        self.root.title("System Info")
        self.create_widgets()
        self.root.iconbitmap("airplay.ico")

        # Initialize initial network usage counters
        net_io = psutil.net_io_counters()
        self.initial_bytes_sent = net_io.bytes_sent
        self.initial_bytes_recv = net_io.bytes_recv

# -------------------------- UPDATE PROGRESS BARS ------------------------ #
    def update_progressbars(self):
        """
        Updates the CPU, memory, and disk usage progress bars and their labels.

        This method retrieves the current CPU, memory, and disk usage statistics
        and updates the associated progress bars and text labels in the UI.
        This method is called every 1000 milliseconds to provide real-time updates.
        """

        # Get current CPU usage percentage
        cpu_percent = psutil.cpu_percent()

        # Get current memory usage percentage
        memory_percent = psutil.virtual_memory().percent

        # Get current disk usage percentage for the root directory
        disk_percent = psutil.disk_usage('/').percent

        # Calculate total and used memory in gigabytes, rounded to two decimal places
        memory_total = round(psutil.virtual_memory().total / (1024.0 ** 3), 2)
        memory_used = round(psutil.virtual_memory().used / (1024.0 ** 3), 2)

        # Calculate total and used disk space in gigabytes, rounded to two decimal places
        disk_total = round(psutil.disk_usage('/').total / (1024.0 ** 3), 2)
        disk_used = round(psutil.disk_usage('/').used / (1024.0 ** 3), 2)

        # Update CPU progress bar with current CPU usage
        self.cpu_progressbar['value'] = cpu_percent

        # Update memory progress bar with current memory usage
        self.memory_progressbar['value'] = memory_percent

        # Update disk progress bar with current disk usage
        self.disk_progressbar['value'] = disk_percent

        # Format the CPU usage text
        cpu_text_str = f"CPU Usage: {cpu_percent}%"

        # Format the memory usage text with used and total memory in GB and percentage
        memory_text_str = f"Memory Usage: {
            memory_used}GB/{memory_total}GB ({memory_percent}%)"

        # Format the disk usage text with used and total disk space in GB and percentage
        disk_text_str = f"Disk Usage: {
            disk_used}GB/{disk_total}GB ({disk_percent}%)"

        # Update the CPU usage text label in the UI
        self.cpu_text.config(text=cpu_text_str)

        # Update the memory usage text label in the UI
        self.memory_text.config(text=memory_text_str)

        # Update the disk usage text label in the UI
        self.disk_text.config(text=disk_text_str)

        # Get network usage data (in bytes) and calculate the MB usage
        net_io = psutil.net_io_counters()
        bytes_sent = round(
            # Convert to MB
            (net_io.bytes_sent - self.initial_bytes_sent) / (1024 ** 2), 2)
        bytes_recv = round(
            # Convert to MB
            (net_io.bytes_recv - self.initial_bytes_recv) / (1024 ** 2), 2)

        # Format the network usage text
        network_text_str = f"Sent: {
            bytes_sent} MB / Received: {bytes_recv} MB"

        # Update the network usage text label in the UI
        self.network_text.config(text=network_text_str)

        # Schedule the next update of the progress bars after 1000 milliseconds
        self.root.after(1000, self.update_progressbars)

# -------------------------- CREATE WIDGETS ------------------------------ #
    def create_widgets(self):
        # Create and position the CPU usage label
        self.cpu_label = tk.Label(self.root, text="CPU Usage")
        self.cpu_label.grid(row=0, column=0, sticky="e",
                            padx=10, pady=(20, 5))  # Extra padding on top

        # Create and position the CPU progress bar
        self.cpu_progressbar = ttk.Progressbar(
            self.root, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.cpu_progressbar.grid(row=0, column=1, padx=10, pady=(20, 5))

        # Create and position the CPU usage text label
        self.cpu_text = tk.Label(self.root, text="")
        self.cpu_text.grid(row=0, column=2, sticky="w", padx=10, pady=(20, 5))

        # Create and position the memory usage label
        self.memory_label = tk.Label(self.root, text="Memory Usage")
        self.memory_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)

        # Create and position the memory progress bar
        self.memory_progressbar = ttk.Progressbar(
            self.root, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.memory_progressbar.grid(row=1, column=1, padx=10, pady=5)

        # Create and position the memory usage text label
        self.memory_text = tk.Label(self.root, text="")
        self.memory_text.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Create and position the disk usage label
        self.disk_label = tk.Label(self.root, text="Disk Usage")
        self.disk_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)

        # Create and position the disk progress bar
        self.disk_progressbar = ttk.Progressbar(
            self.root, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.disk_progressbar.grid(row=2, column=1, padx=10, pady=5)

        # Create and position the disk usage text label
        self.disk_text = tk.Label(self.root, text="")
        self.disk_text.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        # Create and position the network usage label at the bottom
        self.network_label = tk.Label(self.root, text="Network Usage")
        self.network_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)

        # Create and position the network progress bar
        self.network_progressbar = ttk.Progressbar(
            self.root, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.network_progressbar.grid(row=3, column=1, padx=10, pady=5)

        # Create and position the network usage text label
        self.network_text = tk.Label(self.root, text="")
        self.network_text.grid(row=3, column=2, sticky="w", padx=10, pady=5)

# -------------------------- START APP ----------------------------------- #
    def start(self):
        thread = threading.Thread(target=self.update_progressbars)
        thread.start()

        self.root.mainloop()


app = App()
app.start()
