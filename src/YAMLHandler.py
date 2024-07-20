from yaml import safe_load


def read_from_yaml(target: str = "version") -> str | dict:
    try:
        with open("./conf.yaml", "r") as file:
            return safe_load(file)[target]
    except FileNotFoundError:
        return "not found"
