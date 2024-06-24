import customtkinter as ctk
from threading import Thread
from headerFrame import HeaderFrame
from mainFrame import MainFrame
from resultFrame import ResultFrame

"""
TODO:
1. DOCUMENTATION AND MORE COMMENTS!
2. fix UI
"""

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Network scanner')
        self.geometry('900x520')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.headerFrame = HeaderFrame(self)
        self.headerFrame.grid(row=0, column=0, padx=0, rowspan=2, pady=0, sticky="nsew")

        self.mainFrame = MainFrame(self)
        self.mainFrame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.mainFrame.configure(fg_color="transparent")
        self.mainFrame.scanButton.configure(command=self.start_work)

        self.resultFrame = ResultFrame(self, title="List of found IP addresses", fg_color="transparent",
                                       border_width=2, border_color=("grey80", "grey20"))
        self.resultFrame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.records: list = []

    def clear_records(self) -> None:
        # Clears resultFrame from labels and buttons
        for record in self.records:
            record[0].destroy()
            record[1].destroy()

        self.records = []

    def start_work(self) -> None:
        # Start scanning on different thread because it won't interfere with GUI's thread
        Thread(target=self.start_scan).start()

    def start_scan(self):
        self.clear_records()

        found_addresses: set = self.mainFrame.start_scan()

        for i, address in enumerate(found_addresses):
            new_label = ctk.CTkLabel(self.resultFrame, text=f"{address}")
            new_label.grid(row=i, column=0, padx=10, pady=(5, 0), sticky="w")

            new_copy_button = ctk.CTkButton(self.resultFrame, text="Copy to clipboard", command=lambda:
                                            self.clipboard_append(address))
            new_copy_button.grid(row=i, column=1, padx=0, pady=(5, 0), sticky="w")
            self.records.append([new_label, new_copy_button])

    def refresh_ui(self):
        self.update()
        self.after(1000, self.refresh_ui)


if __name__ == '__main__':
    app: ctk.CTk = App()
    app.mainloop()
