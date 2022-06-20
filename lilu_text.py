from textblob import TextBlob
from googletrans import Translator

# dicts or smth
# python -m textblob.download_corpora

translator = Translator()


def russian_bitch_do_you_speak_it(text: str) -> (str, str):
    print(f'detecting {text}')
    lang = translator.detect(text)
    if lang.lang == 'ru': return text, ''

    result = translator.translate(text, dest='ru', src=lang.lang)
    return result.text, text
