from gtts import gTTS

def joke_to_sound_file(joke_text):
    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=joke_text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save('joke.mp3')