#!/usr/bin/env python3
import sys

current_url = None
current_count = 0
url = None

for line in sys.stdin:
    line = line.strip()
    url, count = line.split('\t', 1)
    
    try:
        count = int(count)
    except ValueError:
        continue

    if current_url == url:
        current_count += count
    else:
        if current_url and current_count > 5:  
            print(f'{current_url}\t{current_count}')
        current_url = url
        current_count = count

if current_url == url and current_count > 5:
    print(f'{current_url}\t{current_count}')