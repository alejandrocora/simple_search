# Simple Search

Command-line tool to make a quick search and obtain links from DuckDuckGo or Google.

## Installation

`$ git clone https://github.com/alejandrocora/simple_search`  
`$ cd simple_search`  
`$ pip3 install .`

## Help

Run `simple_search --help` for help:
```
usage: simple_search [-h] --query QUERY [--npages NPAGES] [--duckduckgo] [--google] [--languages LANGS] [--print] [--output OUTPUT]

options:
  -h, --help         show this help message and exit

required arguments:
  --query QUERY      Query string to search.

optional arguments:
  --npages NPAGES    Number of result pages to collect.
  --duckduckgo       Use DuckDuckGo (both will be used if none is selected).
  --google           Use Google (both will be used if none is selected).
  --languages LANGS  Search language code (default: en_US)
  --print            Print results.
  --output OUTPUT    Save results into a given file.
```