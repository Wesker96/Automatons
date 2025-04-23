import os

import sublime
import sublime_plugin

from .lib.GenTemplate import SrcTemplate, TbTemplate


class SrcTemplateCommand(sublime_plugin.TextCommand):
    def run(self, edit, syntax):
        obj_test = SrcTemplate()

        cursor_position = self.view.sel()[0].begin()
        self.view.insert(edit, cursor_position, obj_test.insert())

        self.view.set_syntax_file(syntax)


class TbTemplateCommand(sublime_plugin.TextCommand):
    def run(self, edit, syntax):
        obj_test = TbTemplate()

        cursor_position = self.view.sel()[0].begin()
        self.view.insert(edit, cursor_position, obj_test.insert())

        self.view.set_syntax_file(syntax)
