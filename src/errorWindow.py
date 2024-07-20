from customtkinter import CTkToplevel, CTkLabel, CTkButton


class ErrorWindow(CTkToplevel):
    def __init__(self, err_msg: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x150")
        self.title("Error!")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.msgLabel = CTkLabel(self, text=err_msg, font=("", 15))
        self.msgLabel.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        self.closeButton = CTkButton(self, text="Close", command=self.destroy)
        self.closeButton.grid(row=1, column=0, padx=10, pady=10, sticky="we")
