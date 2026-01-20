#!/usr/bin/python3

import os
import glob
import re
import json
import requests
import urllib
from datetime import datetime

countfile = {}

regex = re.compile(r' [0-9][0-9]* ')
for file in ['personal-ranking-of-speaker-reviewers.md']:
    newfile = []
    number = 0
    if file.endswith('.md'):
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('### #'):
                    number += 1
                    splitline = line.split(' ')
                    if splitline[1].startswith('#'):
                        line = '### #' + str(number) + ' ' + ' '.join(splitline[2:])
                    else:
                        line = '### #' + str(number) + ' ' + ' '.join(splitline[1:])

                newfile.append(line)

        with open(file, 'w') as f:
            f.write(''.join(newfile))
        #exit(0)
        if number > 0:
            countfile[file] = number

newfile = []
with open('index.md') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('- '):
            url = line.split('(')[1].split('/')[1]
            filename = url + '.md'
            if filename in countfile:
                if countfile[filename] > 0:
                        line = re.sub(regex, ' ' + str(countfile[filename]) + ' ', line, count=1)
        newfile.append(line)
with open('index.md', 'w') as f:
    f.write(''.join(newfile))
