#!/usr/bin/python3

import os
import re
from datetime import datetime

count = {}

current_datetime = datetime.now()
regex = re.compile('[0-9][0-9][0-9]*')
total = 0
for file in os.listdir():
    newfile = ''
    number = 0
    if file.endswith('.md'):
        with open(file) as f:
            lines = f.readlines()
        with open(file, 'w') as f:
            for line in lines:
                if line.startswith('### #'):
                    number += 1
                    if file != 'personal-ranking-of-speaker-reviewers.md':
                        total += 1
                    splitline = line.split(' ')
                    if splitline[1].startswith('#'):
                        newline = '### #' + str(number) + ' ' + ' '.join(splitline[2:])
                    else:
                        newline = '### #' + str(number) + ' ' + ' '.join(splitline[1:])
                else:
                    newline = line         
                f.write(newline)
        count[file] = number

with open('index.md') as f:
    lines = f.readlines()
with open('index.md', 'w') as f:
    for line in lines:
        if line.startswith('This website ranks a total of'):
            line = re.sub(regex, str(total), line)
        if line.startswith('Last updated '):
            date = current_datetime.strftime("%m/%d/%Y")
            line = 'Last updated ' + date + '\n'
        if line.startswith('- '):
            url = line.split('(')[1].split('/')[1]
            filename = url + '.md'
            if filename in count:
                if count[filename] > 0:
                    if filename != 'personal-ranking-of-speaker-reviewers.md':
                        line = line.split(':')[0].strip() + ': ' + str(count[filename]) + ' speakers ranked\n'
                    else:
                        line = line.split(':')[0].strip() + ': ' + str(count[filename]) + ' reviewers ranked\n'
        f.write(line)
