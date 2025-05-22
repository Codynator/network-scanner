"""
Network Scanner - simple GUI application written in Python designed for scanning local networks.
MIT License

Copyright (c) 2025 Nataniel Krzempek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from customtkinter import CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, set_appearance_mode, CTkCheckBox, set_widget_scaling, set_window_scaling
from webbrowser import open as wb_open


class SettingsFrame(CTkFrame):
    """
    Frame containing different configuration options.
    """
    def __init__(self, master) -> None:
        super().__init__(master)

        self.columnconfigure(0, weight=1)

        self.headerLabel = CTkLabel(self, text="Settings", font=("", 16))
        self.headerLabel.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.strictCheckCheckBox = CTkCheckBox(self, text="Strict check", onvalue=True, offvalue=False)
        self.strictCheckCheckBox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.strictCheckCheckBox.select()

        self.useMultipleThreadsCheckBox = CTkCheckBox(self, text="Use multiple threads", onvalue=True, offvalue=False)
        self.useMultipleThreadsCheckBox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.useMultipleThreadsCheckBox.select()

        self.themeLabel = CTkLabel(self, text="Current theme:")
        self.themeLabel.grid(row=3, column=0, padx=10, pady=0, sticky="ew")
        self.themeMenu = CTkOptionMenu(self, values=['System', 'Light', 'Dark'], command=self.theme_change)
        self.themeMenu.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.scaleLabel = CTkLabel(self, text="Interface scale:")
        self.scaleLabel.grid(row=5, column=0, padx=10, pady=0, sticky="ew")
        self.scaleMenu = CTkOptionMenu(self, values=["100%", "110%", "125%", "150%"], command=self.scale_change)
        self.scaleMenu.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")

    @staticmethod
    def theme_change(theme: str) -> None:
        set_appearance_mode(theme)

    @staticmethod
    def scale_change(scale: str) -> None:
        parsed_scale: float = int(scale[:-1]) / 100
        set_widget_scaling(parsed_scale)
        set_window_scaling(parsed_scale)


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

        self.creditButton = CTkButton(self, text="Created by\nNataniel Krzempek", fg_color="transparent",
                                      text_color=("black", "white"), command=lambda:
                                      wb_open("https://github.com/Codynator/network-scanner", new=2))
        self.creditButton.grid(row=7, column=0, padx=10, pady=10, sticky="ew")
