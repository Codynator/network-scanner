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
