import requests
import argparse
from bs4 import BeautifulSoup

from constants import *


class DuckDuckGo():
    def __init__(self):
        self.links = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-agent':DEFAULT_HEADER
        })
        self.last_query = ''
        self.last_response = ''

    def change_browser_language(self, lang_code):
        self.session.headers.update({
            'Accept-language':lang_code
        })

    def search(self, query):
        self.last_query = query
        self.last_response = self.session.get(DUCKDUCKGO_SEARCH_URL+query)
        return self.last_response

    def next_page(self):
        soup = BeautifulSoup(self.last_response.text, 'html.parser')
        try:
            self.last_response = self.session.post(DUCKDUCKGO_SEARCH_URL+self.last_query,
                '&s='+soup.find('input', {'name':'s'}).get('value')+
                '&nextParams='+soup.find('input', {'name':'nextParams'}).get('value')+
                '&v=l'+soup.find('input', {'name':'v'}).get('value')+
                '&o='+soup.find('input', {'name':'o'}).get('value')+
                '&dc='+soup.find('input', {'name':'dc'}).get('value')+
                '&api='+soup.find('input', {'name':'api'}).get('value')+
                '&vqd='+soup.find('input', {'name':'vqd'}).get('value'))
            return self.last_response
        except:
            return None

    def get_page_results(response):
        links = []
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', {'class':'result__url'}):
            links.append(link.get_text().strip('\n').strip('   ').strip('\n'))
        return links

    def start_scrap(self, query):
        self.links = self.links + DuckDuckGo.get_page_results(self.search(query))

    def scrap(self, query, npages):
        npages = npages - 1
        self.start_scrap(query)
        for i in range(npages):
            page = self.next_page()
            if page:
                self.links = self.links + DuckDuckGo.get_page_results(page)
            else:
                break

    def clean_links(self):
        self.links = []

    def get_links(self):
        return self.links

    def print_links(self):
        for link in self.links:
            print(link)


class Google():
    def __init__(self):
        self.links = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-agent':DEFAULT_HEADER
        })
        self.last_query = ''
        self.last_response = ''

    def change_browser_language(self, lang_code):
        self.session.headers.update({
            'Accept-language':lang_code
        })

    def search(self, query):
        self.last_query = query
        self.last_response = self.session.get(GOOGLE_SEARCH_URL+query)
        return self.last_response

    def next_page(self):
        next_a = BeautifulSoup(self.last_response.text, 'html.parser').find('a', {'id':'pnnext'})
        if next_a:
            self.last_response = self.session.get('https://google.com'+next_a.get('href'))
            return self.last_response
        return None

    def is_blocked(response):
        soup = BeautifulSoup(response.text, 'html.parser').find('script', {'src':'https://www.google.com/recaptcha/api.js'})
        if soup:
            return True
        else:
            return False

    def get_page_results(response):
        if Google.is_blocked(response):
            raise Exception("CAPTCHA REQUIRED: Unable to obtain results.")
        links = []
        soup = BeautifulSoup(response.text, 'html.parser').find('div', {'id':'res'})
        for link in soup.find_all('a', {'data-jsarwt':'1'}):
            links.append(link.get('href').strip('\n').strip('   ').strip('\n'))
        return links

    def start_scrap(self, query):
        self.links = self.links + Google.get_page_results(self.search(query))

    def scrap(self, query, npages):
        npages = npages - 1
        self.start_scrap(query)
        for i in range(npages):
            page = self.next_page()
            if page:
                self.links = self.links + Google.get_page_results(page)
            else:
                break

    def clean_links(self):
        self.links = []

    def get_links(self):
        return self.links

    def print_links(self):
        for link in self.links:
            print(link)


def file_list(filename, list):
    f = open(filename, 'a')
    for i in list:
        f.write(i+'\n')
    f.close()


def search_for_links(query, npages, search_engines, languages):
    links = []
    for engine in search_engines:
        for lang_code in languages: # doesn't work in Google for now
            engine.change_browser_language(lang_code)
            engine.scrap(query, npages)
        links = links + engine.get_links()
    return links


def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('--query', dest='query', required=True, help='')
    optional.add_argument('--npages', dest='npages', type=int, default=0, help='')
    optional.add_argument('--duckduckgo', dest='duckduckgo', action='store_const', const=DuckDuckGo(), default=False, help='')
    optional.add_argument('--google', dest='google', action='store_const', const=Google(), default=False, help='')
    optional.add_argument('--languages', dest='langs', default='en_US', help='')
    optional.add_argument('--print', dest='to_print', action='store_true', default=False, help='')
    optional.add_argument('--output', dest='output', default=False, help='')
    args = parser.parse_args()
    query = args.query
    npages = args.npages
    search_engines = []
    languages = args.langs.split(',')
    if args.duckduckgo : search_engines.append(args.duckduckgo)
    if args.google : search_engines.append(args.google)
    if not search_engines : search_engines = [Google(), DuckDuckGo()]
    to_print = args.to_print
    output = args.output
    links = search_for_links(query, npages, search_engines, languages)
    links = list(dict.fromkeys(links))
    if to_print:
        for link in links:
            print(link)
    if output:
        file_list(output, links)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Quitting...")
        sys.exit
