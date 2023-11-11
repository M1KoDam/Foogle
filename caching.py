import json
import datetime


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


class IndexCache:
    def __init__(self, max_write_cache_size: int, max_json_cache_size):
        self.cache_path = "Data/cache/index.json"
        self.cache = self.__load_index_from_json()
        self.max_write_cache_size = max_write_cache_size
        self.max_json_cache_size = max_json_cache_size

    def write_index_to_cache(self, directory: str, index: dict, files_word_count: dict, files_directory: dict):
        self.cache[directory] = (index, files_word_count, files_directory, datetime.datetime.now())
        self.__write_index_to_json()

    def load_index_from_cache(self, directory: str) -> (dict, dict, dict):
        if directory in self.cache.keys():
            index, files_word_count, files_directory, creation_time = self.cache[directory]
            return index, files_word_count, files_directory
        return {}, {}, {}

    def __load_index_from_json(self) -> dict:
        try:
            with open(self.cache_path, "r", encoding='utf-8') as read_file:
                file_data = read_file.read()
                if file_data.strip() != "":
                    return json.loads(file_data, object_hook=datetime_hook)
        except FileNotFoundError:
            with open(self.cache_path, "w", encoding='utf-8'):
                pass
        return {}

    def __write_index_to_json(self):
        write_cache = {}
        with open(self.cache_path, "w", encoding='utf-8') as write_file:
            for key, value in self.cache.items():
                if len(self.cache[key][0]) < self.max_write_cache_size:
                    write_cache[key] = value

            sorted_cache = dict(sorted(list(write_cache.items()), key=lambda x: x[1][3], reverse=True))
            sized_cache = {k: sorted_cache[k] for k in list(sorted_cache)[:self.max_json_cache_size]}
            json.dump(sized_cache, write_file, ensure_ascii=False, default=datetime_handler)


def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return {
            "__type__": "datetime",
            "isoformat": obj.isoformat()
        }
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def datetime_hook(obj):
    if "__type__" in obj and obj["__type__"] == "datetime":
        return datetime.datetime.fromisoformat(obj["isoformat"])
    return obj
