"""
Original repository link: https://github.com/Jiusoft/fax-browser
"""
import tkinter as tk


def download_file(item):
    root = tk.Tk()

    def save():
        item.accept()
        root.destroy()

    tk.Label(master=root,
             text=f'What would you like to do with {item.suggestedFileName()} ({item.totalBytes()} Bytes)').pack()
    tk.Button(master=root, text='Save', command=save).pack()
    tk.Button(master=root, text='Cancel', command=root.destroy).pack()
    root.mainloop()
# Enhancements coming soon...
