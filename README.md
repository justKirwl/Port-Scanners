# Python Port Scanner Suite

A collection of three different port scanner implementations in Python. This project demonstrates various networking approaches, ranging from low-level socket programming to high-level asynchronous I/O and integration with industry-standard tools.

## 🚀 Features

The suite includes three distinct scanning methods:

1.  **Nmap-Based**: Leveraging the power of `python-nmap` for robust and detailed network analysis.
2.  **Multithreaded (ThreadPool)**: High-speed scanning using `concurrent.futures` to manage multiple socket connections simultaneously.
3.  **Asynchronous (Asyncio)**: A modern, non-blocking approach using `asyncio` and `Semaphores` for efficient resource management.

## 🛠 Prerequisites

### System Requirements
To use the **Nmap version**, you must have Nmap installed on your system:
- **Linux**: `sudo apt install nmap`
- **macOS**: `brew install nmap`
- **Windows**: Download from [nmap.org](https://nmap.org)

### Python Dependencies
Install the required libraries via pip:
```bash
pip install python-nmap tabulate
```

📊 Comparison of Methods
Method	Best For	Technology
Nmap	Accuracy & OS Detection	nmap binary wrapper
Threads	Stability & Simplicity	ThreadPoolExecutor
Asyncio	Scalability & Performance	asyncio + Sockets

🎨 UI & Presentation
All scanners feature:
Colored Output: Highlighting open ports for better readability.
Tabular Data: Results are neatly organized using the tabulate library with rounded grid styles.

⚠️ Disclaimer
This tool is for educational and ethical testing purposes only. Scanning targets without prior authorization is illegal and unethical. Use it responsibly on your own hardware or authorized environments (like scanme.nmap.org).

📝 License
This project is licensed under the MIT License.