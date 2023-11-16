import sys
from indexer import Indexer
from files_finder import FilesFinder
from gui import *
from caching import *
import threading


class Api(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(
            parent,
            title=title,
            size=(640, 480),
            style=wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION
        )

        self.SetIcon(wx.Icon('Data/Icons/icon.png', wx.BITMAP_TYPE_PNG))

        self.menuBar = MenuBar(self)
        self.inputPanel = InputPanel(self)
        self.statusBar = self.CreateStatusBar()

        self.status = "Ready"

        self.index_cache = IndexCache(10000, 10)

        self.ur_cache_size = 30
        self.undo_cache = []
        self.redo_cache = []
        self.cur_ur_cache = None

        self.ignore = None

    def threadFindPhrase(self, use_cache=False):
        self.inputPanel.onBlockButtons()
        self.blockUndoRedoButtons()
        self.inputPanel.onUpdateValues()

        directory = self.inputPanel.get_directory()
        phrase = self.inputPanel.cur_phrase
        found_files = []

        if directory.replace(" ", "") == "":
            DialogueWindows.NotifyDirectoryLineCantBeEmpty()
        elif phrase.replace(" ", "") == "":
            DialogueWindows.NotifyPhraseLineCantBeEmpty()
        elif len(self.menuBar.permissionMenu.permissions) == 0:
            DialogueWindows.NotifyChooseMoreThanZeroPermissions()
        elif not os.path.isdir(directory):
            DialogueWindows.DrawDirectoryOpenError(directory)
        else:
            if use_cache:
                indexer, index, files_word_count, files_directory = self.tryFindIndexInCache(directory)
            else:
                indexer, index, files_word_count, files_directory = self.buildIndex(directory)

            self.onStatusUpdate("Finding...")
            found_files = indexer.find(phrase, index, files_word_count)
            new_cache = CacheElement(directory, phrase, found_files)
            if len(found_files) == 0:
                DialogueWindows.NotifyNoFileFound(directory, phrase)
            else:
                self.updateUndoRedo(new_cache)

            self.onStatusUpdate("Writing to cache...")
            self.index_cache.write_index_to_cache(directory, index, files_word_count, files_directory)

        wx.CallAfter(self.inputPanel.outputPanel.addFileButtons, found_files)
        self.onStatusUpdate("Ready")
        self.inputPanel.onUnblockButtons()

    def tryFindIndexInCache(self, directory: str):
        index, files_word_count, files_directory = self.index_cache.load_index_from_cache(directory)
        if len(index) == 0:
            return self.buildIndex(directory)
        indexer = self.createIndexer(files_directory)
        return indexer, index, files_word_count, files_directory

    def buildIndex(self, directory: str):
        self.onStatusUpdate("Looking for files...")
        finder = FilesFinder(path=directory,
                             ignore=self.ignore,
                             permissions=self.menuBar.permissionMenu.permissions)
        files_directory = finder.get_files_directory()
        self.onStatusUpdate("Creating an index...")
        indexer = self.createIndexer(files_directory)
        index, files_word_count = indexer.build_index()
        return indexer, index, files_word_count, files_directory

    def createIndexer(self, files_directory: list):
        return Indexer(files_directory,
                       use_stop_words=self.menuBar.optionsMenu.use_stop_words,
                       use_morphy=self.menuBar.optionsMenu.use_morphy,
                       ld_deep=self.menuBar.optionsMenu.ldMenu.ld)

    def onFindPhraseUsingCache(self, event):
        thread = threading.Thread(target=self.threadFindPhrase, kwargs={'use_cache': True})
        thread.start()

    def onReBuildIndex(self, event):
        thread = threading.Thread(target=self.threadFindPhrase, kwargs={'use_cache': False})
        thread.start()

    def onQuit(self, event):
        self.Close()
        sys.exit()

    def onStatusUpdate(self, status):
        self.status = status
        self.statusBar.SetStatusText(self.status)

    def onSettings(self, event):
        pass

    def onChooseDirectory(self, event):
        dlg = wx.DirDialog(self, "Выберите директорию", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            directory = dlg.GetPath()
            self.inputPanel.directoryBox.tc.SetValue(directory)

        dlg.Destroy()

    def onUndo(self, event):
        self.addToRedoCache()
        if len(self.undo_cache) > 0:
            self.cur_ur_cache = self.undo_cache.pop()
        self.updateAppByCache()

    def onRedo(self, event):
        self.addToUndoCache()
        if len(self.redo_cache) > 0:
            self.cur_ur_cache = self.redo_cache.pop()
        self.updateAppByCache()

    def updateUndoRedo(self, new_cache: CacheElement):
        self.redo_cache.clear()
        if self.cur_ur_cache is not None and self.cur_ur_cache not in self.undo_cache and self.cur_ur_cache != new_cache:
            self.addToUndoCache()

        self.cur_ur_cache = new_cache
        self.updateUndoRedoButtons()

    def updateAppByCache(self):
        self.inputPanel.cur_directory = self.cur_ur_cache.directory
        self.inputPanel.cur_phrase = self.cur_ur_cache.phrase

        self.inputPanel.directoryBox.tc.SetValue(self.cur_ur_cache.directory)
        self.inputPanel.phraseBox.tc.SetValue(self.cur_ur_cache.phrase)

        self.inputPanel.outputPanel.addFileButtons(self.cur_ur_cache.found_files)
        self.updateUndoRedoButtons()

    def blockUndoRedoButtons(self):
        self.menuBar.actionsMenu.undo_item.Enable(False)
        self.menuBar.actionsMenu.redo_item.Enable(False)

    def updateUndoRedoButtons(self):
        self.menuBar.actionsMenu.undo_item.Enable(True if len(self.undo_cache) > 0 else False)
        self.menuBar.actionsMenu.redo_item.Enable(True if len(self.redo_cache) > 0 else False)

    def addToUndoCache(self):
        self.undo_cache.append(self.cur_ur_cache)
        if len(self.undo_cache) > self.ur_cache_size:
            self.undo_cache.pop(0)

    def addToRedoCache(self):
        self.redo_cache.append(self.cur_ur_cache)
        if len(self.redo_cache) > self.ur_cache_size:
            self.redo_cache.pop(0)


def main():
    # D:\SteamLibrary\steamapps\common\Skyrim Special Edition
    # One or more plugins could not find the correct versions of the master files they depend on.
    # TestFiles
    # главны приоритетов в жизнях
    app = wx.App()
    api = Api(None, "Foogle")
    api.Center()
    api.Show()

    app.MainLoop()


if __name__ == "__main__":
    main()
