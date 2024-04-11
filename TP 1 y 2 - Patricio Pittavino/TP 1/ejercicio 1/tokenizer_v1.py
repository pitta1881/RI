import re

MAX_LONG = 20
MIN_LONG = 3

def removeStopWords(words_list, stop_words_list):
    cleaned_text = [word for word in words_list if word not in stop_words_list]
    return cleaned_text

def findWords(content):
    REGEX_WORDS = f'[a-z0-9]{{{MIN_LONG},{MAX_LONG}}}'
    return re.findall(REGEX_WORDS, content)

def tokenizer(content, stop_words_list = None):
    content = content.lower()
    content = findWords(content)
    if stop_words_list != None:
        content = removeStopWords(content, stop_words_list)
    return content