import sublime
import sublime_plugin

from .lib.GenTemplate import SrcTemplate


class SrcTemplateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        obj_test = SrcTemplate()

        cursor_position = self.view.sel()[0].begin()

        self.view.insert(edit, cursor_position, obj_test.wrap_section(obj_test.SECT_DESCRIPTION))


class TbTemplateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.sel().clear()
        self.view.sel().add_all(self.view.find_all("example"))
