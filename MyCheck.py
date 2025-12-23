#!/usr/bin/env python3
"""
mycheck.py
A simple system & network self-check tool.
Only use this on machines and networks you own or have permission for.
"""

import sys
import os
import socket
import time
import subprocess
import platform
from datetime import datetime
VERSION = "0.1-learning"


# -- IP helpers --

def get_local_ip():
    """Return the local LAN IP of this machine."""
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except socket.error as e:
        print(f"[warn] Could not get local IP: {e}")
        return "127.0.0.1"


# -- Port scanning --

def check_my_ports():
    """Check common ports on this computer."""
    print("\n=== Checking this computer ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    ips = ["127.0.0.1", get_local_ip()]
    seen = set()
    ips = [ip for ip in ips if not (ip in seen or seen.add(ip))]

    print("IP addresses:")
    for ip in ips:
        print(f"  - {ip}")
    print()

    common_ports = [
        21,    # FTP
        22,    # SSH
        23,    # Telnet
        25,    # SMTP
        80,    # HTTP
        443,   # HTTPS
        445,   # SMB
        1433,  # MSSQL
        3306,  # MySQL
        3389,  # RDP
        5432,  # PostgreSQL
        5900,  # VNC
        8080,  # HTTP alt
        8443   # HTTPS alt
    ]

    open_ports = []

    print("Scanning localhost (127.0.0.1):")
    for port in common_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.4)
                if sock.connect_ex(("127.0.0.1", port)) == 0:
                    service = "service detected"

                    # simple HTTP banner check
                    if port == 80:
                        try:
                            sock.sendall(b"HEAD / HTTP/1.0\r\nHost: localhost\r\n\r\n")
                            data = sock.recv(1024).decode(errors="ignore")
                            for line in data.splitlines():
                                if line.lower().startswith("server:"):
                                    service = line.strip()
                                    break
                            else:
                                service = "HTTP server"
                        except socket.error:
                            service = "HTTP server"

                    print(f"  [open] {port} ({service})")
                    open_ports.append(f"127.0.0.1:{port} - {service}")

        except socket.error as e:
            print(f"  [error] Port {port}: {e}")

    if open_ports:
        print(f"\nFound {len(open_ports)} open ports:")
        for item in open_ports:
            print(f"  - {item}")

        with open("my_open_ports.txt", "w") as f:
            f.write(f"My Open Ports - {datetime.now()}\n")
            f.write("=" * 40 + "\n")
            for item in open_ports:
                f.write(item + "\n")

        print("\nSaved results to my_open_ports.txt")
    else:
        print("\nNo common ports appear to be open.")

    print("\n=== Port check finished ===")


# -- Network scan --

def check_my_network():
    """Look for other devices on the local network."""
    print("\n=== Checking local network ===")

    local_ip = get_local_ip()
    parts = local_ip.split(".")
    if len(parts) != 4:
        print("Could not determine network range.")
        return

    base = ".".join(parts[:3]) + "."
    print(f"Local network assumed: {base}0/24\n")

    found = []
    system = platform.system().lower()

    for i in range(1, 21):  # small range to keep it fast
        ip = base + str(i)
        if ip == local_ip:
            continue

        if system == "windows":
            cmd = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]

        try:
            result = subprocess.run(cmd, capture_output=True, timeout=3)
            if result.returncode == 0:
                try:
                    name = socket.gethostbyaddr(ip)[0]
                except socket.herror:
                    name = "unknown"

                print(f"  [+] {ip} ({name})")
                found.append((ip, name))

        except subprocess.TimeoutExpired:
            pass

    if found:
        with open("my_network_devices.txt", "w") as f:
            f.write(f"My Network Devices - {datetime.now()}\n")
            f.write("=" * 40 + "\n")
            for ip, name in found:
                f.write(f"{ip} - {name}\n")

        print("\nSaved results to my_network_devices.txt")
    else:
        print("No other active devices found.")

    print("\n=== Network scan finished ===")


# -- Service check --

def check_my_services():
    """Check for common local services."""
    print("\n=== Checking running services ===")

    services = []

    # check common ports
    service_ports = {
        "Web server": [80, 443, 8080, 3000, 5000],
        "Database": [3306, 5432, 27017, 6379]
    }

    for name, ports in service_ports.items():
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.4)
                    if sock.connect_ex(("127.0.0.1", port)) == 0:
                        services.append(f"{name} on port {port}")
            except socket.error:
                pass

    # process check (basic)
    try:
        if os.name == "posix":
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
            keywords = ["apache", "nginx", "mysql", "postgres", "mongod", "redis", "ssh"]
            for line in result.stdout.splitlines():
                for key in keywords:
                    if key in line.lower():
                        services.append(f"Process: {key}")
                        break

        else:
            result = subprocess.run(
                ["tasklist"],
                capture_output=True,
                text=True
            )
            keywords = ["apache", "nginx", "mysql", "postgres", "mongo", "redis"]
            for line in result.stdout.splitlines():
                for key in keywords:
                    if key in line.lower():
                        services.append(f"Process: {key}")
                        break

    except Exception as e:
        print(f"[warn] Could not list processes: {e}")

    if services:
        services = list(dict.fromkeys(services)) 
        for svc in services:
            print(f"  - {svc}")

        with open("my_services.txt", "w") as f:
            f.write(f"My Services - {datetime.now()}\n")
            f.write("=" * 40 + "\n")
            for svc in services:
                f.write(svc + "\n")

        print("\nSaved results to my_services.txt")
    else:
        print("No common services detected.")

    print("\n=== Service check finished ===")

# -- Main --

def main():
    print("\n" + "=" * 50)
    print(f" My System Checker v{VERSION}")
    print("Scan your own computer & network safely")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python mycheck.py me")
        print("  python mycheck.py network")
        print("  python mycheck.py services")
        print("  python mycheck.py all\n")
        return

    cmd = sys.argv[1].lower()

    if cmd == "me":
        check_my_ports()
    elif cmd == "network":
        check_my_network()
    elif cmd == "services":
        check_my_services()
    elif cmd == "all":
        check_my_ports()
        check_my_network()
        check_my_services()
    else:
        print("Unknown command.")

    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")