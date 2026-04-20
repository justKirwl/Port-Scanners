# Python Port Scanner Suite

A powerful collection of port scanning implementations in Python. This suite allows you to choose between a raw socket-based approach (using Asyncio or Threads) and a professional-grade scanner powered by the `nmap` library.

## 🚀 Features

- **Multiple Modes**: Choose between `Nmap-library`, `Asyncio`, or `Multithreaded` engines.
- **Advanced CLI**: Fully controlled via command-line arguments.
- **Flexible Port Selection**: Supports single ports, comma-separated lists, and ranges (e.g., `80,443,1000-2000`).
- **Beautiful UI**: Results are displayed in clean, formatted tables using `tabulate`.
- **Colored Output**: Visual status indicators for better readability.

## 🛠 Prerequisites

### System Requirements
To use the **Library (Nmap) version**, you must have Nmap installed:
- **Linux**: `sudo apt install nmap`
- **macOS**: `brew install nmap`
- **Windows**: [nmap.org/download.html](https://nmap.org)

### Python Dependencies
```bash
pip install python-nmap tabulate
```
📖 Usage
1. Library Version (Recommended)
The nmap_scanner.py uses the official Nmap engine. It is faster, more accurate, and provides more reliable state detection than raw socket scripts.
bash
python nmap_scanner.py --host scanme.nmap.org --ports 22,80,443
2. Raw Versions (Async/Threads)
For lightweight scanning without external dependencies (except tabulate):
bash
# Using Asyncio (default)
python scanner.py --host 192.168.1.1 --ports 1-1024 --mode async

# Using Threads
python scanner.py --host 127.0.0.1 --ports 80,443,8080 --mode thread
⚙️ Arguments
Argument	Description	Example
--host	Target IP or domain	--host google.com
--ports	Ports, lists, or ranges	--ports 80,443,1-100
--mode	Engine (for raw version)	--mode async or thread
💡 Which one to use?
Use the Nmap Library version for professional network auditing. It handles complex network conditions and provides the most precise results.
Use Raw versions for learning purposes or when you need a quick, standalone script without installing the Nmap binary.

⚠️ Disclaimer
This tool is for educational and ethical testing purposes only. Scanning targets without prior authorization is illegal and unethical. Use it responsibly on your own hardware or authorized environments (like scanme.nmap.org).

📝 License
This project is licensed under the MIT License.