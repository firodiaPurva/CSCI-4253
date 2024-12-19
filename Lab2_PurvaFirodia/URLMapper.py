#!/usr/bin/env python3
import sys
import re


url_regex = r'href="([^"]+)"'

for line in sys.stdin:
    line = line.strip()
    urls = re.findall(url_regex, line)
    for url in urls:
        print(f'{url}\t1')