import tkinter as tk
from tkinter import ttk
import psutil
import threading
import atexit
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        self.container = ttk.Frame(root, padding=10)
        self.container.pack()

        self.network_label = ttk.Label(self.container, text="Network Usage")
        self.network_label.pack()

        self.upload_label = ttk.Label(self.container, text="Upload: 0 KB/s")
        self.upload_label.pack()

        self.download_label = ttk.Label(self.container, text="Download: 0 KB/s")
        self.download_label.pack()

        self.is_running = True
        self.upload_data = []  # Store network upload data
        self.download_data = []  # Store network download data
        self.network_time = []  # Store time data for the x-axis (network)
        self.prev_upload = psutil.net_io_counters().bytes_sent
        self.prev_download = psutil.net_io_counters().bytes_recv
        self.update_thread = threading.Thread(target=self.update_gauges_thread)
        self.update_thread.start()

        # Create Matplotlib figures and canvases for the line charts
        self.figure_cpu = plt.figure(figsize=(6, 3), tight_layout=True)
        self.cpu_ax = self.figure_cpu.add_subplot(111)
        self.canvas_cpu = FigureCanvasTkAgg(self.figure_cpu, master=root)
        self.canvas_cpu.get_tk_widget().pack()

        self.figure_network = plt.figure(figsize=(6, 3), tight_layout=True)
        self.network_ax = self.figure_network.add_subplot(111)
        self.canvas_network = FigureCanvasTkAgg(self.figure_network, master=root)
        self.canvas_network.get_tk_widget().pack()

        # Register cleanup function to stop threads on exit
        atexit.register(self.cleanup)

    def cleanup(self):
        self.is_running = False
        self.update_thread.join()

    def update_gauges_thread(self):
        while self.is_running:
            network_stats = psutil.net_io_counters()

            self.root.after(0, self.update_gauges, network_stats)
            time.sleep(1)  # Add a small delay to prevent busy-waiting

    def update_gauges(self, network_stats):
        current_upload = network_stats.bytes_sent
        current_download = network_stats.bytes_recv

        upload_speed = (current_upload - self.prev_upload) / 1024
        download_speed = (current_download - self.prev_download) / 1024

        self.prev_upload = current_upload
        self.prev_download = current_download

        # Update network data for the line chart
        self.upload_data.append(upload_speed)
        self.download_data.append(download_speed)
        self.network_time.append(time.time())  # Use current time as x-axis value

        # Update the line charts with new data
        self.update_line_charts()

        # Update labels with network speed information
        self.upload_label.config(text=f"Upload: {upload_speed:.1f} KB/s")
        self.download_label.config(text=f"Download: {download_speed:.1f} KB/s")

    def update_line_charts(self):
        self.network_ax.clear()
        self.network_ax.plot(self.network_time, self.upload_data, marker='o', linestyle='-', color='green', label='Upload')
        self.network_ax.plot(self.network_time, self.download_data, marker='o', linestyle='-', color='blue', label='Download')
        self.network_ax.set_xlabel('Time')
        self.network_ax.set_ylabel('Network Speed (KB/s)')
        self.network_ax.set_title('Network Bandwidth Over Time')
        self.network_ax.legend()
        self.network_ax.grid(True)
        self.canvas_network.draw()

    def stop(self):
        self.is_running = False

def main():
    root = tk.Tk()
    app = SystemMonitorApp(root)

    def on_closing():
        app.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
