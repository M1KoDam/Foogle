import pymorphy2
import json
import re
from algorithm import LD, tf_idf
from collections import Counter

from indexer_infrastructure import *

with open('StopWords/stopwords-ru.json', encoding='utf-8') as json_file:
    stop_words_ru = set(json.load(json_file))

with open('StopWords/stopwords-eng.json', encoding='utf-8') as json_file:
    stop_words_eng = set(json.load(json_file))

RU_PATTERN = re.compile("[а-яА-ЯёЁ]+")
DEL_PATTERN = re.compile('[\W_]+')
ENCODING = ['utf-8', 'cp1251', 'cp1252', 'cp437', 'utf-16be']


class Indexer:
    def __init__(self, files, use_stop_words, use_morphy, ld_deep):
        print("use_stop_words:", use_stop_words)
        print("use_morphy:", use_morphy)
        print("ld_deep:", ld_deep)

        self.files = files
        self.use_stop_words = use_stop_words
        self.use_morphy = use_morphy
        self.ld_deep = ld_deep

        self.Morphy_ru = pymorphy2.MorphAnalyzer(lang='ru')

    def find(self, input_phrase: str) -> list:
        indexer, files_word_count = self.process_files()
        and_flag, or_flag, not_flag, phrases = find_bool_operation(input_phrase.lower())

        results = []
        for phrase in phrases:
            processed_phrase = self.process_phrase(phrase)

            results.append(self.find_phrase(indexer, processed_phrase, files_word_count))

        if and_flag:
            return list(set.intersection(*map(set, results)))[:10]
        elif or_flag:
            return list(set.union(*map(set, results)))[:10]
        elif not_flag:
            return list(set(self.files)-set(results[0]))[:10]
        return results[0][:10]

    def match_phrase_to_indexer(self, indexer: dict, processed_phrase: list):
        files_to_index = {}
        new_phrase = []

        coll = list(indexer.keys())
        for word in processed_phrase:
            ld_words, best_ld_word = LD.try_get_words_ld(word, coll, min((len(word) - 1) // 2, self.ld_deep))
            new_phrase.append(best_ld_word)

            for ld_word in ld_words:
                if best_ld_word in files_to_index.keys():
                    for key, value in indexer[ld_word].items():
                        if key in files_to_index[best_ld_word].keys():
                            files_to_index[best_ld_word][key] = files_to_index[best_ld_word][key] + value
                        else:
                            files_to_index[best_ld_word][key] = value
                else:
                    files_to_index[best_ld_word] = indexer[ld_word]

        return swap_keys(files_to_index), new_phrase

    def find_phrase(self,
                    indexer: dict,
                    processed_phrase: list,
                    file_word_count: dict,
                    tf_idf_range=0,
                    phrase_range=0.5) -> list:
        files_words, processed_phrase = self.match_phrase_to_indexer(indexer, processed_phrase)
        print("Processed phrase:", processed_phrase)
        priority = {}
        priority_range = tf_idf_range

        for file_name, words in files_words.items():
            if len(processed_phrase) == 1:
                power = tf_idf(word_in_file=len(words[processed_phrase[0]]),
                               file_words_count=file_word_count[file_name],
                               files_count=len(self.files),
                               files_count_with_word=len(indexer[processed_phrase[0]].keys()))

            else:
                temp_indexes = []
                for i, value in enumerate(words.values()):
                    temp_indexes.extend([index - i for index in value])

                power = temp_indexes.count(Counter(temp_indexes).most_common(1)[0][0]) / len(processed_phrase)
                priority_range = phrase_range

            if power > priority_range:
                priority[file_name] = power

        return [item[0] for item in sorted(priority.items(), key=lambda x: x[1], reverse=True)]

    def process_files(self) -> (dict, dict):
        print("START PROCESSING FILES")
        file_to_words = {}
        file_word_count = {}
        for file_name in self.files:
            for encoding in ENCODING:
                try:
                    with open(file_name, 'r', encoding=encoding) as file:
                        file_data = file.read().lower()
                        file_data = re.sub(DEL_PATTERN, ' ', file_data).split()
                        processed_data = self.process_data(file_data)
                        file_word_count[file_name] = len(processed_data)
                        file_to_words[file_name] = processed_data
                    break
                except UnicodeDecodeError:
                    pass
            else:
                print(f"Error opening {file_name}")

        file_to_index = {}
        for file_name in file_to_words.keys():
            file_to_index[file_name] = make_word_to_index(file_to_words[file_name])

        print("END PROCESSING FILES")
        return swap_keys(file_to_index), file_word_count

    def process_phrase(self, phrase: str) -> list:
        phrase = re.sub(DEL_PATTERN, ' ', phrase).lower()
        return self.process_data(phrase.split())

    def process_data(self, data: list) -> list:
        processed_data = []
        for word in data:
            if self.use_stop_words and (word in stop_words_ru or word in stop_words_eng):
                continue
            if self.use_morphy and bool(re.search(RU_PATTERN, word)):
                word = self.Morphy_ru.normal_forms(word)[0]
            processed_data.append(word)
        return processed_data


def main():
    pass


if __name__ == "__main__":
    main()
