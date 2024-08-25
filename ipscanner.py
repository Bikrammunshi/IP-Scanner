import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def check_ports(ip, port, delay, open_ports):
    """Check if a port is open on a given IP."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(delay)
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports[port] = "Open"
        except socket.error as e:
            print(f"Socket error occurred: {e}")


def scanning_ports(ip, delay, max_threads):
    """Scan ports on a given IP address."""
    open_ports = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for port in range(1, 5000):
            executor.submit(check_ports, ip, port, delay, open_ports)

    print("Open Ports: ")
    for port, status in open_ports.items():
        try:
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "Unknown Service"
        print(f"{port}\t{service}")


def get_host_address_range(ip_range):
    """Extract network address and host range from IP addresses."""
    def split_ip(ip):
        parts = ip.split('.')
        return '.'.join(parts[:3]) + '.', parts[3]

    network_addr, first_host = split_ip(ip_range[0])
    network_addr1, last_host = split_ip(ip_range[1])

    if network_addr != network_addr1:
        raise ValueError("IP range does not have the same network address.")
    
    return network_addr, first_host, last_host


def ping_hosts(network_addr, first_host, last_host):
    """Ping a range of hosts to check if they are up."""
    opn_hosts = []
    for i in range(int(first_host), int(last_host) + 1):
        ip_to_ping = f"{network_addr}{i}"
        try:
            process = subprocess.run(["ping", "-c", "1", "-W", "1", ip_to_ping], capture_output=True, text=True)
            if "ttl" in process.stdout.lower():
                print(f"Host {ip_to_ping} is UP")
                opn_hosts.append(ip_to_ping)
            else:
                print(f"Host {ip_to_ping} is DOWN")
        except subprocess.SubprocessError as e:
            print(f"Subprocess error: {e}")
    return opn_hosts


def main():
    print(""" 
     ___ ____  ____
    |_ _|  _ \/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
     | || |_) \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
     | ||  __/ ___) | (_| (_| | | | | | | |  __/ |   
    |___|_|   |____/ \___\__,_|_| |_|_| |_|\___|_| 

    Made by Bikramaditya Munshi
    Preferred for Linux machines
    -----------------------------------------------------------------
    """)
    print("Class C IP addresses accepted.")

    choice = input("Will you be working with a single IP address? Enter 'y' to say yes: ")
    if choice.lower() == 'y':
        target = input("Enter the IP address or the host name: ")
        try:
            first_ip = last_ip = socket.gethostbyname(target)
        except socket.gaierror:
            print("Host not identified or might be down.")
            return
    else:
        first_ip = input("Enter the first IP address: ")
        last_ip = input("Enter the last IP address: ")

    start_time = datetime.now()
    print("\nStarting process...")
    print(f"Start time: {start_time}\n")

    try:
        network_addr, first_host, last_host = get_host_address_range((first_ip, last_ip))
    except ValueError as ve:
        print(ve)
        return

    opn_hosts = ping_hosts(network_addr, first_host, last_host)
    print(f"{len(opn_hosts)} hosts up out of {int(last_host) - int(first_host) + 1}")

    for ip in opn_hosts:
        print(f"\nScanning open ports on {ip}...")
        scanning_ports(ip, delay=100000, max_threads=1000000)  # Adjust max_threads based on your system capacity

    end_time = datetime.now()
    print("\nCompleted Process...")
    print(f"End time: {end_time}")
    print(f"Total time: {end_time - start_time}")


if __name__ == "__main__":
    main()
