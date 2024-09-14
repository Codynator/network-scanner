from customtkinter import CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, set_appearance_mode, CTkCheckBox
from webbrowser import open as wb_open


class SettingsFrame(CTkFrame):
    """
    Frame containing different configuration options.
    """
    def __init__(self, master) -> None:
        super().__init__(master)

        self.columnconfigure(0, weight=1)

        self.headerLabel = CTkLabel(self, text="Options", font=("", 16))
        self.headerLabel.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.strictCheckCheckBox = CTkCheckBox(self, text="Strict check", onvalue=True, offvalue=False)
        self.strictCheckCheckBox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.strictCheckCheckBox.select()

        self.useMultipleThreadsCheckBox = CTkCheckBox(self, text="Use multiple threads", onvalue=True, offvalue=False)
        self.useMultipleThreadsCheckBox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.useMultipleThreadsCheckBox.select()


class HeaderFrame(CTkFrame):
    """
    Frame that contains: application title, version and possibility to change appearance mode.
    """
    def __init__(self, master) -> None:
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((2, 4), weight=1)

        self.title = CTkLabel(self, text="Network Scanner", font=("", 20))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.subtitle = CTkLabel(self)
        self.subtitle.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.settingsFrame = SettingsFrame(self)
        self.settingsFrame.grid(row=3, column=0, padx=0, pady=0, sticky="nsew")
        self.settingsFrame.configure(fg_color="transparent")

        self.themeLabel = CTkLabel(self, text="Current theme:")
        self.themeLabel.grid(row=5, column=0, padx=10, pady=0, sticky="ew")
        self.themeMenu = CTkOptionMenu(self, values=['System', 'Light', 'Dark'], command=self.theme_change)
        self.themeMenu.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.creditButton = CTkButton(self, text="Created by Codynator", fg_color="transparent",
                                      text_color=("black", "white"), command=lambda:
                                      wb_open("https://github.com/Codynator/network-scanner", new=2))
        self.creditButton.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

    @staticmethod
    def theme_change(theme: str) -> None:
        set_appearance_mode(theme)
