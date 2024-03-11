#!/usr/bin/python3

import os
import re
from datetime import datetime

current_datetime = datetime.now()
regex = re.compile('[0-9][0-9][0-9]*')
total = 0
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
                    total += 1
                else:
                    newline = line         
                f.write(newline)

with open('index.md') as f:
    lines = f.readlines()
with open('index.md', 'w') as f:
    for line in lines:
        if line.startswith('I'):
            line = re.sub(regex, str(total), line)
        if line.startswith('Last updated '):
            date = current_datetime.strftime("%m/%d/%Y")
            line = 'Last updated ' + date + '\n'
        f.write(line)
