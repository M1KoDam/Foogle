import math


def levenstein_distances(string1: str, string2: str) -> int:
    if string1 == string2:
        return 0
    if len(string1) == 0:
        return len(string2)
    if len(string2) == 0:
        return len(string1)
    if string1[-1] == string2[-1]:
        return levenstein_distances(string1[:-1], string2[:-1])

    return min(1 + levenstein_distances(string1[:-1], string2),
               1 + levenstein_distances(string1[:-1], string2[:-1]),
               1 + levenstein_distances(string1, string2[:-1]))


def ld(string1: str, string2: str, max_deep: int, deep=0) -> int:
    if deep > max_deep:
        return 10000
    if string1 == string2:
        return deep
    if len(string1) == 0:
        deep = deep + len(string2)
        return 10000 if deep > max_deep else deep
    if len(string2) == 0:
        deep = deep + len(string1)
        return 10000 if deep > max_deep else deep
    if string1[-1] == string2[-1]:
        return ld(string1[:-1], string2[:-1], max_deep, deep)

    return min(ld(string1[:-1], string2, max_deep, deep + 1),
               ld(string1[:-1], string2[:-1], max_deep, deep + 1),
               ld(string1, string2[:-1], max_deep, deep + 1))


def tf_idf(word_in_file: int,
           file_words_count: int,
           files_count: int,
           files_count_with_word: int,
           priority_range=0) -> float:
    tf = word_in_file / file_words_count
    itf = math.log10(files_count / files_count_with_word)
    power = tf * itf

    if power > priority_range:
        return power
    return 0


class LD:
    @staticmethod
    def equals_ld(string1: str, string2: str, ld_deep: int) -> bool:
        if ld(string1, string2, ld_deep) <= ld_deep:
            return True
        return False

    @staticmethod
    def list_in_list_ld(sub_coll: list, main_coll: list, ld_deep: int) -> bool:
        for word in sub_coll:
            eq = False
            for item in main_coll:
                if LD.equals_ld(word, item, ld_deep):
                    eq = True
            if not eq:
                return False
        return True

    @staticmethod
    def word_in_list_ld(word: str, coll: list, ld_deep: int):
        for item in coll:
            if LD.equals_ld(word, item, ld_deep):
                return True
        return False

    @staticmethod
    def try_get_words_ld(word: str, coll: list, ld_deep: int) -> (list, str):
        best_item = ""
        ld_best = 10000
        items = []
        for item in coll:
            ld_result = ld(word, item, ld_deep)
            if ld_result <= ld_deep:
                if ld_result < ld_best:
                    best_item = item
                    ld_best = ld_result
                items.append(item)

        return items, best_item


def main():
    print(levenstein_distances("главный", "главны"))
    print(ld("главный", "главны", 1))
    print(ld("abcdegz", "abcde", 3))
    print(ld("abcdefghijk", "iucdefhyhij", 3))


if __name__ == "__main__":
    main()
