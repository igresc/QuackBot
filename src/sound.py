from gtts import gTTS

def string_to_sound_file(string_text, file_name):
    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=string_text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save(file_name)