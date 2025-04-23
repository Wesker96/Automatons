import os
import json

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


class CreateStructProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        path2prj = self.window.project_file_name()

        if path2prj is None:
            sublime.message_dialog("Project file is not found. Please check that the project is open")
            return None
        else:
            path2prj = os.path.dirname(path2prj)

        for entry in os.listdir(path2prj):
            if os.path.isdir(os.path.join(path2prj, entry)):
                sublime.message_dialog("Project is not empty")
                return None

        self.create_folder_structure(path2prj)
        self.add_folder_to_prj(path2prj)

    @staticmethod
    def create_folder_structure(path):
        os.makedirs(os.path.join(path, "doc"), exist_ok=True)
        os.makedirs(os.path.join(path, "src"), exist_ok=True)
        os.makedirs(os.path.join(path, "tb"), exist_ok=True)

    def add_folder_to_prj(self, path):
        project_data = self.window.project_data()

        folders = project_data.get("folders", [])
        folders.append({"path": path})
        project_data["folders"] = folders

        self.window.set_project_data(project_data)
