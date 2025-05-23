#!/usr/bin/python3

import os
import glob
import re
import json
import requests
from datetime import datetime

count = {}
countfile = {}
count['total'] = 0
count['bookshelf'] = 0
count['portable'] = 0

def youtubeid_to_title(ytid):
    url = 'https://www.googleapis.com/youtube/v3/videos?id=' + ytid + '&key=AIzaSyD2nni2ukaZIWlsI1oFq5BWfhEVL7LjPVQ%20&part=snippet'
    request = requests.get(url, timeout=30)
    data = request.json()
    description = data['items'][0]['snippet']['channelTitle'] + ': ' + data['items'][0]['snippet']['title']
    return description.replace('|', '')

try:
    with open('youtubeLookup.json') as f:
        youtubeLookup = json.load(f)
except:
    youtubeLookup = {}

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
                elif re.match('^    - <https://www.youtube.com/watch', line):
                    try:
                        ytid = line.split('=')[1].split('>')[0]
                        if ytid not in youtubeLookup: 
                            description = youtubeid_to_title(ytid)
                            line = '    - [' + description + '](https://www.youtube.com/watch?v=' + ytid + ')\n'
                    except:
                        print('Error fetching info for ' + ytid + '\n')
                        youtubeLookup[ytid] = False
                    newline = line

                else:
                    newline = line         
                f.write(newline)
        if number > 0:
            countfile[file] = number

with open('youtubeLookup.json', 'w') as f:
    f.write(json.dumps(youtubeLookup, indent=4, sort_keys=True))

with open('index.md') as f:
    lines = f.readlines()
with open('index.md', 'w') as f:
    for line in lines:
        if line.startswith('Speaker Ranking ranks a total of'):
            line = re.sub(regex, ' ' + str(count['total']) + ' ', line, count=1)
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

for filename in glob.glob(os.path.join('./', 'top-recommended*.md')):
    with open(filename) as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
        for line in lines:
            if line.startswith('This page lists'):
                line = re.sub(regex, ' ' + str(count['portable']) + ' ', line, count=1)
            f.write(line)

with open('bookshelf-top-recommended.md') as f:
    lines = f.readlines()
with open('bookshelf-top-recommended.md', 'w') as f:
    for line in lines:
        if line.startswith('This page lists'):
            line = re.sub(regex, ' ' + str(count['bookshelf']) + ' ', line, count=1)
        f.write(line)

for file in countfile:
    with open(file) as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            if line.startswith('This page ranks'):
                line = re.sub(regex, ' ' + str(countfile[file]) + ' ', line, count=1)
            f.write(line)
