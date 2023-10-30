from indexer import Indexer
from files_finder import FilesFinder


class Api:
    def __init__(self):
        self.__PROGRAM_RUNNING = True
        self.finder = None
        self.files_full_names = None
        self.indexer = None

    def find_files(self, path=r'C:\Users', ignore=None, permissions=None):
        self.finder = FilesFinder(path=path,
                                  ignore=ignore,
                                  permissions=permissions)
        self.files_full_names = self.finder.get_files_directory()
        print(len(self.files_full_names))

    def find_phrase(self, phrase, ld_deep):
        print("Start Finding")
        self.indexer = Indexer(self.files_full_names, ld_deep=ld_deep)
        print(self.indexer.find_phrase(phrase))

        return
        #while self.__PROGRAM_RUNNING:
        #    pass


def main():
    api = Api()
    api.find_files(path=f"D:\SteamLibrary\steamapps\common\Skyrim Special Edition",
                   permissions=["txt", "ini"])
    api.find_phrase("One or more plugins could not find the correct versions of the master files they depend on.", 2)
    api.find_files(path="TestFiles",
                   permissions=["txt", "ini"])
    api.find_phrase("главны приоритетов в жизнях", 2)


if __name__ == "__main__":
    main()
