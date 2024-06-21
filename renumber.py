#!/usr/bin/python3

import os
import re
from datetime import datetime

count = {}
countfile = {}
count['total'] = 0
count['bookshelf'] = 0
count['portable'] = 0

current_datetime = datetime.now()
regex = re.compile(' [0-9][0-9]* ')
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
                        if file.startswith('bookshelf-'):
                            count['bookshelf'] += 1
                        else:
                            count['portable'] += 1
                        count['total'] += 1
                    splitline = line.split(' ')
                    if splitline[1].startswith('#'):
                        newline = '### #' + str(number) + ' ' + ' '.join(splitline[2:])
                    else:
                        newline = '### #' + str(number) + ' ' + ' '.join(splitline[1:])
                else:
                    newline = line         
                f.write(newline)
        if number > 0:
            countfile[file] = number

with open('index.md') as f:
    lines = f.readlines()
with open('index.md', 'w') as f:
    for line in lines:
        if line.startswith('This website ranks a total of'):
            line = re.sub(regex, ' ' + str(count['total']) + ' ', line)
        if line.startswith('Last updated '):
            date = current_datetime.strftime("%m/%d/%Y")
            line = 'Last updated ' + date + '\n'
        if line.startswith('- '):
            url = line.split('(')[1].split('/')[1]
            filename = url + '.md'
            if filename in countfile:
                if countfile[filename] > 0:
                    if filename != 'personal-ranking-of-speaker-reviewers.md':
                        line = line.split(':')[0].strip() + ': ' + str(countfile[filename]) + ' speakers ranked\n'
                    else:
                        line = line.split(':')[0].strip() + ': ' + str(countfile[filename]) + ' reviewers ranked\n'
        f.write(line)

with open('top-recommended.md') as f:
    lines = f.readlines()
with open('top-recommended.md', 'w') as f:
    for line in lines:
        if line.startswith('This page lists'):
            line = re.sub(regex, ' ' + str(count['portable']) + ' ', line)
        f.write(line)

with open('bookshelf-top-recommended.md') as f:
    lines = f.readlines()
with open('bookshelf-top-recommended.md', 'w') as f:
    for line in lines:
        if line.startswith('This page lists'):
            line = re.sub(regex, ' ' + str(count['bookshelf']) + ' ', line)
        f.write(line)

for file in countfile:
    with open(file) as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            if line.startswith('This page ranks'):
                line = re.sub(regex, ' ' + str(countfile[file]) + ' ', line)
            f.write(line)
