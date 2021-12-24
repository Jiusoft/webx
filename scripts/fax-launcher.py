"""
Original repository link: https://github.com/Jiusoft/fax-browser
Author: Jothin kumar (https://jothin-kumar.github.io)
"""
import tkinter as tk
from time import sleep
from threading import Thread
from requests import get
from datetime import datetime

version = '1.0.0'

root = tk.Tk()
root.overrideredirect(True)
root.geometry(f'400x200+{int(root.winfo_screenwidth() / 2) - 200}+{int(root.winfo_screenheight() / 2 - 100)}')
root.configure(background='green')
tk.Label(master=root, text='FAX browser', font=('Ariel', 30), bg='green').pack()
tk.Label(master=root, text='By Jiusoft', font=('Ariel', 20), bg='green').pack()
progress_label = tk.Label(master=root, text='', font=('Ariel', 15), bg='green')
progress_label.pack(side=tk.BOTTOM)


def log(message):
    now = datetime.now()
    with open('launcher-logs.txt', 'a+') as log_file:
        log_file.write(f'[{now.year}:{now.month}:{now.day}:{now.hour}:{now.minute}:{now.second}]: {message}\n')


def in_progress_msg(msg):
    def command():
        progress_label['text'] = msg
        while True:
            sleep(0.5)
            if progress_label['text'] in [msg, msg + '.', msg + '..']:
                progress_label['text'] += '.'
            elif progress_label['text'] == msg + '...':
                progress_label['text'] = msg
            else:
                break

    Thread(target=command).start()


def check_for_updates():
    in_progress_msg('Checking for updates')
    latest_version = get('https://cdn.jiu-soft.com/fax-browser/latest-version.txt').text.strip('\n')
    log(f'lv - {latest_version}')
    return latest_version != version


def download_update():
    in_progress_msg('Downloading update')
    with open('update_temp.zip', 'wb') as file:
        file.write(get('https://cdn.jiu-soft.com/fax-browser/fax-browser-files.zip', allow_redirects=True).content)


Thread(target=check_for_updates).start()
root.mainloop()
