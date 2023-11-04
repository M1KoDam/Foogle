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


def find_bool_operation(phrase: str) -> (bool, bool, bool, list):
    if "[and]" in phrase:
        return True, False, False, phrase.split("[and]")
    if "[or]" in phrase:
        return False, True, False, phrase.split("[or]")
    if "[not]" in phrase:
        return False, False, True, [phrase.replace("[not]", "")]
    return False, False, False, [phrase]


def main():
    pass


if __name__ == "__main__":
    main()
