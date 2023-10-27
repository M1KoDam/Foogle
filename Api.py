from indexer import Indexer

class Api:
    def __init__(self):
        self.__PROGRAM_RUNNING = True

    def run_program(self):
        while self.__PROGRAM_RUNNING:
            pass

def main():
    api = Api()
    #api.run_program()
    indexer = Indexer(["TestFiles/TestFile1.txt", "TestFiles/TestFile2.txt", "TestFiles/TestFile3.txt"])
    indexer.find_phrase("приоритет в жизни")
    indexer.find_phrase("приоритет")


if __name__ == "__main__":
    main()