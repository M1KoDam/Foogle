from indexer_infrastructure import *


class Indexer:
    def __init__(self, file_paths, ld_deep=0):
        self.indexer = process_files(file_paths)
        self.ld_deep = ld_deep

    def find_phrase(self, phrase: str):
        processed_phrase = process_phrase(phrase)
        print(f"processed_phrase = {processed_phrase}")
        files_to_index = {}
        coll = list(self.indexer.keys())
        for word in processed_phrase:
            w = LD.try_get_word_ld(word, coll, self.ld_deep)
            if w != " ":
                files_to_index[w] = self.indexer[w]

        files_words = swap_keys(files_to_index)
        return get_file_priority_on_phrase(files_words)


def main():
    pass


if __name__ == "__main__":
    main()
