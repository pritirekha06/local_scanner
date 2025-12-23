#!/usr/bin/env python3
"""
quickweb.py
Quick check to see if any web services are running locally.
Only scan your own machine or private network IPs.
"""

import socket
import sys
import time

#-- Core logic --

def check_local_web(ip="127.0.0.1"):
    """Check for common web services on the given local IP."""

    print(f"\n=== Checking web services on {ip} ===")
    print("(Local machine / private network only)\n")

    web_ports = [
        (80, "HTTP"),
        (443, "HTTPS"),
        (8080, "HTTP alternate"),
        (3000, "Node.js dev server"),
        (5000, "Flask dev server"),
        (8000, "Python http.server"),
        (8443, "HTTPS alternate"),
        (9000, "PHP"),
        (8888, "Jupyter Notebook")
    ]

    found = []

    for port, label in web_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)

                if sock.connect_ex((ip, port)) == 0:
                    server_info = "unknown"

                    # try a simple HTTP request
                    try:
                        sock.sendall(
                            b"GET / HTTP/1.0\r\nHost: localhost\r\n\r\n"
                        )
                        response = sock.recv(1024).decode(errors="ignore")

                        for line in response.splitlines():
                            line_low = line.lower()
                            if line_low.startswith("server:"):
                                server_info = line.split(":", 1)[1].strip()
                                break
                            if "apache" in line_low:
                                server_info = "Apache"
                                break
                            if "nginx" in line_low:
                                server_info = "nginx"
                                break
                            if "iis" in line_low:
                                server_info = "IIS"
                                break

                    except socket.error:
                        server_info = "running (no banner)"

                    print(f"[open] {label} on port {port}")
                    print(f"       Server: {server_info}")

                    found.append((port, label, server_info))

        except socket.error as e:
            print(f"[warn] Could not check port {port}: {e}")

        time.sleep(0.05)

    print()

    if found:
        print(f"Detected {len(found)} web service(s):")
        for port, label, server in found:
            print(f"  - {label} ({port}): {server}")

        with open("my_web_servers.txt", "w") as f:
            f.write(f"Local Web Services on {ip}\n")
            f.write("=" * 40 + "\n")
            for port, label, server in found:
                f.write(f"Port {port} ({label}): {server}\n")

        print("\nResults saved to my_web_servers.txt")

        print("\nIf you did not expect these services:")
        print("  - Check what software started them")
        print("  - Stop unused dev servers")
        print("  - Secure or firewall exposed services")

    else:
        print("No web servers detected (this is normal).")
        print("\nTip to test this script:")
        print("  python -m http.server 8080")
        print("Then run this script again.")

    print("\n=== Scan complete ===")


# -- Entry point --

def main():
    if len(sys.argv) > 1:
        ip = sys.argv[1]

        # basic safety check
        allowed = (
            ip == "127.0.0.1"
            or ip == "localhost"
            or ip.startswith("192.168.")
            or ip.startswith("10.")
        )

        if not allowed:
            print("\nError: This script is for local/private IPs only.")
            print("Use 127.0.0.1 or your home network IP.")
            return

        check_local_web(ip)
    else:
        check_local_web()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")