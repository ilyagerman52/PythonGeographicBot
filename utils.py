from translate import Translator
import re


def translate(en_str):
    translator = Translator(to_lang='Russian')
    ru_str = translator.translate(en_str)
    if ru_str[:3] == 'г. ':
        ru_str = ru_str[3:]
    if len(re.findall(r"[а-яA-Я-'.’ ]", ru_str)) != len(ru_str):
        print(en_str, ru_str)
        return
    return ru_str