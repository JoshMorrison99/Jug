# Juggernaut
Juggernaut is a contextual directory bruteforcing tool that is nice to the servers and fully automated. 
<br/>
<br/>

**Features**
- Similar to `meg`, Juggernaut will fuzz one word on each URL before proceeding to the next word in the wordlist. 
- Uses Wappalyzer to detect the technology being used and will fuzz with the corresponding wordlist.
- Creates a base request and random request to get the number of words in response, output will only be displayed if the fuzzed status code is 200 and the number of words in fuzzed response is different from the number of words in base response and random response. 
