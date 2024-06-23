import customtkinter as ctk
from webbrowser import open as wb_open
from subprocess import run, CalledProcessError, CompletedProcess
# from concurrent.futures import ThreadPoolExecutor, as_completed
from netaddr import IPSet, IPRange


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self, text="Network Scanner", font=("", 20))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.subtitle = ctk.CTkLabel(self, text="Version 0.14")
        self.subtitle.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.themeLabel = ctk.CTkLabel(self, text="Current theme:")
        self.themeLabel.grid(row=3, column=0, padx=10, pady=0, sticky="ew")
        self.themeMenu = ctk.CTkOptionMenu(self, values=['System', 'Light', 'Dark'],
                                           command=self.theme_change)
        self.themeMenu.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.creditButton = ctk.CTkButton(self, text="Created by Codynator", fg_color="transparent",
                                          text_color=("black", "white"), command=lambda:
                                          wb_open("https://github.com/Codynator/network-scanner", new=2))
        self.creditButton.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    @staticmethod
    def theme_change(theme: str):
        ctk.set_appearance_mode(theme)


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure((0, 1, 2), weight=1)

        self.osLabel = ctk.CTkLabel(self, text="Choose your OS:")
        self.osLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.osMenu = ctk.CTkOptionMenu(self, values=['Linux', 'Windows'], command=self.set_preview_command)
        self.osMenu.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="we")

        self.previewLabel = ctk.CTkLabel(self, text="Command preview:")
        self.previewLabel.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        self.previewEntry = ctk.CTkEntry(self)
        self.previewEntry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="we")
        self.previewEntry.insert(0, "ping -c 1 -w 3")

        self.addressesRangeLabel = ctk.CTkLabel(self, text="Designate a range of IP addresses to scan",
                                                fg_color=("grey80", "grey20"), corner_radius=10)
        self.addressesRangeLabel.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="we")
        self.rangeFromEntry = ctk.CTkEntry(self, placeholder_text="from, e.g.: 192.168.1.0")
        self.rangeFromEntry.grid(row=3, column=0, padx=10, pady=10, sticky="we")
        self.rangeFromEntry.insert(0, "192.168.1.0")
        self.rangeToEntry = ctk.CTkEntry(self, placeholder_text="to, e.g.: 192.168.1.10")
        self.rangeToEntry.grid(row=3, column=1, padx=10, pady=10, sticky="we")
        self.rangeToEntry.insert(0, "192.168.1.10")

        self.resultLabel = ctk.CTkLabel(self, text="")
        self.resultLabel.grid(row=3, column=2, padx=10, pady=10, sticky="we")

        self.scanButton = ctk.CTkButton(self, text="Scan")
        self.scanButton.grid(row=4, column=1, padx=10, pady=10, sticky="we")

    @staticmethod
    def clear_entry(_entry: ctk.CTkEntry) -> None:
        _entry.delete(0, len(_entry.get()))

    def set_preview_command(self, os_name: str) -> None:
        self.clear_entry(self.previewEntry)

        if os_name == "Linux":
            self.previewEntry.insert(0, "ping -c 1 -w 3")
        else:
            self.previewEntry.insert(0, "ping -n 1 -w 3000")

    def get_command(self) -> list[str]:
        new_command: str = self.previewEntry.get()
        return new_command.split(" ")

    def ping(self, _host: str) -> tuple[str, bool]:
        command: list[str] = [*self.get_command(), _host]

        try:
            output: CompletedProcess = run(command, capture_output=True, text=True, check=True)
            return (_host, True) if output.returncode == 0 else (_host, False)
        except CalledProcessError:
            return _host, False

    def start_scan(self) -> set:
        ip1: str = self.rangeFromEntry.get()
        ip2: str = self.rangeToEntry.get()

        ip_addresses: IPSet = IPSet(IPRange(ip1, ip2))
        ip_addresses_set: set = set()
        for ip in ip_addresses:
            ip_addresses_set.add(str(ip))

        available_addresses = set()

        for ip_address in ip_addresses_set:
            new_address = self.ping(ip_address)
            if new_address[1]:
                available_addresses.add(new_address[0])

        return available_addresses


class ResultFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, label_text=title, label_font=("", 15), **kwargs)
        self.columnconfigure(0, weight=1)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Network scanner')
        self.geometry('800x500')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.headerFrame = HeaderFrame(self)
        self.headerFrame.grid(row=0, column=0, padx=0, rowspan=2, pady=0, sticky="nsew")

        self.mainFrame = MainFrame(self)
        self.mainFrame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.mainFrame.configure(fg_color="transparent")
        self.mainFrame.scanButton.configure(command=self.start_scan)

        self.resultFrame = ResultFrame(self, title="List of found IP addresses", fg_color="transparent",
                                       border_width=2, border_color=("grey80", "grey20"))
        self.resultFrame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.records = []

    def clear_records(self):
        ...

    def start_scan(self):
        found_addresses = self.mainFrame.start_scan()

        for i, address in enumerate(found_addresses):
            new_label = ctk.CTkLabel(self.resultFrame, text=f"{address}")
            new_label.grid(row=i, column=0, padx=10, pady=(5, 0), sticky="w")

            new_copy_button = ctk.CTkButton(self.resultFrame, text="Copy to clipboard", command=lambda:
                                            self.clipboard_append(address))
            new_copy_button.grid(row=i, column=1, padx=0, pady=(5, 0), sticky="w")
            self.records.append([new_label, new_copy_button])

            self.clipboard_append(address)


if __name__ == '__main__':
    app: ctk.CTk = App()
    app.mainloop()
