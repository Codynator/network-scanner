from customtkinter import CTkFrame, CTkLabel, CTkOptionMenu, CTkEntry, CTkButton, CTkProgressBar, CTkCheckBox
from subprocess import run, CalledProcessError, CompletedProcess
from concurrent.futures import ThreadPoolExecutor, as_completed
from netaddr import IPSet, IPRange, AddrFormatError


class MainFrame(CTkFrame):
    """
    Main frame containing the parameters for application. It is responsible for the scanning process.
    """
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(2, weight=1)

        self.osLabel = CTkLabel(self, text="Choose your OS:")
        self.osLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.osMenu = CTkOptionMenu(self, values=['Linux', 'Windows'], command=self.set_preview_command)
        self.osMenu.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="we")

        self.previewLabel = CTkLabel(self, text="Command preview:")
        self.previewLabel.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        self.previewEntry = CTkEntry(self)
        self.previewEntry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="we")
        self.previewEntry.insert(0, "ping -c 1 -w 3")

        self.alwaysSaveResultCheckbox = CTkCheckBox(self, text="Always save result", onvalue=True, offvalue=False)
        self.alwaysSaveResultCheckbox.grid(row=2, column=3, padx=10, pady=10, sticky="e")

        self.addressesRangeLabel = CTkLabel(self, text="Designate a range of IP addresses to scan",
                                            fg_color=("grey80", "grey20"), corner_radius=10)
        self.addressesRangeLabel.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="we")
        self.rangeFromEntry = CTkEntry(self, placeholder_text="from, e.g.: 192.168.1.0")
        self.rangeFromEntry.grid(row=3, column=0, padx=10, pady=10, sticky="we")
        self.rangeFromEntry.insert(0, "192.168.1.0")
        self.rangeToEntry = CTkEntry(self, placeholder_text="to, e.g.: 192.168.1.10")
        self.rangeToEntry.grid(row=3, column=1, padx=10, pady=10, sticky="we")
        self.rangeToEntry.insert(0, "192.168.1.10")

        self.saveResultButton = CTkButton(self, text="Save result", state="disabled")
        self.saveResultButton.grid(row=3, column=3, padx=10, pady=10, sticky="we")

        self.scanButton = CTkButton(self, text="Scan")
        self.scanButton.grid(row=4, column=0, padx=10, pady=10, sticky="we")

        self.scanProgressbar = CTkProgressBar(self)
        self.scanProgressbar.grid(row=4, column=1, columnspan=3, padx=(10, 10), pady=(20, 0), sticky="we")
        self.scanProgressbar.set(0)

        self.scanProgressLabel = CTkLabel(self, text="0%")
        self.scanProgressLabel.grid(row=4, column=1, columnspan=3, padx=10, pady=(0, 20), sticky="we")

    @staticmethod
    def clear_entry(_entry: CTkEntry) -> None:
        _entry.delete(0, len(_entry.get()))

    def set_preview_command(self, os_name: str) -> None:
        self.clear_entry(self.previewEntry)

        if os_name == "Linux":
            self.previewEntry.insert(0, "ping -c 1 -w 3")
        else:
            self.previewEntry.insert(0, "ping -n 1 -w 3000 -4")

    def get_command(self) -> list[str]:
        new_command: str = self.previewEntry.get()
        return new_command.split(" ")

    def ping(self, _host: str) -> tuple[str, bool]:
        command: list[str] = [*self.get_command(), _host]

        try:
            output: CompletedProcess = run(command, capture_output=True, text=True, check=True)
            if "unreachable" in output.stdout.strip().lower() or output.returncode != 0:
                return _host, False

            return _host, True
        except CalledProcessError:
            return _host, False

    def start_scan(self) -> set[str]:
        """
        Gets the set of all IP addresses from given range and then pings them on multiple threads. It also disables the
        scan button and updates the progressbar.
        :return: set containing all found IP addresses
        """
        self.scanButton.configure(state="disabled")

        ip1: str = self.rangeFromEntry.get()
        ip2: str = self.rangeToEntry.get()

        try:
            ip_addresses: IPSet = IPSet(IPRange(ip1, ip2))
        except AddrFormatError:
            ip_addresses: IPSet = IPSet(IPRange(ip2, ip1))

        ip_addresses_set: set = set()
        for ip in ip_addresses:
            ip_addresses_set.add(str(ip))

        available_addresses = set()

        self.scanProgressbar.set(0)
        increase_value_by: float = 1 / len(ip_addresses_set)

        with ThreadPoolExecutor() as executor:
            futures: set = {executor.submit(self.ping, host) for host in ip_addresses_set}
            for future in as_completed(futures):
                if future.result()[1]:
                    print(f"Found IP: {future.result()[0]}")
                    available_addresses.add(future.result()[0])

                new_value = self.scanProgressbar.get() + increase_value_by
                self.scanProgressbar.set(new_value)
                self.scanProgressLabel.configure(text=f"{int(new_value * 100)}%")

        self.scanProgressbar.set(1)
        self.scanProgressLabel.configure(text="100%")
        self.scanButton.configure(state="normal")
        self.saveResultButton.configure(state="normal")
        return available_addresses
