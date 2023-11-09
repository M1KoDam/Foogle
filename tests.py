import unittest
from files_finder import FilesFinder
from indexer import Indexer
from algorithm import levenstein_distances, ld, tf_idf


class TestIndexer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIndexer, self).__init__(*args, **kwargs)
        self.directory = "TestFiles"
        self.permissions = ["txt", "py", "ini", "html"]

        self.finder = FilesFinder(path=self.directory,
                                  permissions=self.permissions)

        self.indexer = Indexer(self.finder.get_files_directory(),
                               use_stop_words=True,
                               use_morphy=False,
                               ld_deep=2)

    def test_indexer_phrase(self):
        found_files = self.indexer.find("главны приоритетов в жизнях")
        self.assertEqual(found_files,
                         ['TestFiles\\TestFile1.ini', 'TestFiles\\TestFile3.html', 'TestFiles\\TestFile2.txt'])

    def test_indexer_not_word(self):
        found_files = self.indexer.find("[not] главны")
        self.assertEqual(found_files,
                         ['TestFiles\\TestFile5.txt'])

    def test_indexer_and_word(self):
        found_files = self.indexer.find("деньги [and] главны")
        self.assertEqual(found_files,
                         ['TestFiles\\TestFile1.ini'])

    def test_indexer_or_word(self):
        found_files = self.indexer.find("пустышка [or] главны приоритетов в жизнях")
        self.assertEqual(sorted(found_files),
                         sorted(['TestFiles\\TestFile5.txt', 'TestFiles\\TestFile1.ini',
                                 'TestFiles\\TestFile2.txt', 'TestFiles\\TestFile3.html']))

    def test_indexer_word(self):
        found_files = self.indexer.find("главны")
        self.assertEqual(found_files,
                         ['TestFiles\\TestFile1.ini', 'TestFiles\\TestFile3.html',
                          'TestFiles\\TestFile2.txt', 'TestFiles\\TestFile4.txt'])


class AlgorithmIndexer(unittest.TestCase):
    def test_td_idf(self):
        self.assertEqual(0.12, tf_idf(3, 100, 10000000, 1000))

    def test_levenstein(self):
        self.assertEqual(5, levenstein_distances("привет", "приветствую"))
        self.assertEqual(1, levenstein_distances("cat", "cats"))
        self.assertEqual(0, levenstein_distances("cucumber", "cucumber"))
        self.assertEqual(3, levenstein_distances("тектоник", "тоник"))
        self.assertLessEqual(5, ld("привет", "приветствую", 3))
        self.assertEqual(1, ld("cat", "cats", 3))
        self.assertEqual(0, ld("cucumber", "cucumber", 3))
        self.assertEqual(3, ld("тектоник", "тоник", 3))
        self.assertLessEqual(2, ld("тектоник", "тоник", 3))


if __name__ == "__main__":
    pass
