import nmap
from typing import Iterable

nm = nmap.PortScanner()

def scan_ports(ports: Iterable[int] = [], host: str = 'localhost', colored_output: bool = True) -> None:
    BLUE = '\033[94m' if colored_output else ''
    GREEN = '\033[92m' if colored_output else ''
    BLACK_ON_BLUE = '\033[34m' if colored_output else ''
    RESET = '\033[0m' if colored_output else ''

    nm.scan(host, ",".join([str(port) for port in ports]) if ports else None)

    for host in nm.all_hosts():
        print('-' * 30)
        print(f"Host: {BLUE}{host}{RESET}")
        print(f"State: {nm[host].state()}")

        for proto in nm[host].all_protocols():
            print('-' * 15)
            print(f'Protocol: {proto}')

            lport: list[int] = list(nm[host][proto].keys())
            lport.sort()
            for port in lport:
                state = nm[host][proto][port]['state']
                print(f'port : {GREEN}{port}{RESET}  state: {BLACK_ON_BLUE}{state}{RESET}')