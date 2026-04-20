import nmap
from typing import Iterable

import argparse

nm = nmap.PortScanner()

def parse_ports(ports_str: str) -> list[int]:
    result = []
    for part in ports_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    return sorted(list(set(result)))

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

def main():
    parser = argparse.ArgumentParser(description="Python-Nmap Port Scanner")
    parser.add_argument("--host", type=str, default="localhost", help="Target host (default: localhost)")
    parser.add_argument("--ports", type=str, help="Ports to scan (e.g., 80,443 or 20-1024)")

    args = parser.parse_args()

    if args.ports:
        ports_list = parse_ports(args.ports)
    else:
        ports_list = list(range(1, 1025))

    scan_ports(host=args.host, ports=ports_list)

if __name__ == '__main__':
    main()