#Local_Scanner
A simple Python-based scanner to check **my own computer and home network** for open ports, running services, connected devices, and local web servers.

## Features

- Checks **MY computer** for open ports  
- Finds devices on **MY home network**  
- Checks what **services are running** on MY PC  
- Looks for **web servers** on MY machines  

## Requirements

- Python 3.x

## Usage

### mycheck.py

```bash
python mycheck.py <command>
Commands:

me – Scan MY computer for open ports

network – Scan MY local network for connected devices

services – Check running services on MY PC

all – Run all checks (ports + network + services)

Examples:

bash
Copy code
python mycheck.py me
python mycheck.py network
python mycheck.py services
python mycheck.py all
quickweb.py
bash
Copy code
python quickweb.py [local_ip]
Arguments:

local_ip (optional) – IP to check for web services

Default: 127.0.0.1 (your own computer)

Allowed: 127.0.0.1, localhost, 192.168.x.x, 10.x.x.x

Examples:

bash
Copy code
python quickweb.py
python quickweb.py 192.168.1.50
What It Saves
my_open_ports.txt – list of open ports on your computer

my_network_devices.txt – devices detected on your local network

my_services.txt – detected services running on your PC

my_web_servers.txt – detected web servers

Output
Results are printed directly in the terminal / console

Report files are saved automatically if something is found

Output depends on current system and network state

###Disclaimer

Use this tool ONLY on computers and networks you own or have explicit permission to scan.

This project scans local IPs only (127.0.0.1, localhost, 192.168.x.x, 10.x.x.x) and does NOT scan public websites.



