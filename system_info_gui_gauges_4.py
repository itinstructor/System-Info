import tkinter as tk
from tkinter import ttk
import psutil
import threading
import atexit
import time

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        self.container = ttk.Frame(root, padding=10)
        self.container.pack()

        self.cpu_label = ttk.Label(self.container, text="CPU Usage")
        self.cpu_label.pack()

        self.cpu_canvas = tk.Canvas(self.container, width=150, height=150)
        self.cpu_canvas.pack()

        self.cpu_percent_label = ttk.Label(self.container, text="0%")
        self.cpu_percent_label.pack()

        self.memory_label = ttk.Label(self.container, text="Memory Usage")
        self.memory_label.pack()

        self.memory_canvas = tk.Canvas(self.container, width=150, height=150)
        self.memory_canvas.pack()

        self.memory_percent_label = ttk.Label(self.container, text="0%")
        self.memory_percent_label.pack()

        self.network_label = ttk.Label(self.container, text="Network Usage")
        self.network_label.pack()

        self.upload_label = ttk.Label(self.container, text="Upload: 0 KB/s")
        self.upload_label.pack()

        self.download_label = ttk.Label(self.container, text="Download: 0 KB/s")
        self.download_label.pack()

        self.is_running = True
        self.update_thread = threading.Thread(target=self.update_gauges_thread)
        self.update_thread.start()

        # Register cleanup function to stop threads on exit
        atexit.register(self.cleanup)

    def cleanup(self):
        self.is_running = False
        self.update_thread.join()

    def draw_circular_gauge(self, canvas, percent):
        x = y = 75
        radius = 60
        start_angle = 90  # Start from top (12 o'clock)
        extent = -360 * percent / 100  # Calculate extent in degrees

        canvas.create_arc(
            x - radius, y - radius, x + radius, y + radius,
            start=start_angle, extent=extent,
            fill='green', outline=''
        )

    def update_gauges_thread(self):
        while self.is_running:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            network_stats = psutil.net_io_counters()

            self.root.after(0, self.update_gauges, cpu_percent, memory_percent, network_stats)
            time.sleep(1)  # Add a small delay to prevent busy-waiting

    def update_gauges(self, cpu_percent, memory_percent, network_stats):
        self.draw_circular_gauge(self.cpu_canvas, cpu_percent)
        self.cpu_percent_label.config(text=f"{cpu_percent:.1f}%")

        self.draw_circular_gauge(self.memory_canvas, memory_percent)
        self.memory_percent_label.config(text=f"{memory_percent:.1f}%")

        upload_speed = network_stats.bytes_sent / 1024
        download_speed = network_stats.bytes_recv / 1024

        self.upload_label.config(text=f"Upload: {upload_speed:.1f} KB/s")
        self.download_label.config(text=f"Download: {download_speed:.1f} KB/s")

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
