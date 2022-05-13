"""
Original repository link: https://github.com/Jiusoft/webx
Author: Jothin kumar (https://jothin.tech/)
"""
from os import listdir
from os.path import join
from pathlib import Path
from hashlib import sha256

files = []
folders = ['scripts/webx']
while folders:
    for folder in folders:
        for path in listdir(folder):
            path = join(folder, path)
            if Path(path).is_file():
                files.append(path)
            elif Path(path).is_dir():
                folders.append(path)
        folders.remove(folder)

with open('file-hashes.txt', 'w') as _:
    _.write('')
for file in files:
    with open('file-hashes.txt', 'a+') as hash_file:
        with open(file, 'rb') as file_content:
            hash_ = sha256(file_content.read()).hexdigest()
            print(f'https://raw.githubusercontent.com/Jiusoft/webx/main/{file} || {hash_}')
            hash_file.write(f'https://raw.githubusercontent.com/Jiusoft/webx/main/{file} || {hash_}\n')

print('\nDone.')
