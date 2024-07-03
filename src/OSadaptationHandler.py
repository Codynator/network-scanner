from platform import system

os_name: str = system()
mono_font_family: str = "Cascadia Mono" if os_name == "Windows" else "Monospace"
os_list: list = ["Windows", "Linux"] if os_name == "Windows" else ["Linux", "Windows"]


def get_mono_font() -> str:
    return mono_font_family


def get_os_list() -> list[str]:
    return os_list
