from concurrent.futures import ThreadPoolExecutor
import socket

import asyncio
import tabulate

from typing import Iterable

GREEN = '\033[92m'
BLUE = '\033[94m'
PURPLE = '\033[35m'
RESET = '\033[0m'
BLACK_ON_BLUE = '\033[34m'

def get_service_name(port: int) -> str:
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"

def check_port(args: tuple[str, int]) -> tuple[int, bool] | list[str]:
    host, port = args
    try:
        with socket.create_connection((host, port), timeout=2):
            return [f'{PURPLE}{get_service_name(port)}{RESET}', f"{GREEN}{port}{RESET}", f"{BLUE}open{RESET}"]
    except (ConnectionRefusedError, socket.timeout, OSError):
        return port, False

def scan_ports(ports: Iterable[int] = [], host: str = 'localhost') -> None:
    try:
        if not ports:
            ports = range(1, 1024 + 1)

        print('-' * 30)
        print(f"Host: {BLUE}{host}{RESET}")

        try:
            socket.gethostbyname(host)
            print('State: up')
        except socket.gaierror:
            print('State: down (Host not found)')
            return

        with ThreadPoolExecutor(max_workers=100) as executor:
            results = list(executor.map(check_port, [(host, p) for p in ports]))

        table_data = [r for r in results if r and len(r) == 3]
    
        if table_data:
            print(tabulate.tabulate(table_data, headers=["Service", "Port", "State"], tablefmt="rounded_grid"))
        else:
            print("No open ports found.")

    except (KeyboardInterrupt, EOFError):
        return

async def async_scan_port(port: int, semaphore: asyncio.Semaphore, host: str = 'localhost') -> list[str] | None:
    async with semaphore:
        try:
            await asyncio.sleep(0.1)

            _, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=2)
            writer.close()
            await writer.wait_closed()
            return [f"{PURPLE}{get_service_name(port)}{RESET}", f"{GREEN}{port}{RESET}", f"{BLUE}open{RESET}"]
        except (KeyboardInterrupt, EOFError, OSError):
            return
    
async def async_main() -> None:
    host = 'scanme.nmap.org'
    ports = range(1, 1025)

    semaphore = asyncio.Semaphore(100)

    print('-' * 30)
    print(f"Host: {BLUE}{host}{RESET}")

    try:
        socket.gethostbyname(host)
        print(f'State: up')
    except socket.gaierror:
        print(f'State: down (Host not found)')
        return

    results = await asyncio.gather(*(async_scan_port(p, semaphore, host) for p in ports))

    table_data = [r for r in results if r]

    if table_data:
        print(tabulate.tabulate(table_data, headers=["Service", "Port", "State"], tablefmt="rounded_grid"))
    else:
        print("No open ports found.")