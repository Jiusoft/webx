"""
Original repository link: https://github.com/Jiusoft/fax-browser
"""
import tkinter as tk


def download_file(item):
    root = tk.Tk()
    root.overrideredirect(True)
    root.eval('tk::PlaceWindow . center')
    filename = item.suggestedFileName()
    root.wm_title(f'{filename} download - FAX browser')

    def save():
        item.accept()
        root.destroy()

    tk.Label(master=root,
             text=f'What would you like to do with {filename}').pack()
    tk.Button(master=root, text='Save', command=save).pack()
    tk.Button(master=root, text='Cancel', command=root.destroy).pack()
    root.mainloop()
# Enhancements coming soon...
