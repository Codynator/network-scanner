from customtkinter import CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, set_appearance_mode
from webbrowser import open as wb_open


class HeaderFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.title = CTkLabel(self, text="Network Scanner", font=("", 20))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.subtitle = CTkLabel(self, text="Version 0.17")
        self.subtitle.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.themeLabel = CTkLabel(self, text="Current theme:")
        self.themeLabel.grid(row=3, column=0, padx=10, pady=0, sticky="ew")
        self.themeMenu = CTkOptionMenu(self, values=['System', 'Light', 'Dark'], command=self.theme_change)
        self.themeMenu.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.creditButton = CTkButton(self, text="Created by Codynator", fg_color="transparent",
                                      text_color=("black", "white"), command=lambda:
                                      wb_open("https://github.com/Codynator/network-scanner", new=2))
        self.creditButton.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    @staticmethod
    def theme_change(theme: str):
        set_appearance_mode(theme)
