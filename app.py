import customtkinter as ctk
from webbrowser import open as wb_open


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self, text="Network Scanner", font=("", 20))
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.subtitle = ctk.CTkLabel(self, text="Version 0.11")
        self.subtitle.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.spacer = ctk.CTkLabel(self, text="")
        self.spacer.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")

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

        self.osLabel = ctk.CTkLabel(self, text="Choose your OS:")
        self.osLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.osMenu = ctk.CTkOptionMenu(self, values=['Linux', 'Windows'], command=self.set_preview_command)
        self.osMenu.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        self.previewLabel = ctk.CTkLabel(self, text="Command preview:")
        self.previewLabel.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        self.previewEntry = ctk.CTkEntry(self)
        self.previewEntry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="w")
        self.previewEntry.insert(0, "ping -c 1 -w 3")

        self.patternLabel = ctk.CTkLabel(self, text="IP pattern:")
        self.patternLabel.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="w")
        self.patternEntry = ctk.CTkEntry(self, placeholder_text="192.168.1.0")
        self.patternEntry.grid(row=1, column=2, padx=10, pady=(0, 10), sticky="w")

        # self.searchButton = ctk.CTkButton(self, text="Scan")

    @staticmethod
    def clear_entry(_entry: ctk.CTkEntry):
        _entry.delete(0, len(_entry.get()))

    def set_preview_command(self, os_name: str):
        self.clear_entry(self.previewEntry)

        if os_name == "Linux":
            self.previewEntry.insert(0, "ping -c 1 -w 3")
        else:
            self.previewEntry.insert(0, "ping -n 1 -w 3000")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Network scanner')
        self.geometry('800x400')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.headerFrame = HeaderFrame(self)
        self.headerFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.mainFrame = MainFrame(self)
        self.mainFrame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.mainFrame.configure(fg_color="transparent")


if __name__ == '__main__':
    app: ctk.CTk = App()
    app.mainloop()
