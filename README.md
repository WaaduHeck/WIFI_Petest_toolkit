# WIFI_Petest_toolkit

📡 WiFi Penetration Toolkit (Python)
A command-line-based WiFi security testing toolkit built with Python.
This project automates common wireless penetration testing tasks using the Aircrack-ng suite for educational and authorised lab environments.

⚠️ This tool is strictly for educational purposes and authorised security testing only.

🚀 Features
✅ Automatic root privilege check
✅ Required tool verification (Aircrack-ng suite)
✅ Monitor mode automation
✅ Wireless network scanning
✅ WPA/WPA2 handshake capture
✅ Deauthentication testing
✅ Password cracking using wordlists
✅ WPS testing support
✅ Clean interactive CLI menu
✅ Colored terminal UI

🛠️ Technologies Used
Python 3
Linux (Tested on Kali Linux / Ubuntu)
Aircrack-ng Suite:
airmon-ng
airodump-ng
aireplay-ng
aircrack-ng
Reaver (for WPS testing)

📦 Installation
1️⃣ Clone Repository
git clone https://github.com/yourusername/wifi-penetration-toolkit.git
cd wifi-penetration-toolkit

2️⃣ Install Required Tools
On Debian-based systems:
sudo apt update
sudo apt install aircrack-ng reaver

▶️ Usage
Run the tool with root privileges:
sudo python3 toolkit.py
Main Menu Options:
Scan Networks
Capture WPA Handshake
Deauthentication Attack
Crack Password
WPS Attack
Exit

📌 Workflow Example
Select wireless interface (e.g., wlan0)
Enable monitor mode automatically
Scan available WiFi networks
Capture the handshake of the target network
Use the wordlist to attempt password cracking

🔐 Ethical Use & Disclaimer
This tool is developed for:
Cybersecurity students
Lab environments
Capture The Flag (CTF) practice
Authorised penetration testing

🚫 Do NOT use this tool on networks you do not own or have explicit permission to test.
Unauthorised usage may violate laws in your country.

🎯 Learning Objectives
This project demonstrates understanding of:
Wireless security concepts
WPA/WPA2 authentication process
Handshake capturing
Deauthentication mechanism
Wordlist-based cracking
Linux networking tools
Subprocess handling in Python
CLI application design

🧠 Future Improvements
Logging system
Automatic handshake detection
Better error handling
GUI version (Tkinter or PyQt)
Report generation
Multi-threaded cracking support

👨‍💻 Author
WaaduHeck
Cybersecurity Student
Focused on Ethical Hacking & Penetration Testing
