#!/usr/bin/env python3
"""
    Name: psutil_system_info.py
    Author: William A Loring
    Created: 09-18-21 Revised:
    Purpose: Test program with functions for monitoring CPU
    and RAM usage in Python with PsUtil
"""
# pip install psutil
import psutil
# importing module
import platform

# system name
system_name = platform.system()
# platform details
platform_details = platform.platform()

# processor name
processor_name = platform.processor()

# architectural detail
architecture_details = platform.architecture()
network_name = platform.node()

print(f"            OS: {system_name}")
print(f"    OS Version: {platform_details}")
print(f"     Processor: {processor_name}")
print(f"     Host Name: {network_name}")

"""
    Obtains the system's average CPU load as measured 
    over a period of 500 milliseconds.
    interval=0.5
    :returns: System CPU load as a percentage.
    :rtype: float
"""
cpu_percent = psutil.cpu_percent(interval=None)

"""
    Obtains the real-time value of the current CPU frequency.
    :returns: Current CPU frequency in BHz.
    :rtype: int
"""
cpu_freq = int(psutil.cpu_freq().current) / 1024

"""
    Obtains the absolute number of RAM bytes currently in use by the system.
    :returns: System RAM usage in Gigabytes.
    :rtype: int
"""
ram_useage = int(psutil.virtual_memory().total -
                 psutil.virtual_memory().available)
ram_useage = ram_useage / 1024 / 1024 / 1024


"""
    Obtains the total amount of RAM in bytes available to the system.
    :returns: Total system RAM in bytes.
    :rtype: int
"""
ram_total = int(psutil.virtual_memory().total)
ram_total = ram_total / 1024 / 1024 / 1024


"""
    Obtains the system's current RAM usage.
    :returns: System RAM usage as a percentage.
    :rtype: float
"""
virtual_memory = psutil.virtual_memory().percent


print(
    f"           CPU: {psutil.cpu_count(logical=False)}")
print(f"   Logical CPU: {psutil.cpu_count()}")

# Output current CPU usage as a percentage
print(f"     CPU usage: {cpu_percent} %")

# Output current CPU frequency in GHz
print(
    f" CPU frequency: {cpu_freq:,.2f} GHz")

# Output total RAM in GB
print(
    f"     RAM total: {ram_total:,.2f} GB")

# Output current RAM usage in GB
print(
    f"     RAM usage: {ram_useage:,.2f} GB")

# Output current RAM usage as a percentage.
print(f"     RAM usage: {virtual_memory} %")
