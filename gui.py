import re

import wx
import threading

APP_SETTINGS = 1
APP_OPEN_DIRECTORY = 2
APP_FIND_PHRASE = 3
APP_BUILD_INDEX = 4

ALL = 10150
TXT = 10230
INI = 10231
HTML = 10232
JSON = 10233
CSV = 10234
DLL = 10235
PY = 10236
CS = 10237

LD0 = 11900
LD1 = 11901
LD2 = 11902
LD3 = 11903

USW = 12300

UM = 12560


encoding = ['utf-8', 'cp1251', 'cp1252', 'cp437', 'utf-16be']

class MenuBar(wx.MenuBar):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        self.frame.SetMenuBar(self)

        self.fileMenu = FileMenu(self.frame)
        self.Append(self.fileMenu, "&File")

        self.actionsMenu = ActionsMenu(self.frame)
        self.Append(self.actionsMenu, "Actions")

        self.permissionMenu = PermissionMenu(self.frame)
        self.Append(self.permissionMenu, 'Permissions')

        self.optionsMenu = OptionsMenu(self.frame)
        self.Append(self.optionsMenu, "Options")


class FileMenu(wx.Menu):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        self.exit_item = wx.MenuItem(self, wx.ID_EXIT, "Exit\tCtrl+Q", "App exit")
        self.exit_item.SetBitmap(wx.Bitmap("Data/Icons/exit16.png"))
        self.Append(self.exit_item)

        self.frame.Bind(wx.EVT_MENU, self.frame.onSettings, id=APP_SETTINGS)
        self.frame.Bind(wx.EVT_MENU, self.frame.onQuit, id=wx.ID_EXIT)


class ActionsMenu(wx.Menu):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        self.undo_item = wx.MenuItem(self, wx.ID_UNDO, "Undo\tCtrl+Z", "undo")
        self.Append(self.undo_item)
        self.undo_item.Enable(False)

        self.redo_item = wx.MenuItem(self, wx.ID_REDO, "Redo\tCtrl+Shift+Z", "redo")
        self.Append(self.redo_item)
        self.redo_item.Enable(False)

        self.frame.Bind(wx.EVT_MENU, self.frame.onUndo, id=wx.ID_UNDO)
        self.frame.Bind(wx.EVT_MENU, self.frame.onRedo, id=wx.ID_REDO)


class PermissionMenu(wx.Menu):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.permissions = ['txt', 'ini']

        self.all_item = self.Append(ALL, 'all', kind=wx.ITEM_CHECK)

        self.AppendSeparator()

        self.txt_item = self.Append(TXT, 'txt', kind=wx.ITEM_CHECK)
        self.txt_item.Check(True)
        self.ini_item = self.Append(INI, 'ini', kind=wx.ITEM_CHECK)
        self.ini_item.Check(True)
        self.html_item = self.Append(HTML, 'html', kind=wx.ITEM_CHECK)
        self.json_item = self.Append(JSON, 'json', kind=wx.ITEM_CHECK)
        self.csv_item = self.Append(CSV, 'csv', kind=wx.ITEM_CHECK)
        self.dll_item = self.Append(DLL, 'dll', kind=wx.ITEM_CHECK)
        self.py_item = self.Append(PY, 'py', kind=wx.ITEM_CHECK)
        self.cs_item = self.Append(CS, 'cs', kind=wx.ITEM_CHECK)

        frame.Bind(wx.EVT_MENU, self.onCheckAllItem, self.all_item)

        self.items = [self.txt_item, self.ini_item, self.html_item, self.json_item,
                      self.csv_item, self.dll_item, self.py_item, self.cs_item]
        for item in self.items:
            frame.Bind(wx.EVT_MENU, self.onCheckItem, item)

    def onCheckAllItem(self, event):
        menu_item = self.frame.GetMenuBar().FindItemById(event.GetId())
        if menu_item.IsChecked():
            self.permissions.clear()
            for item in self.items:
                item.Check(True)
                self.permissions.append(item.GetItemLabel())
        else:
            for item in self.items:
                item.Check(False)
                self.permissions.remove(item.GetItemLabel())

    def onCheckItem(self, event):
        menu_item = self.frame.GetMenuBar().FindItemById(event.GetId())
        if menu_item.IsChecked():
            self.permissions.append(menu_item.GetItemLabel())
            if len(self.permissions) == len(self.items):
                self.all_item.Check(True)
        else:
            self.all_item.Check(False)
            self.permissions.remove(menu_item.GetItemLabel())


