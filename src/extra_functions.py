import os, requests, random, json
from gtts import gTTS

def string_to_sound_file(string_text, file_name, lang="en"):
    # Language in which you want to convert
    language = lang

    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=string_text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save(file_name)

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

def joke_request():
    # icanhazdadjoke.com api definitions
    dadjoke_url = "https://icanhazdadjoke.com/"
    headers = {'Accept': 'application/json', 'User-Agent': 'Api tests (sergicastro2001@gmail.com)'}
    r = requests.get(url=dadjoke_url, headers=headers)
    joke = r.json()["joke"]
    return joke

def rm_file(filename):
    try:
        os.remove(filename)
    except PermissionError as e:
        print(e)

def get_rand_insult():
    r = requests.get(url="https://raw.githubusercontent.com/EddieSharp/Insultos/master/diccionario.txt")
    insult_list = r.text.splitlines()
    return random.choice(insult_list)