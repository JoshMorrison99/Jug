# Juggernaut
Juggernaut is a directory bruteforcing tool that is nice to servers and fully automated. This tool is basically `meg`, but doesn't require supervision or filtering. 
<br/>
<br/>

**Features**
- Juggernaut will fuzz one word on each URL before proceeding to the next word in the wordlist. 
- Creates a base request and random request to get the number of words in response, output will only be displayed if the fuzzed status code is 200 and the number of words in fuzzed response is different from the number of words in base response and random response. 

**Usage**
```
cat alive.txt | python jug.py
```
