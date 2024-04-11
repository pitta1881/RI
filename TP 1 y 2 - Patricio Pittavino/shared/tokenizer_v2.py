from nltk.stem import PorterStemmer, LancasterStemmer
import os
import re

MAX_LONG = 20
MIN_LONG = 3
porter_stemmer = PorterStemmer()
lancaster_stemmer = LancasterStemmer()

def loadFileStopWords(stop_words_file: str):
    complete_route = os.path.abspath(stop_words_file)
    with open(complete_route, 'r', encoding='utf-8') as file:
        stop_words = set(word.strip() for word in file.readlines())
    return stop_words

def useStemmer(stemmer, content):
    if stemmer == 'porter':
        return [porter_stemmer.stem(word) for word in content]
    if stemmer == 'lancaster':
        return [lancaster_stemmer.stem(word) for word in content]
    return content

def removeStopWords(words_list, stop_words_list):
    cleaned_text = [word for word in words_list if word not in stop_words_list]
    return cleaned_text

def findAbbreviations(content):
    REGEX_ABBREVIATIONS = r'\b[A-Z](?:[\\.&]?[A-Z]){1,7}\b'
    REGEX_SPECIFIC = r'(?:Sr\.)|(?:Sra\.)'
    list_abbr = re.findall(REGEX_ABBREVIATIONS, content)
    list_abbr += re.findall(REGEX_SPECIFIC, content)
    content_without_abbr = re.sub(REGEX_ABBREVIATIONS, '', content)
    content_without_abbr = re.sub(REGEX_SPECIFIC, '', content_without_abbr)
    return content_without_abbr.strip(), list_abbr 

def findEmailsAndUrls(content):
    REGEX_EMAILS = r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    REGEX_URLS = r'((ht|f)tps?:\/\/\S*)'
    list_emails = re.findall(REGEX_EMAILS, content)
    list_urls = [protoDom for protoDom,_ in re.findall(REGEX_URLS, content)]
    content_without_emails = re.sub(REGEX_EMAILS, '', content)
    content_without_urls = re.sub(REGEX_URLS, '', content_without_emails)
    return content_without_urls.strip(), list_emails + list_urls

def findDatesNumbersAndPhones(content):
    REGEX_DATES = r'[0-9]+-[0-9]+-[0-9]+'
    REGEX_NUMBERS = r' (\d+)'
    REGEX_PHONES = r'\+?\d{6,}|\+?\d{8,}|\d{2,}-\d{5,}|\+?\d+-\d{2,}-\d{5,}'
    list_dates = re.findall(REGEX_DATES, content)
    content_without_dates = re.sub(REGEX_DATES, '', content)
    list_phones = re.findall(REGEX_PHONES, content_without_dates)
    content_without_phones = re.sub(REGEX_PHONES, '', content_without_dates)
    list_numbers = re.findall(REGEX_NUMBERS, content_without_phones)
    content_without_numbers = re.sub(REGEX_NUMBERS, '', content_without_phones)
    return content_without_numbers.strip(), list_dates + list_phones + list_numbers

def findNames(content):
    REGEX_NAME = r'\b[A-Z][a-z]+\b(?:\s+[A-Z][a-z]+)*'
    list_names = re.findall(REGEX_NAME, content)
    content_without_names = re.sub(REGEX_NAME, '', content)
    return content_without_names.strip(), list_names

def findWords(content):
    REGEX_WORDS = f'[a-z0-9]{{{MIN_LONG},{MAX_LONG}}}'
    list_words = re.findall(REGEX_WORDS, content)
    content_without_words = re.sub(REGEX_WORDS, '', content)
    return content_without_words.strip(), list_words

def tokenizer(content, stop_words_list = None):
    content, emailsAndUrls_list = findEmailsAndUrls(content)
    content, datesNumbersAndPhones_list = findDatesNumbersAndPhones(content)
    content, abbreviations_list = findAbbreviations(content)
    content, names_list = findNames(content)
    content, words_list = findWords(content.lower())
    content = emailsAndUrls_list + datesNumbersAndPhones_list + abbreviations_list + names_list + words_list
    if stop_words_list != None:
        content = removeStopWords(content, stop_words_list)
    return content