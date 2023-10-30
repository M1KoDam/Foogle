import json
import re
from algorithm import LD
from collections import Counter

with open('StopWords/stopwords-ru.json', encoding='utf-8') as json_file:
    stop_words_ru = set(json.load(json_file))

with open('StopWords/stopwords-eng.json', encoding='utf-8') as json_file:
    stop_words_eng = set(json.load(json_file))

PATTERN = re.compile('[\W_]+')
ENCODING = ['utf-8', 'cp1251', 'cp1252', 'cp437', 'utf-16be']


def process_files(file_paths) -> dict:
    print("START PROCESSING FILES")
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

    print("END PROCESSING FILES")
    return swap_keys(file_to_index)


def process_phrase(phrase) -> list:
    phrase = re.sub(PATTERN, ' ', phrase).lower()
    return process_data(phrase.split())


def process_data(data: list) -> list:
    processed_data = []
    for word in data:
        if len(word) == 1 or word in stop_words_ru or word in stop_words_eng:
            # LD.word_in_list_ld(word, stop_words_ru, 0) or LD.word_in_list_ld(word, stop_words_eng, 0):
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


def swap_keys(file_to_index: dict) -> dict:
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


def get_file_priority_on_phrase(files_words: dict, priority_range=0):
    priority = {}
    for file_name, word in files_words.items():
        temp_indexes = []

        for i, value in enumerate(word.values()):
            temp_indexes.extend([index - i for index in value])

        power = temp_indexes.count(Counter(temp_indexes).most_common(1)[0][0])
        if power > priority_range:
            priority[file_name] = power

    return sorted(priority.items(), key=lambda x: x[1], reverse=True)[:10]

