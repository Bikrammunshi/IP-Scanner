     ___ ____  ____
    |_ _|  _ \/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
     | || |_) \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
     | ||  __/ ___) | (_| (_| | | | | | | |  __/ |   
    |___|_|   |____/ \___\__,_|_| |_|_| |_|\___|_| 

    Made by Bikramaditya Munshi
    Preferred for Linux machines



### Overview

This Python script is a network utility designed for scanning a range of IP addresses and checking which ones are online (up) and then scanning those online IPs for open TCP ports. This tool is particularly suited for Linux machines due to the use of the `ping` command with specific parameters.

### Requirements

To run this script, you need:

1. **Python 3.6 or higher**: The script uses modern Python features, including `f-strings` and `concurrent.futures.ThreadPoolExecutor`, which are supported in Python 3.6+.
2. **Python Standard Library Modules**:
    - `subprocess`: Used to run system commands for pinging IP addresses.
    - `socket`: Provides low-level networking interfaces for checking open ports.
    - `concurrent.futures`: Facilitates concurrent execution using thread pools.
    - `datetime`: Used for tracking the duration of the scanning process.
3. **Operating System**:
    - **Linux**: The script is optimized for Linux systems because the `ping` command syntax (`c` for count and `W` for wait time) is specific to Linux. Adjustments are necessary for other operating systems like Windows.

### How It Works

1. **User Input**:
    - The script begins by asking the user if they want to work with a single IP address or a range of IP addresses.
    - If the user chooses a single IP address, they can input either a hostname or an IP address. The script resolves the hostname to an IP if necessary.
    - If a range is desired, the user inputs the starting and ending IP addresses.
2. **IP Address Validation and Range Setup**:
    - For IP ranges, the script ensures that both IP addresses belong to the same network address. This validation prevents the scanning of unrelated IP blocks.
3. **Host Availability Check (Ping)**:
    - The script pings each IP address in the specified range to determine if the host is up or down.
    - It uses the `ping` command with a timeout of 1 second (`W 1`). The number of packets sent is 1 (`c 1`).
    - If a host responds, it is marked as "UP," and further port scanning is performed on that IP.
4. **Port Scanning**:
    - For each IP that is up, the script scans ports from 1 to 4999 using threads for concurrent scanning.
    - It uses the `ThreadPoolExecutor` to manage a pool of threads, which allows multiple port checks to happen simultaneously.
    - Ports that are open are recorded, and their corresponding services (if known) are displayed.
5. **Output**:
    - The script outputs a list of hosts that are up and their corresponding open ports along with the service names associated with those ports.
    - It also provides timing information on how long the scanning process took.
6. **Error Handling**:
    - The script includes basic error handling for socket errors, subprocess errors, and invalid user input.

### Usage Instructions

1. **Run the Script**:
    - Open a terminal on a Linux machine.
    - Navigate to the directory where the script is located.
    - Run the script using Python: `python3 script_name.py`
2. **Follow Prompts**:
    - If scanning a single IP or hostname, input the appropriate information when prompted.
    - If scanning a range, provide the start and end IPs of the range. Ensure both IPs belong to the same network.
3. **Review Results**:
    - The script will display hosts that are up and the open ports on each host.
    - Check the console output for details on the scanning process and timing.

### Customization and Optimization

- **Port Range**: By default, the script scans ports from 1 to 4999. You can modify the `range` in the `scanning_ports` function to scan different port ranges.
- **Thread Pool Size**: Adjust the `max_threads` parameter in the `scanning_ports` function call. A higher number can speed up scanning on systems with more resources but may cause network congestion or trigger IDS/IPS systems.
- **Ping Timeout and Count**: Modify the `ping` command parameters to change the number of packets or timeout duration.

### Notes

- **Ethical Use**: Ensure you have permission to scan any IP addresses or networks. Unauthorized scanning can be illegal and may lead to severe consequences.
- **Performance**: This script is not optimized for extremely large networks or very high port ranges. For extensive scanning, consider using professional tools like Nmap.
