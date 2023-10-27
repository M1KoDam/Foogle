import json
import re
from algorithm import LD

with open('StopWords/stopwords-ru.json', encoding='utf-8') as json_file:
    stop_words_ru = json.load(json_file)

with open('StopWords/stopwords-eng.json', encoding='utf-8') as json_file:
    stop_words_eng = json.load(json_file)

PATTERN = re.compile('[\W_]+')
ENCODING = ['utf-8', 'cp1251', 'cp1252', 'cp437', 'utf-16be']
ld = LD(3)


def process_files(file_paths) -> dict:
    file_to_words = {}
    for file_name in file_paths:
        for encoding in ENCODING:
            try:
                with open(file_name, 'r', encoding=encoding) as file:
                    file_data = file.read().lower()
                    file_data = re.sub(PATTERN, ' ', file_data)
                    file_to_words[file_name] = process_data(file_data.split())
                break
            except UnicodeDecodeError:
                pass
        else:
            print(f"Error opening {file_name}")

    file_to_index = {}
    for file_name in file_to_words.keys():
        file_to_index[file_name] = make_word_to_index(file_to_words[file_name])

    return swap_keys(file_to_index)


def process_phrase(phrase) -> list:
    phrase = re.sub(PATTERN, ' ', phrase).lower()
    return process_data(phrase.split())


def process_data(data) -> list:
    processed_data = []
    for word in data:
        if len(word) < 3: # or ld.word_in_list_ld(word, stop_words_ru) or ld.word_in_list_ld(word, stop_words_eng):
            continue
        processed_data.append(word)
    return processed_data


def make_word_to_index(file_to_words) -> dict:
    word_to_index = {}
    for index, word in enumerate(file_to_words):
        if word in word_to_index.keys():
            word_to_index[word].append(index)
            continue
        word_to_index[word] = [index]
    return word_to_index


def swap_keys(file_to_index) -> dict:
    """Swap key1 and key2 in {key1: {key2: value2}, ...}"""
    file_index = {}
    for file_name in file_to_index.keys():
        for word in file_to_index[file_name]:
            if word in file_index.keys():
                if file_name in file_index.keys():
                    file_index[word][file_name].extend(file_to_index[file_name][word])
                else:
                    file_index[word][file_name] = file_to_index[file_name][word]
            else:
                file_index[word] = {file_name: file_to_index[file_name][word]}
    return file_index


def get_file_on_phrase(files_words: dict, phrase: list):
    priority = []
    for file_name, word in files_words.items():
        temp = []

        if not ld.list_in_list_ld(phrase, word.keys()):
            continue

        for i, value in enumerate(word.values()):
            temp.append([index-i for index in value])

        if set(temp[0]).intersection(*temp):
            priority.append(file_name)

    return priority

