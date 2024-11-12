import tkinter as tk
from tkinter import ttk
import psutil

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        
        self.cpu_label = tk.Label(root, text="CPU Usage")
        self.cpu_label.pack()

        self.cpu_gauge = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.cpu_gauge.pack()

        self.memory_label = tk.Label(root, text="Memory Usage")
        self.memory_label.pack()

        self.memory_gauge = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.memory_gauge.pack()

        self.update_gauges()
        
    def update_gauges(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent

        self.cpu_gauge["value"] = cpu_percent
        self.memory_gauge["value"] = memory_percent

        self.root.after(1000, self.update_gauges)

def main():
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
