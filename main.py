from subprocess import run


def check_range(pattern: list[int], position: int = -1, start_val: int = 0, end_val: int = 1) -> None:
    if start_val >= end_val:
        end_val = start_val + 1

    for _i in range(start_val, end_val):
        pattern[position] = _i
        print(linux_ping('.'.join(map(str, pattern))))


def linux_ping(host):
    command: list[str] = ['ping', '-c', '1', host]
    return run(command, capture_output=True, text=True).stdout


if __name__ == '__main__':
    ipPattern: list[int] = [192, 168, 1, 1]
    check_range(ipPattern, position=-1, start_val=0, end_val=10)
