import sys
import requests
import warnings
import concurrent.futures
from Wappalyzer import Wappalyzer, WebPage

base = {}

def main():
    warnings.filterwarnings("ignore")

    urls = sys.stdin.readlines()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url in urls:
            executor.submit(get_base, url)

    with open('sample.txt') as wordlist:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for word in wordlist: 
                for url in urls:
                    executor.submit(run, url, word)

def get_base(_url):
    url = _url.strip()
    try:
        response = requests.get(f"{url}/", timeout=2, allow_redirects=False)
        base[url] = {}
        line_count = len(response.text.split('\n'))
        base[url]["status_code"] = response.status_code
        base[url]["line_count"] = line_count
        base[url]["word_count"] = len(response.text.split())
        base[url]["technology"] = {}

        # Create a Wappalyzer object and analyze the webpage
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_response(response)
        detected = wappalyzer.analyze(webpage)

        base[url]["technology"] = detected
    except:
        pass

def run(_url, _word):
    url = _url.strip()
    word = _word.strip()
    
    try:
        response = requests.get(f"{url}/{word}", timeout=2, allow_redirects=False)
        line_count = len(response.text.split('\n'))
        word_count = len(response.text.split())
        #print(f"{(url + '/' + word):75}     [Status: {response.status_code}, Size: {len(response.content)}, Words: {word_count}, Lines: {line_count}]")

        if(response.status_code == 200 and base[url]["word_count"] != word_count):
            print(f"{url}/{word}")
    except requests.exceptions.RequestException as e:
        pass


main()
