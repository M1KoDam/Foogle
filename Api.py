import sys
from indexer import Indexer
from files_finder import FilesFinder
from GUI import *
import threading


class Api(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(
            parent,
            title=title,
            size=(640, 480),
            style=wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION
        )

        self.manuBar = FMenuBar(self)
        self.inputPanel = InputPanel(self)
        self.statusBar = self.CreateStatusBar()

        self.ld_deep = 2
        self.status = "Ready"

        self.ignore = None
        self.permissions = ["txt", "ini"]
        self.finder = FilesFinder(path=self.inputPanel.directoryBox.tc.Value,
                                  ignore=self.ignore,
                                  permissions=self.permissions)

    def threadFindPhrase(self):
        self.onStatusUpdate("Looking for files...")
        self.finder = FilesFinder(path=self.inputPanel.directoryBox.tc.Value,
                                  ignore=self.ignore,
                                  permissions=self.permissions)
        files_directory = self.finder.get_files_directory()
        self.onStatusUpdate("Creating an index...")
        phrase = self.inputPanel.phraseBox.tc.Value
        indexer = Indexer(files_directory, ld_deep=self.ld_deep)
        wx.CallAfter(self.inputPanel.fOutputPanel.add_files, indexer.find_phrase(phrase))
        self.onStatusUpdate("Ready")

    def onFindPhrase(self, event):
        thread = threading.Thread(target=self.threadFindPhrase)
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


def main():
    # api.find_files(path=f"D:\SteamLibrary\steamapps\common\Skyrim Special Edition",
    #               permissions=["txt", "ini"])
    # api.find_phrase("One or more plugins could not find the correct versions of the master files they depend on.")
    # api.find_files(path="TestFiles",
    #               permissions=["txt", "ini"])
    # api.find_phrase("главны приоритетов в жизнях")
    app = wx.App()
    api = Api(None, "Foogle")
    api.Center()
    api.Show()

    app.MainLoop()


if __name__ == "__main__":
    main()
