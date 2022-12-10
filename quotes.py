# load random lines from web

import requests
import json
import random

url = "https://type.fit/api/quotes"

total_lines = 3000
lines = 0

with open("/home/tototmek/Projects/Python/splash/quotes.data", "a") as file:
    for i in range(total_lines):
        response = requests.get(url)
        quotes = json.loads(response.text)
        quote = random.choice(quotes)
        try:
            file.write(quote["text"] + "~" + quote["author"] + "\n")
        except:
            pass
        lines += 1
        print("\rProgress: " + str(lines) + "/" + str(total_lines), end="")
