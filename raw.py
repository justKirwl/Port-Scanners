from concurrent.futures import ThreadPoolExecutor
import socket

import asyncio
import tabulate

import argparse

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
        return None
    
def parse_ports(ports_str: str) -> list[int]:
    result = []
    for part in ports_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    return sorted(list(set(result)))
    
def run_threaded_scan(host: str, ports: list[int]) -> None:
    try:
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
        
        table_data = [r for r in results if r]
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
        
async def run_async_scan(host: str, ports: list[int]) -> None:
    try:
        print('-' * 30)
        print(f"Host: {BLUE}{host}{RESET}")

        try:
            socket.gethostbyname(host)
            print('State: up')
        except socket.gaierror:
            print('State: down (Host not found)')
            return

        semaphore = asyncio.Semaphore(100)
        tasks = [async_scan_port(p, semaphore, host) for p in ports]
        results = await asyncio.gather(*tasks)
        
        table_data = [r for r in results if r]
        if table_data:
            print(tabulate.tabulate(table_data, headers=["Service", "Port", "State"], tablefmt="rounded_grid"))
        else:
            print("No open ports found.")
    except (KeyboardInterrupt, EOFError):
        return
        
def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-mode Port Scanner")
    parser.add_argument("--host", type=str, default="localhost", help="Target host (default: localhost)")
    parser.add_argument("--ports", type=str, help="Ports to scan (e.g., 80,443 or 20-1024)")
    parser.add_argument("--mode", choices=['async', 'thread'], default='async', help="Scan mode")

    args = parser.parse_args()

    if args.ports:
        ports_list = parse_ports(args.ports)
    else:
        ports_list = list(range(1, 1025))

    if args.mode == 'async':
        asyncio.run(run_async_scan(args.host, ports_list))
    else:
        run_threaded_scan(args.host, ports_list)

if __name__ == '__main__':
    main()