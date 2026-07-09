# paperweight 📋
A lightweight Python application that records your copying history.

Nothing is stored externally, and there is no "pin" feature. All your copied text vanishes when your computer turns off.

Allegedly, Windows' clipboard history is stored on the cloud, which can be potentially dangerous if copying sensitive information. So, I decided to opt out, and make my own local clipboard history app. 

This is not meant to be impressive, more of a practice repo for me to make good public content! Thank you for this opportunity, Hackclub!!

---
## Installation
1. Make sure your computer has Windows OS installed
2. Click on `paperweight.exe`
3. Click on the download symbol
<img width="134" height="53" alt="image" src="https://github.com/user-attachments/assets/e407bca3-99dd-4dc0-aef6-2792251dbb08" />

4. Launch paperweight.exe and enjoy!

If Windows attempts to "protect your PC", you can press "More info" and then "Run anyway". No, I'm not evil. 

## How to Use
The app tracks your copy activity. Ctrl+C anything, and it'll show up in the app! 
The exit button does not actually end the app process, the app tracks in the background too! To bring the window back up again, press Ctrl+Alt+V.

To actually end the app process, go to Task Manager, search for "paperweight", and end task.

If you don't want to manually launch the app all the time, you can make it a start up app. Follow these tutorials:

[Windows](https://support.microsoft.com/en-us/windows/experience/startup-boot/configure-startup-applications-in-windows)

[macOS](https://support.apple.com/en-ca/guide/mac-help/mh15189/mac)

For Linux, it depends on what distribution you have. Please research yourself, sorry 😿

## Editing The Code
1. Click on `paperweight.py`
2. Click on the download symbol (same as above)
3. Time to make a `venv`! Move `paperweight.py` into a project directory.

Go to your project directory and run these lines (in order)

Windows (Command Prompt):
```
python -m venv .venv
.venv\Scripts\activate.bat
```

macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```

You'll know it's activated when you see `(.venv)` at the beginning of the terminal line.

6. Using `pip`, install `pyperclip`, `customtkinter`, and `pynput`
7. Code to your heart's desire!!!
