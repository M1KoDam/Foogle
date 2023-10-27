from indexer_infrastructure import *


class Indexer:
    def __init__(self, file_paths):
        self.indexer = process_files(file_paths)
        self.ld = LD(3)

    def find_phrase(self, phrase: str):
        processed_phrase = process_phrase(phrase)
        print(f"processed_phrase = {processed_phrase}")
        files_to_index = {}
        for word in processed_phrase:
            w = self.ld.try_get_word_ld(word, list(self.indexer.keys()))
            if w != " ":
                files_to_index[w] = self.indexer[w]

        files_words = swap_keys(files_to_index)
        return get_file_on_phrase(files_words, processed_phrase)


def main():
    pass


if __name__ == "__main__":
    main()
