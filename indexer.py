from indexer_infostructure import process_files, process_phrase, swap_keys


class Indexer:
    def __init__(self, file_paths):
        self.indexer = process_files(file_paths)

    def find_phrase(self, phrase : str):
        processed_phrase = process_phrase(phrase)
        print(processed_phrase)
        files_to_index = {}
        for word in processed_phrase:
            if word in self.indexer.keys():
                files_to_index[word] = self.indexer[word]

        files_words = swap_keys(files_to_index)
        self.get_file(files_words, [])

    def get_file(self, files_words : dict, phrase : list):
        priority = []
        for file_name, word in files_words.items():
            temp = []
            for i, value in enumerate(word.values()):
                temp.append([index-i for index in value])

            if set(temp[0]).intersection(*temp):
                priority.append(file_name)

        print(priority)


def main():
    pass


if __name__ == "__main__":
    main()
