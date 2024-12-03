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

        self.cpu_gauge = ttk.Progressbar(
            self.container, orient="horizontal", length=300, mode="determinate")
        self.cpu_gauge.pack()

        self.cpu_percent_label = ttk.Label(self.container, text="0%")
        self.cpu_percent_label.pack()

        self.memory_label = ttk.Label(self.container, text="Memory Usage")
        self.memory_label.pack()

        self.memory_gauge = ttk.Progressbar(
            self.container, orient="horizontal", length=300, mode="determinate")
        self.memory_gauge.pack()

        self.memory_percent_label = ttk.Label(self.container, text="0%")
        self.memory_percent_label.pack()

        self.disk_label = ttk.Label(self.container, text="Disk Usage")
        self.disk_label.pack()

        self.disk_gauge = ttk.Progressbar(
            self.container, orient="horizontal", length=300, mode="determinate")
        self.disk_gauge.pack()

        self.disk_percent_label = ttk.Label(self.container, text="0%")
        self.disk_percent_label.pack()

        self.network_label = ttk.Label(self.container, text="Network Usage")
        self.network_label.pack()

        self.network_gauge = ttk.Progressbar(
            self.container, orient="horizontal", length=300, mode="determinate")
        self.network_gauge.pack()

        self.network_percent_label = ttk.Label(self.container, text="0 KB/s")
        self.network_percent_label.pack()

        self.is_running = True
        self.update_thread = threading.Thread(target=self.update_gauges_thread)
        self.update_thread.start()

        # Register cleanup function to stop threads on exit
        atexit.register(self.cleanup)

    def cleanup(self):
        self.is_running = False
        self.update_thread.join()

    def update_gauges_thread(self):
        while self.is_running:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            network_percent = psutil.net_io_counters().bytes_sent / 1024

            self.root.after(0, self.update_gauges, cpu_percent,
                            memory_percent, disk_percent, network_percent)
            time.sleep(1)  # Add a small delay to prevent busy-waiting

    def update_gauges(self, cpu_percent, memory_percent, disk_percent, network_percent):
        self.cpu_gauge["value"] = cpu_percent
        self.cpu_percent_label.config(text=f"{cpu_percent:.1f}%")

        self.memory_gauge["value"] = memory_percent
        self.memory_percent_label.config(text=f"{memory_percent:.1f}%")

        self.disk_gauge["value"] = disk_percent
        self.disk_percent_label.config(text=f"{disk_percent:.1f}%")

        self.network_gauge["value"] = network_percent
        self.network_percent_label.config(text=f"{network_percent:.1f} KB/s")

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
