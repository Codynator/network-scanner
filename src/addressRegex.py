from re import match


def is_proper_format(adr: str):
    ipv4_regex: str = r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"
    ipv6_regex: str = r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$"
    ipv6_comp_regex: str = r"^::([0-9a-fA-F]{1,4}:){2}[0-9a-fA-F]{1,4}$"

    if match(ipv4_regex, adr) or match(ipv6_regex, adr) or match(ipv6_comp_regex, adr):
        return True
    else:
        return False
