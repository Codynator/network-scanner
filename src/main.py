from customtkinter import CTk, CTkLabel, CTkButton, set_appearance_mode, set_default_color_theme, CTkFont
from threading import Thread
from headerFrame import HeaderFrame
from mainFrame import MainFrame
from resultFrame import ResultFrame
from math import ceil
from datetime import datetime
from OSadaptationHandler import get_mono_font


set_appearance_mode("System")
set_default_color_theme("green")


class App(CTk):
    """
    Core object of the whole application. Combines all frames together and is responsible for scanning process.
    """
    def __init__(self) -> None:
        super().__init__()

        self.title('Network scanner')
        self.geometry('900x520')
        self.minsize(800, 500)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.monoFont = CTkFont(family=get_mono_font(), size=12)

        self.headerFrame = HeaderFrame(self)
        self.headerFrame.grid(row=0, column=0, padx=0, rowspan=2, pady=0, sticky="nsew")

        self.mainFrame = MainFrame(self)
        self.mainFrame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.mainFrame.configure(fg_color="transparent")
        self.mainFrame.scanButton.configure(command=self.start_work)
        self.mainFrame.saveResultButton.configure(command=self.save_result)

        self.resultFrame = ResultFrame(self, title="List of found IP addresses", fg_color=("white", "black"),
                                       border_width=2, border_color=("grey80", "grey20"))
        self.resultFrame.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nsew")
        self.records: list = []
        self.found_addresses: set = set()

    def clear_records(self) -> None:
        """
        Clears the resultFrame from all labels and buttons. Currently, this function can throw errors due to widget
        removing mechanism, but they have no impact on the performance of the application.
        :return: None
        """
        for record in self.records:
            record[0].destroy()
            record[1].destroy()

        self.records = []

    def start_work(self) -> None:
        """
        Starts the start_scan function on different thread because otherwise it would interfere with CTk thread.
        :return: None
        """
        Thread(target=self.start_scan).start()

    def start_scan(self) -> None:
        """
        Starts the mainFrames method start_scan and changes the appearance of the UI for the duration of scanning.
        :return: None
        """
        self.title("(Scanning...) Network Scanner")
        self.clear_records()

        self.found_addresses = self.mainFrame.start_scan()

        if _format := self.mainFrame.get_format():
            formatted_addresses: set = set()

            for address in self.found_addresses:
                address = self.mainFrame.convert_to_ipv6(address, _format)
                formatted_addresses.add(address)

            self.found_addresses = set(formatted_addresses)

        self.create_records_grid(self.found_addresses, 2)
        self.title("Network Scanner")

        if self.mainFrame.alwaysSaveResultCheckbox.get():
            self.save_result()

    def refresh_ui(self) -> None:
        self.update()
        self.after(1000, self.refresh_ui)

    def clipboard_handler(self, _val) -> None:
        self.clipboard_clear()
        self.clipboard_append(_val)

    def create_copy_button_handler(self, _val) -> clipboard_handler:
        return lambda: self.clipboard_handler(_val)

    def create_records_grid(self, data: set, cols: int) -> None:
        """
        Creates a grid for labels and buttons. Each label has its own button.
        :param data: 1D set containing all found IP addresses
        :param cols: amount of columns containing labels in one row (columns for button are created automatically)
        :return: None
        """
        parsed_data: list = list(data)
        rows = ceil(len(parsed_data) / cols)
        modified_data: list = [parsed_data[i * cols: (i + 1) * cols] for i in range(rows)]

        col_indexes: list = [i for i in range(cols * 2)]
        self.resultFrame.columnconfigure(tuple(col_indexes), weight=1)

        for _row, _row_list in enumerate(modified_data):
            for _col, _val in enumerate(_row_list):
                new_label = CTkLabel(self.resultFrame, text=f"> {_val}", font=self.monoFont,
                                     text_color=("green", "green2"))
                new_label.grid(row=_row, column=_col * 2, padx=10, pady=(5, 0), sticky="w")

                new_copy_button = CTkButton(self.resultFrame, text="Copy",
                                            command=self.create_copy_button_handler(_val),
                                            font=self.monoFont, fg_color="transparent",
                                            text_color=("black", "white"),
                                            corner_radius=0,
                                            hover_color=("green2", "green"))
                new_copy_button.grid(row=_row, column=_col * 2 + 1, padx=0, pady=(5, 0), sticky="w")
                self.records.append([new_label, new_copy_button])

    def save_result(self):
        current_date = datetime.now()
        new_file_name = f"network_scan_{current_date:%Y-%m-%d_%H-%M-%S}.txt"

        with open(new_file_name, "w") as file:
            for address in list(self.found_addresses):
                file.write(address + "\n")


if __name__ == '__main__':
    app: CTk = App()
    app.mainloop()
