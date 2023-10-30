import json


def write_json(write_from: str, write_to: str):
    with open(write_from, 'r', encoding='utf-8') as file:
        data = file.readlines()
        data = [string.replace("\n", "") for string in data]
        with open(write_to, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)


def main():
    write_json("StopWords/stopwords-ru.txt", "StopWords/stopwords-ru.json")
    write_json("StopWords/stopwords-eng.txt", "StopWords/stopwords-eng.json")


if __name__ == "__main__":
    main()
