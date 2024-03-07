from googletrans import Translator

def translate_text(text):
    translator = Translator()
    translated = translator.translate(text, dest='en')
    return translated.text