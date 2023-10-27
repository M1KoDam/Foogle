import json
import re

with open('StopWords/stopwords-ru.json', encoding='utf-8') as json_file:
    stop_words_ru = json.load(json_file)

with open('StopWords/stopwords-eng.json', encoding='utf-8') as json_file:
    stop_words_eng = json.load(json_file)

pattern = re.compile('[\W_]+')

def process_files(file_paths) -> dict:
    file_to_words = {}
    for file_name in file_paths:
        with open(file_name, 'r', encoding='utf-8') as file:
            file_data = file.read().lower()
            file_data = re.sub(pattern, ' ', file_data)
            file_to_words[file_name] = process_data(file_data.split())

    file_to_index = {}
    for file_name in file_to_words.keys():
        file_to_index[file_name] = make_word_to_index(file_to_words[file_name])

    return swap_keys(file_to_index)


def process_phrase(phrase) -> list:
    phrase = re.sub(pattern, ' ', phrase).lower()
    return process_data(phrase.split())


def process_data(data) -> list:
    processed_data = []
    for word in data:
        if len(word) < 3 or word in stop_words_ru or word in stop_words_eng:
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

