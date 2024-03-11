#!/usr/bin/python3

import os


for file in os.listdir():
    newfile = ''
    number = 1
    if file.endswith('-size.md'):
        with open(file) as f:
            lines = f.readlines()
        with open(file, 'w') as f:
            for line in lines:
                if line.startswith('### '):
                    splitline = line.split(' ')
                    if splitline[1].startswith('#'):
                        newline = '### #' + str(number) + ' ' + ' '.join(splitline[2:])
                    else:
                        newline = '### #' + str(number) + ' ' + ' '.join(splitline[1:])
                    number += 1
                else:
                    newline = line         
                f.write(newline)

