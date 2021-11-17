"""
Original repository link: https://github.com/Jiusoft/fax-browser
"""
import tkinter as tk


def download_file(item):
    root = tk.Tk()
    filename = item.suggestedFileName()
    root.wm_title(f'{filename} download - Jiusoft fax browser')

    def save():
        item.accept()
        root.destroy()

    tk.Label(master=root,
             text=f'What would you like to do with {filename} ({item.totalBytes()} Bytes)').pack()
    tk.Button(master=root, text='Save', command=save).pack()
    tk.Button(master=root, text='Cancel', command=root.destroy).pack()
    root.mainloop()
# Enhancements coming soon...
