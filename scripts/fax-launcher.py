import tkinter as tk
from time import sleep
from threading import Thread

root = tk.Tk()
root.overrideredirect(True)
root.geometry(f'400x200+{int(root.winfo_screenwidth() / 2) - 200}+{int(root.winfo_screenheight() / 2 - 100)}')
root.configure(background='green')
progress_label = tk.Label(master=root, text='', font=('Ariel', 20), bg='green')
progress_label.pack()


def check_for_updates():
    progress_label['text'] = 'Checking for updates'

    def progress_update_command():
        while True:
            sleep(0.5)
            if progress_label['text'] == 'Checking for updates':
                progress_label['text'] = 'Checking for updates.'
            elif progress_label['text'] == 'Checking for updates.':
                progress_label['text'] = 'Checking for updates..'
            elif progress_label['text'] == 'Checking for updates..':
                progress_label['text'] = 'Checking for updates...'
            elif progress_label['text'] == 'Checking for updates...':
                progress_label['text'] = 'Checking for updates'
            else:
                break

    Thread(target=progress_update_command).start()


Thread(target=check_for_updates).start()
root.mainloop()
