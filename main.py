from subprocess import run, CalledProcessError, CompletedProcess
from concurrent.futures import ThreadPoolExecutor, as_completed


def return_range(pattern: list[int], position: int = -1, start_val: int = 0, end_val: int = 1) -> set[str]:
    if start_val >= end_val:
        end_val = start_val + 1

    commands: set = set()

    for _i in range(start_val, end_val):
        pattern[position] = _i
        commands.add('.'.join(map(str, pattern)))

    return commands


def linux_ping(_host: str) -> tuple[str, bool]:
    command: list[str] = ['ping', '-c', '1', '-w', '3', _host]
    try:
        output: CompletedProcess = run(command, capture_output=True, text=True, check=True)
        return (_host, True) if output.returncode == 0 else (_host, False)
    except CalledProcessError:
        return _host, False


if __name__ == '__main__':
    ipPattern: list[int] = [192, 168, 1, 1]
    ipAddresses: set[str] = return_range(ipPattern, end_val=10)
    pingsResult: set[tuple] = set()
    blacklist: set[str] = set()

    addToBlacklist: bool = input("Do you want to add IPs to a blacklist? (y/n) ").lower().startswith('y')
    if addToBlacklist:
        numOfIPs: int = int(input('Input a number of addresses to blacklist: '))
        for i in range(numOfIPs):
            blacklist.add(input(f'{i + 1}. '))

    ipAddresses = ipAddresses - blacklist

    with ThreadPoolExecutor() as executor:
        futures: set = {executor.submit(linux_ping, host) for host in ipAddresses}
        for future in as_completed(futures):
            pingsResult.add(future.result())

    for result in pingsResult:
        print(result)