class LevensteinDistancesMenu(wx.Menu):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.ld = 2

        self.__ld0 = self.Append(LD0, '0', kind=wx.ITEM_RADIO)
        self.__ld1 = self.Append(LD1, '1', kind=wx.ITEM_RADIO)
        self.__ld2 = self.Append(LD2, '2', kind=wx.ITEM_RADIO)
        self.__ld2.Check(True)
        self.__ld3 = self.Append(LD3, '3', kind=wx.ITEM_RADIO)

        self.items = [self.__ld0, self.__ld1, self.__ld2, self.__ld3]
        for item in self.items:
            frame.Bind(wx.EVT_MENU, self.onRadioItem, item)

    def onRadioItem(self, event):
        menu_item = self.frame.GetMenuBar().FindItemById(event.GetId())
        if menu_item.IsChecked():
            self.ld = int(menu_item.GetItemLabel())


class OptionsMenu(wx.Menu):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.use_stop_words = True
        self.use_morphy = False

        self.__usw = self.Append(USW, 'Stop words', kind=wx.ITEM_CHECK)
        self.__usw.Check(True)
        self.__um = self.Append(UM, 'Morphy (RU)', kind=wx.ITEM_CHECK)

        self.AppendSeparator()

        self.ldMenu = LevensteinDistancesMenu(self.frame)
        self.AppendSubMenu(self.ldMenu, "Levenstein Distances")

        frame.Bind(wx.EVT_MENU, self.onCheckUsp, self.__usw)
        frame.Bind(wx.EVT_MENU, self.onCheckUm, self.__um)

    def onCheckUsp(self, event):
        self.use_stop_words = not self.use_stop_words

    def onCheckUm(self, event):
        self.use_morphy = not self.use_morphy


class DialogueWindows:
    @staticmethod
    def DrawDirectoryOpenError(directory):
        wx.MessageBox(f'Error opening directory: {directory}', 'Error')

    @staticmethod
    def DrawFileOpenError(file_name):
        wx.MessageBox(f'Error opening file: {file_name}', 'Error')

    @staticmethod
    def NotifyNoFileFound(directory, phrase):
        wx.MessageBox(f'No file was found on phrase "{phrase}" in directory: {directory}', 'Notify')

    @staticmethod
    def NotifyDirectoryLineCantBeEmpty():
        wx.MessageBox(f'Directory line can`t be empty', 'Notify')

    @staticmethod
    def NotifyPhraseLineCantBeEmpty():
        wx.MessageBox(f'Phrase line can`t be empty', 'Notify')

    @staticmethod
    def NotifyChooseMoreThanZeroPermissions():
        wx.MessageBox(f'Please select at least one permission', 'Notify')


class DirectoryBox(wx.BoxSizer):
    def __init__(self, parent, text, image, button_id, value, bind_func):
        super().__init__(wx.HORIZONTAL)

        self.tc = wx.TextCtrl(parent, value=value)
        self.st = wx.StaticText(parent, label=text)
        self.bitmap_button = wx.BitmapButton(parent, button_id, bitmap=wx.Bitmap(image))

        self.Add(self.st, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=3)
        self.Add(self.tc, proportion=1, flag=wx.LEFT | wx.RIGHT, border=8)
        self.Add(self.bitmap_button, flag=wx.LEFT | wx.RIGHT, border=3)

        self.bitmap_button.Bind(wx.EVT_BUTTON, bind_func)


class PhraseBox(wx.BoxSizer):
    def __init__(self, parent, text, find_image, build_image, find_id, build_id, value, find_func, build_func):
        super().__init__(wx.HORIZONTAL)

        self.tc = wx.TextCtrl(parent, value=value)
        self.st = wx.StaticText(parent, label=text)
        self.find_button = wx.BitmapButton(parent, find_id, bitmap=wx.Bitmap(find_image))
        self.build_button = wx.BitmapButton(parent, build_id, bitmap=wx.Bitmap(build_image))

        self.Add(self.st, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=3)
        self.Add(self.tc, proportion=1, flag=wx.LEFT | wx.RIGHT, border=8)
        self.Add(self.find_button, flag=wx.LEFT | wx.RIGHT, border=3)
        self.Add(self.build_button, flag=wx.LEFT | wx.RIGHT, border=3)

        self.find_button.Bind(wx.EVT_BUTTON, find_func)
        self.build_button.Bind(wx.EVT_BUTTON, build_func)


class OutputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.files_cache = {}

        self.hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.filePanel = wx.Panel(self)
        self.fileSizer = wx.GridSizer(rows=10, cols=1, vgap=5, hgap=5)
        self.filePanel.SetSizer(self.fileSizer)

        self.textPanel = wx.Panel(self)
        self.textSizer = wx.BoxSizer(wx.VERTICAL)
        self.pathLine = wx.TextCtrl(self.textPanel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.textLine = wx.TextCtrl(self.textPanel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.textSizer.Add(self.pathLine, flag=wx.DOWN | wx.EXPAND, border=10)
        self.textSizer.Add(self.textLine, 1, wx.EXPAND)
        self.textPanel.SetSizer(self.textSizer)

        self.hBoxSizer.Add(self.filePanel, 1, flag=wx.EXPAND | wx.TOP, border=5)
        self.hBoxSizer.Add(self.textPanel, 1, flag=wx.EXPAND | wx.LEFT, border=10)
        self.SetSizer(self.hBoxSizer)

    def addFileButtons(self, files_names: list):
        self.clearPanel()
        for file_name in files_names:
            file_name = file_name[len(self.parent.directoryBox.tc.Value):].lstrip('/').lstrip('\\')
            button = wx.Button(self.filePanel, label=file_name)
            self.fileSizer.Add(button, wx.ID_ANY, flag=wx.ALL | wx.EXPAND, border=3)
            button.Bind(wx.EVT_BUTTON, lambda event, name=file_name: self.writeFileInfoToTextLine(event, name))

        self.filePanel.Layout()
        self.filePanel.SetSizer(self.fileSizer)

    def clearPanel(self):
        self.files_cache.clear()
        self.fileSizer.Clear(True)
        self.textLine.Clear()
        self.pathLine.Clear()

    def threadFileInfoToTextLine(self, full_name):
        for e in encoding:
            try:
                with open(full_name, 'r', encoding=e) as file:
                    data = file.read()
                    self.files_cache[full_name] = data
                    self.textLine.SetValue(data)
                    self.pathLine.SetValue(full_name)
                break
            except UnicodeDecodeError:
                pass
            except FileNotFoundError:
                DialogueWindows.DrawFileOpenError(full_name)
                self.textLine.Clear()
                self.pathLine.Clear()
                return

    def writeFileInfoToTextLine(self, event, file_name):
        full_name = f"{self.parent.cur_directory}\\{file_name}"
        if full_name in self.files_cache.keys():
            self.textLine.SetValue(self.files_cache[full_name])
            self.pathLine.SetValue(full_name)
            return

        thread = threading.Thread(target=self.threadFileInfoToTextLine, kwargs={'full_name': full_name})
        thread.start()


class InputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.default_directory = "TestFiles"#os.getcwd()
        self.default_phrase = "главный"

        self.cur_directory = self.default_directory
        self.cur_phrase = self.default_phrase

        self.out_box_sizer = wx.BoxSizer(wx.VERTICAL)

        self.directoryBox = DirectoryBox(
            self,
            text="Directory: ",
            image="Data/Icons/directory16.png",
            button_id=APP_OPEN_DIRECTORY,
            value=self.default_directory,
            bind_func=self.parent.onChooseDirectory
        )
        self.out_box_sizer.Add(self.directoryBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.phraseBox = PhraseBox(
            self,
            text="Phrase: ",
            find_image="Data/Icons/search16.png",
            build_image="Data/Icons/build16.png",
            find_id=APP_FIND_PHRASE,
            build_id=APP_BUILD_INDEX,
            value=self.default_phrase,
            find_func=self.parent.onFindPhraseUsingCache,
            build_func=self.parent.onReBuildIndex
        )
        self.out_box_sizer.Add(self.phraseBox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.outputPanel = OutputPanel(self)
        self.out_box_sizer.Add(self.outputPanel, wx.ID_ANY, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(self.out_box_sizer)

    def onUpdateValues(self):
        self.cur_directory = self.directoryBox.tc.GetValue()
        self.cur_phrase = self.phraseBox.tc.GetValue()

    def onBlockButtons(self):
        self.directoryBox.bitmap_button.Disable()
        self.phraseBox.find_button.Disable()
        self.phraseBox.build_button.Disable()

    def onUnblockButtons(self):
        self.directoryBox.bitmap_button.Enable()
        self.phraseBox.find_button.Enable()
        self.phraseBox.build_button.Enable()

    def get_directory(self):
        if re.fullmatch(r'[A-Z][ :]?[\\/]?', self.cur_directory):
            new_dir = self.cur_directory[0] + ":\\"
            self.cur_directory = new_dir
            self.directoryBox.tc.SetValue(new_dir)
            return new_dir
        else:
            return self.cur_directory


def main():
    pass


if __name__ == "__main__":
    main()
