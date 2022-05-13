"""
Original repository link: https://github.com/Jiusoft/webx
Author: Jothin kumar (https://jothin.tech/)
"""
import tkinter as tk
from tkinter.messagebox import showerror
from time import sleep
from threading import Thread
from requests import get
from os import system
from hashlib import sha256
from datetime import datetime

root = tk.Tk()
root.overrideredirect(True)
root.wm_title('Webx - Jiusoft')
root.resizable(False, False)
root.geometry(f'500x300+{int(root.winfo_screenwidth()/2) - 250}+{int(root.winfo_screenheight()/2) - 150}')
title = tk.Label(root, text='Webx - Jiusoft', font=('Ariel', 25), fg='white')
title.pack(pady=90)
status_label = tk.Label(text='Loading...', fg='white')
status_label.pack(pady=10)

def log(message):
    with open('launcher-logs.txt', 'a+') as log_file:
        now = datetime.now()
        log_file.write(f'{now.year}:{now.month}:{now.day}:{now.hour}:{now.minute}:{now.second} | {message}\n')

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb
def background_color_animation():
    while True:
        for g in range(0, 200):
            background = rgb_to_hex((150, g, 100))
            root.configure(background=background)
            title.configure(background=background)
            status_label.configure(background=background)
            sleep(0.03)
        for g in reversed(range(0, 200)):
            background = rgb_to_hex((150, g, 100))
            root.configure(background=background)
            title.configure(background=background)
            status_label.configure(background=background)
            sleep(0.03)
Thread(target=background_color_animation).start()

def launch_webx():
    status_label.configure(text='Verifying hashes...')
    log('Hash verification triggered')
    try:
        file_hashes_data = get('https://raw.githubusercontent.com/Jiusoft/webx/main/file-hashes.txt').text
    except Exception as e:
        log(f'Failed to fetch file hashes: {e}')
        showerror(title='Error - WebX launcher', message='An error occurred while trying to fetch file hashes. Make sure that you are connected to the internet and try again.')
        exit(1)
    num_of_files = len(file_hashes_data.split('\n')) - 1
    num_of_files_verified = 0
    status_label.configure(text=f'Verifying hashes... [{num_of_files_verified}/{num_of_files}]')

    class FileHash:
        def __init__(self, string):
            self.url = string.split('||')[0].strip()
            self.hash_ = string.split('||')[-1].strip()
            self.path = self.url.replace('https://raw.githubusercontent.com/Jiusoft/webx/main/scripts/', '')

    for line in file_hashes_data.split('\n'):
        if line:
            num_of_files_verified += 1
            status_label.configure(text=f'Verifying hashes... [{num_of_files_verified}/{num_of_files}]')
            file = FileHash(line)
            with open(file.path, 'rb') as file_content:
                if sha256(file_content.read()).hexdigest() != file.hash_:
                    log(f'{file.path} hash mismatched. {file.path} hash: {file.hash_}')
                    with open(file.path, 'wb') as _:
                        try:
                            _.write(get(file.url).content)
                            log(f'{file.path} replaced from {file.url}')
                        except Exception as e:
                            log(f'Failed to fetch {file.url}: {e}')
                            showerror(title='Error - WebX launcher', message=f'An error occurred while fetching {file.url}. Mkae sure that you are connected to the internet and try again.')
                            exit(1)

    root.withdraw()
    if system('cd webx && python3 main.py'):
        log('Event: Launch failed')
        root.deiconify()
        status_label.configure(text='Launch failed.')
        showerror(title='Error - WebX Launcher', message='Failed to launch WebX. Check log file for more info.')
        exit(1)
    log('Event: Launcher exit')
    exit(0)
Thread(target=launch_webx).start()

root.mainloop()
