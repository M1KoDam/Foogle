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
    def __init__(self, ld_deep):
        self.ld_deep = ld_deep

    def equals_ld(self, string1: str, string2: str) -> bool:
        if ld(string1, string2, self.ld_deep) <= self.ld_deep:
            return True
        return False

    def list_in_list_ld(self, sub_coll: list, main_coll: list) -> bool:
        for word in sub_coll:
            eq = False
            for item in main_coll:
                if self.equals_ld(word, item):
                    eq = True
            if not eq:
                return False
        return True

    def word_in_list_ld(self, word: str, coll: list):
        for item in coll:
            if self.equals_ld(word, item):
                return True
        return False

    def try_get_word_ld(self, word: str, coll: list) -> str:
        for item in coll:
            if self.equals_ld(word, item):
                return item
        return " "


def main():
    print(ld("yabxe", "abcde", 3))
    print(ld("abcdegz", "abcde", 3))
    print(ld("abcdefghijk", "iucdefhyhij", 3))


if __name__ == "__main__":
    main()
