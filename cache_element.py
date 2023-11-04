class CacheElement:
    def __init__(self, directory: str, phrase: str, found_files: list):
        self.directory = directory
        self.phrase = phrase
        self.found_files = found_files

    def __eq__(self, other):
        if not isinstance(other, CacheElement) or other is None:
            return False

        if len(self.found_files) != len(other.found_files):
            return False

        for i in range(len(self.found_files)):
            if self.found_files[i] != other.found_files[i]:
                return False

        return self.phrase == other.phrase and self.directory == other.directory

