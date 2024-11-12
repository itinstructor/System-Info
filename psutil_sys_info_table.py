#!/usr/bin/env python3
"""
    Test program with functions for monitoring CPU
    and RAM usage in Python with PsUtil
"""

import os
import sys
import psutil
from time import sleep
# Windows: pip install rich
# Linux: pip3 install rich
# Import Console for console printing
from rich.console import Console
# Import Panel for title displays
from rich.panel import Panel
from rich.table import Table

# Initialize rich.console
console = Console()


class SystemInfo:
    def __init__(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self._sent = 0
        self._recv = 0
        while True:
            table = Table(
                title="\nSystem Information",
                title_style="bold blue",
                header_style="bold blue"
            )

            table.add_column("Description", justify="right")
            table.add_column("Value", min_width=20)
            table.add_row("CPU", f"{psutil.cpu_count(logical=False)}")
            table.add_row("Logical CPU", f"{psutil.cpu_count()}")

            # Output current CPU usage as a percentage
            table.add_row("CPU usage", f"{self.get_cpu_usage_pct()} %")

            # Output current CPU frequency in Ghz
            table.add_row("CPU frequency",
                          f"{(self.get_cpu_frequency()):,.2f} Ghz")

            # Output total RAM in GB
            table.add_row(
                "RAM total", f"{self.get_ram_total():,.2f} GB")

            # Output current RAM usage in GB
            table.add_row(
                "RAM usage",  f"{self.get_ram_usage():,.2f} GB")

            # Output current RAM usage as a percentage
            table.add_row("RAM usage pct", f"{self.get_ram_usage_pct()} %")

            # # Output current Swap usage in GB
            # table.add_row(
            #     "Swap usage",  f"{get_swap_usage() / 1024 / 1024 /1024:,.2f} GB    ")

            # # Output total Swap in GB
            # table.add_row(
            #     "Swap total", f"{get_swap_total() / 1024 / 1024 / 1024:,.2f} GB    ")

            # # Output current Swap usage as a percentage
            # table.add_row("Swap usage", f"{get_swap_usage_pct()} %")

            # Display network io in Kilobits per second
            table.add_row(
                "Net IO sent", f"{self._sent:,.1f} Kbps")
            table.add_row(
                "Net IO recv", f"{self._recv:,.1f} Kbps")

            # Print table to console
            console.print(table)

            # Get current network io statistics in Kbps
            sent_1, recv_1 = self.get_network_io()
            sleep(1)
            # Get current network io statistics in Kbps
            sent_2, recv_2 = self.get_network_io()
            # Subtract first reading from second reading
            # gives us how many kilobits were sent/recv per second
            self._sent = sent_2 - sent_1
            self._recv = recv_2 - recv_1

            # Clear console
            console.clear()

    def get_network_io(self):
        """
            Get current net io counters statistics in bytes
            convert to bits, then kb
        """
        sent = psutil.net_io_counters().bytes_sent
        recv = psutil.net_io_counters().bytes_recv
        # Convert bytes to bits *8, convert bits to kilobits / 1024
        sent = (sent * 8) / 1024
        recv = (recv * 8) / 1024

        return sent, recv

    def get_cpu_usage_pct(self):
        """
            Obtains the system's average CPU load as measured over a period of 500 milliseconds.
            interval=0.5
            :returns: System CPU load as a percentage.
            :rtype: float
        """
        return psutil.cpu_percent(interval=None)

    def get_cpu_frequency(self):
        """
            Obtains the real-time value of the current CPU frequency.
            :returns: Current CPU frequency in BHz.
            :rtype: int
        """
        return int(psutil.cpu_freq().current) / 1024

    def get_ram_total(self):
        """
            Obtains the total amount of RAM in bytes available to the system.
            :returns: Total system RAM in bytes.
            :rtype: int
        """
        ram_total = int(psutil.virtual_memory().total)
        return ram_total / 1024 / 1024 / 1024

    def get_ram_usage(self):
        """
            Obtains the absolute number of RAM bytes currently in use by the system.
            :returns: System RAM usage in Gigabytes.
            :rtype: int
        """
        ram_useage = int(psutil.virtual_memory().total -
                         psutil.virtual_memory().available)
        return ram_useage / 1024 / 1024 / 1024

    def get_ram_usage_pct(self):
        """
            Obtains the system's current RAM usage.
            :returns: System RAM usage as a percentage.
            :rtype: float
        """
        return psutil.virtual_memory().percent

    def get_swap_total(self):
        """
            Obtains the total amount of Swap in bytes available to the system.
            :returns: Total system Swap in Gigabytes.
            :rtype: int
        """
        # Bytes
        swap_total = int(psutil.swap_memory().total)
        return swap_total / 1024 / 1024 / 1024

    def get_swap_usage(self):
        """
            Obtains the absolute number of Swap bytes currently in use by the system.
            :returns: System Swap usage in Gbytes.
            :rtype: int
        """
        # Bytes
        swap_useage = int(psutil.swap_memory().used)
        return swap_useage / 1024 / 1024 / 1024

    def get_swap_usage_pct(self):
        """
            Obtains the system's current Swap usage.
            :returns: System Swap usage as a percentage.
            :rtype: float
        """
        return psutil.swap_memory().percent


if __name__ == "__main__":
    try:
        system_info = SystemInfo()
    except KeyboardInterrupt:
        sys.exit(0)
