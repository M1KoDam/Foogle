import wx


APP_SETTINGS = 1
APP_OPEN_DIRECTORY = 2
APP_FIND_PHRASE = 3


class FMenuBar(wx.MenuBar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.add_file()
        self.add_actions()
        self.parent.SetMenuBar(self)

        self.parent.Bind(wx.EVT_MENU, self.parent.onSettings, id=APP_SETTINGS)
        self.parent.Bind(wx.EVT_MENU, self.parent.onQuit, id=wx.ID_EXIT)

    def add_file(self):
        file_menu = wx.Menu()

        settings_item = wx.MenuItem(file_menu, APP_SETTINGS, "Settings\tCtrl+S", "App settings")
        file_menu.Append(settings_item)

        file_menu.AppendSeparator()

        exit_item = wx.MenuItem(file_menu, wx.ID_EXIT, "Exit\tCtrl+Q", "App exit")
        file_menu.Append(exit_item)

        self.Append(file_menu, "&File")

    def add_actions(self):
        actions_menu = wx.Menu()

        undo_item = wx.MenuItem(actions_menu, wx.ID_UNDO, "Undo\tCtrl+Z", "undo")
        actions_menu.Append(undo_item)

        redo_item = wx.MenuItem(actions_menu, wx.ID_REDO, "Redo\tCtrl+Shift+Z", "redo")
        actions_menu.Append(redo_item)

        self.Append(actions_menu, "&Actions")


class FHorBox(wx.BoxSizer):
    def __init__(self, parent, text, image, button_id, value, bind_func):
        super().__init__(wx.HORIZONTAL)

        self.tc = wx.TextCtrl(parent, value=value)
        self.st = wx.StaticText(parent, label=text)
        self.bitmap_button = wx.BitmapButton(parent, button_id, bitmap=wx.Bitmap(image))

        self.Add(self.st, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=3)
        self.Add(self.tc, proportion=1, flag=wx.LEFT | wx.RIGHT, border=8)
        self.Add(self.bitmap_button, flag=wx.LEFT | wx.RIGHT, border=3)

        self.bitmap_button.Bind(wx.EVT_BUTTON, bind_func)


class FOutputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.filePanel = wx.Panel(self)
        self.fileSizer = wx.BoxSizer(wx.VERTICAL)
        self.filePanel.SetSizer(self.fileSizer)

        self.textPanel = wx.Panel(self)
        self.textSizer = wx.BoxSizer(wx.VERTICAL)
        self.text_field = wx.TextCtrl(self.textPanel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.textSizer.Add(self.text_field, 1, wx.EXPAND)
        self.textPanel.SetSizer(self.textSizer)

        self.hBoxSizer.Add(self.filePanel, 1, wx.EXPAND)
        self.hBoxSizer.Add(self.textPanel, 1, wx.EXPAND)
        self.SetSizer(self.hBoxSizer)

    def add_files(self, files_names: list):
        self.fileSizer.Clear(True)
        for file_name in files_names:
            file_name = file_name[len(self.parent.directoryBox.tc.Value) + 1:]
            button = wx.Button(self.filePanel, label=file_name)
            self.fileSizer.Add(button, wx.ID_ANY, flag=wx.ALL, border=3)
            button.Bind(wx.EVT_BUTTON, lambda event, name=file_name: self.get_file_data(event, name))

        self.filePanel.Layout()
        self.filePanel.SetSizer(self.fileSizer)

    def get_file_data(self, event, file_name):
        self.text_field.Clear()
        encoding = ['utf-8', 'cp1251', 'cp1252', 'cp437', 'utf-16be']
        for e in encoding:
            try:
                with open(self.parent.directoryBox.tc.Value + "/" + file_name, 'r', encoding=e) as file:
                    self.text_field.Value = file.read()
                break
            except UnicodeDecodeError:
                pass


class InputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.default_directory = r'TestFiles'
        self.default_phrase = "главны приоритетов в жизнях"

        self.out_box_sizer = wx.BoxSizer(wx.VERTICAL)

        self.directoryBox = FHorBox(
            self,
            text="Directory: ",
            image="Data/Icons/directory16.png",
            button_id=APP_OPEN_DIRECTORY,
            value=self.default_directory,
            bind_func=self.parent.onChooseDirectory
        )
        self.out_box_sizer.Add(self.directoryBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.phraseBox = FHorBox(
            self,
            text="Phrase: ",
            image="Data/Icons/search16.png",
            button_id=APP_FIND_PHRASE,
            value=self.default_phrase,
            bind_func=self.parent.onFindPhrase
        )
        self.out_box_sizer.Add(self.phraseBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.fOutputPanel = FOutputPanel(self)
        self.out_box_sizer.Add(self.fOutputPanel, wx.ID_ANY, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(self.out_box_sizer)

        # self.file_panel = None
        # self.file_sizer = None
        # self.text_field = None
        # self.create_files_output()


def main():
    pass


if __name__ == "__main__":
    main()
