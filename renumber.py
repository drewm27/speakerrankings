#!/usr/bin/python3

import os
import glob
import re
import json
import requests
import urllib
from datetime import datetime

count = {}
countfile = {}
count['total'] = 0
count['bookshelf'] = 0
count['passive'] = 0
count['portable'] = 0

def youtubeid_to_title(ytid):
    url = 'https://www.googleapis.com/youtube/v3/videos?id=' + ytid + '&key=AIzaSyD2nni2ukaZIWlsI1oFq5BWfhEVL7LjPVQ%20&part=snippet'
    request = requests.get(url, timeout=30)
    data = request.json()
    description = data['items'][0]['snippet']['channelTitle'] + ': ' + data['items'][0]['snippet']['title']
    return description.replace('|', '')

def ebay_url(search):
    return 'https://www.ebay.com/sch/i.html?_nkw=' + urllib.parse.quote(search) + '&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5339110165&customid=f206&toolid=10001&mkevt=1'

try:
    with open('youtubeLookup.json') as f:
        youtubeLookup = json.load(f)
except:
    youtubeLookup = {}

current_datetime = datetime.now()
regex = re.compile(' [0-9][0-9]* ')
for file in os.listdir():
    newfile = []
    number = 0
    if file.endswith('.md'):
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('### #'):
                    number += 1
                    splitline = line.split(' ')
                    if file != 'personal-ranking-of-speaker-reviewers.md':
                        if file.startswith('bookshelf-'):
                            count['bookshelf'] += 1
                        elif file.startswith('passive-'):
                            count['passive'] += 1
                        else:
                            count['portable'] += 1
                        count['total'] += 1

                        if splitline[2].startswith('['):
                            print(line)
                            name = line.split('[')[1].split(']')[0]
                            url = line.split('(')[1].split(')')[0]
                            retailer = url.replace('/lu.', '/').replace('www.', '').split('/')[2].split('.')[0].capitalize()
                            print(name + ' ' + url + ' ' + retailer)
                            #print(ebay_url(name))
                            if retailer == 'Amazon' and not '[[Amazon]' in line:
                                line.replace(':', ' [[Amazon](' + url + ')]:')
                            if not '[[Ebay]' in line:
                                line.replace(':', ' [[Ebay](' + ebay_url(name) + ')]:')


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
                newfile.append(newline)

        with open(file, 'w') as f:
            f.write(''.join(newfile))
        exit(0)
        if number > 0:
            countfile[file] = number

with open('youtubeLookup.json', 'w') as f:
    f.write(json.dumps(youtubeLookup, indent=4, sort_keys=True))

newfile = []
with open('index.md') as f:
    lines = f.readlines()
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
                        line = re.sub(regex, ' ' + str(countfile[filename]) + ' ', line, count=1)
        newfile.append(line)
with open('index.md', 'w') as f:
    f.write(''.join(newfile))

for filename in glob.glob(os.path.join('./', 'top-recommended*.md')):
    newfile = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('This page lists'):
                line = re.sub(regex, ' ' + str(count['portable']) + ' ', line, count=1)
            newfile.append(line)
    with open(filename, 'w') as f:
        f.write(''.join(newfile))

newfile = []
with open('bookshelf-top-recommended.md') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('This page lists'):
            line = re.sub(regex, ' ' + str(count['bookshelf']) + ' ', line, count=1)
        newfile.append(line)
with open('bookshelf-top-recommended.md', 'w') as f:
    f.write(''.join(newfile))

newfile = []
with open('passive-top-recommended.md') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('This page lists'):
            line = re.sub(regex, ' ' + str(count['passive']) + ' ', line, count=1)
        newfile.append(line)
with open('passive-top-recommended.md', 'w') as f:
    f.write(''.join(newfile))

for file in countfile:
    newfile = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('This page ranks'):
                line = re.sub(regex, ' ' + str(countfile[file]) + ' ', line, count=1)
            newfile.append(line)
    with open(file, 'w') as f:
        f.write(''.join(newfile))
