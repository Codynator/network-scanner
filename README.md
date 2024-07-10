<figcaption style="text-align: center">
    <img src="./public/logo.png">
</figcaption>


# Network Scanner

An easy-to-use network scanner that pings IP addresses from designated range. Supports both IPv4 and IPv6.
Supports Linux and Windows (has been tested on Ubuntu 24.04 and Windows 10 and Windows 11). 
GUI created using [CustomTkinter](https://customtkinter.tomschimansky.com/) module.

![example 1](./public/dark_theme.png)
![example 2](./public/light_theme.png)

## Getting started

1. Download or clone the repository.
2. Open in terminal repository's localization and run following command to install required modules:  
 `pip install -r requirements.txt`  
  **You can delete specific module version in `requirements.txt` so that pip installs the latest version.**
3. You're ready to go!

## How to use
1. The scanner should recognize the OS and set a proper ping command by default. If that didn't work you can set the OS
manually or edit the command visible in the entry on the right.
2. Designate a range of IP addresses. Entries accept both IPv4 and any IPv6 formats but remember to **use the same format
in both entries!** Otherwise, the scan may fail.
3. **Optional:** You can force conversion of found IP addresses to chosen IPv6 format.
4. Press scan button. If the designated range is large, scanning may take few minutes.
5. When scan is finished, you can copy each of addresses. You can also save them to txt file by pressing `Save result`
button.

> When `Always save result` is checked, the scanner saves the result after each scan. **It doesn't save when you check
or uncheck it**.

### Ping command flags explanation

| Flag on Windows      | Flag on Linux | Description                    |
|----------------------|---------------|--------------------------------|
| -n [number]          | -c [number]   | Number of packets send to host |
| -w [milliseconds]    | -w [seconds]  | Length of timeout              |


## Knows issues
1. When the program is clearing the list of found IP addresses, it can throw *CustomTkinter*'s errors in the terminal.
They shouldn't have any impact on the scanner's workflow.
2. On Windows: GUI can look glitched.