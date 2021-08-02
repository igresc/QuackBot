import os, requests, random, json

def tenor_get():
    TENOR_API_KEY = os.environ["TENOR_API_KEY"]
    if not os.path.isfile("data/gifs.json"):
        response = requests.get(url="https://g.tenor.com/v1/search?q=duck&key={}&media_filter=basic&limit=50".format(TENOR_API_KEY))
        gif = response.json()
        results = gif["results"]
        with open("data/gifs.json", "w") as f:
            json_string = json.dumps(results)
            f.write(json_string)
            f.close()
    else:
        with open("data/gifs.json", "r") as f:
            json_string = f.read()
            results = json.loads(json_string)
    random_gif = random.choice(results)
    return random_gif["url"]

# print(tenor_get())
