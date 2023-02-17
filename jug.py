import sys
import argparse
import requests
import warnings
import concurrent.futures

base = {}

def main():
    parser = argparse.ArgumentParser(description="Juggernaut is a directory bruteforcing tool that is nice to the servers and fully automated",
    usage="cat alive.txt | python3 jug.py [options]")

    parser.add_argument('-t', metavar='-threads', help="Specify the number of threads (default=25)")
    parser.add_argument('-w', metavar='-wordlist', help="Specify a wordlist.", required=True)

    args = parser.parse_args()

    num_threads = 25
    if(args.t != None):
        num_threads = args.t

    warnings.filterwarnings("ignore")

    urls = sys.stdin.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for url in urls:
            executor.submit(get_base, url)

    with open(args.w) as wordlist:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            for word in wordlist: 
                for url in urls:
                    executor.submit(run, url, word)

def get_base(_url):
    url = _url.strip()
    try:
        base[url] = {}

        # Get Base Response
        response = requests.get(f"{url}/", timeout=2, allow_redirects=False)
        line_count = len(response.text.split('\n'))
        base[url]["status_code"] = response.status_code
        base[url]["line_count"] = line_count
        base[url]["word_count"] = len(response.text.split())

        # Get Random Response
        response = requests.get(f"{url}/shelled", timeout=2, allow_redirects=False)
        line_count = len(response.text.split('\n'))
        base[url]["random_status_code"] = response.status_code
        base[url]["random_line_count"] = line_count
        base[url]["random_word_count"] = len(response.text.split())
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

        if(response.status_code == 200 and base[url]["word_count"] != word_count and base[url]["random_word_count"] != word_count):
            print(f"{url}/{word}")
    except requests.exceptions.RequestException as e:
        pass


main()
