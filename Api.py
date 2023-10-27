from indexer import Indexer
from files_finder import FilesFinder


class Api:
    def __init__(self):
        self.__PROGRAM_RUNNING = True

    def run_program(self):
        finder = FilesFinder(path="D:\SteamLibrary\steamapps\common\Skyrim Special Edition",
                             permissions=["txt", "ini"])
        finder = FilesFinder(path="TestFiles",
                             permissions=["txt", "ini"])
        indexer = Indexer(finder.get_files_directory())
        print(indexer.find_phrase("главны приоритетов в жизнях"))
        #print(indexer.find_phrase("One or more plugins could not find the correct versions of the master files they depend on."))
        return
        #while self.__PROGRAM_RUNNING:
        #    pass


def main():
    api = Api()
    api.run_program()


if __name__ == "__main__":
    main()
