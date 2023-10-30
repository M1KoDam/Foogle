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
    if string1 == string2:
        return deep
    if len(string1) == 0:
        return deep+len(string2)
    if len(string2) == 0:
        return deep+len(string1)
    if string1[-1] == string2[-1]:
        return ld(string1[:-1], string2[:-1], max_deep, deep)

    if deep > max_deep:
        return 10000

    return min(ld(string1[:-1], string2, max_deep, deep + 1),
               ld(string1[:-1], string2[:-1], max_deep, deep + 1),
               ld(string1, string2[:-1], max_deep, deep + 1))


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
    def try_get_word_ld(word: str, coll: list, ld_deep: int) -> str:
        best_item = " "
        best_ld_deep = 100000
        for item in coll:
            ld_result = ld(word, item, ld_deep)
            if ld_result <= ld_deep and best_ld_deep > ld_result:
                best_item = item
                best_ld_deep = ld_result
        return best_item


def main():
    print(levenstein_distances("главный", "главны"))
    print(ld("главный", "главны", 1))
    print(ld("abcdegz", "abcde", 3))
    print(ld("abcdefghijk", "iucdefhyhij", 3))


if __name__ == "__main__":
    main()
