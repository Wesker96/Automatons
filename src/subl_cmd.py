"""Entrypoint file of plugin."""

import os
import shutil

try:
    from loguru import logger
except ImportError:
    from Automatons.src.mocks.mock_loguru import MockLogger
    logger = MockLogger()

import sublime
import sublime_plugin

try:
    from Automatons.src.lib.gen_template import GitignoreTemplate, SrcTemplate, TbTemplate
except ImportError:
    from src.lib.gen_template import GitignoreTemplate, SrcTemplate, TbTemplate


class SrcTemplateCommand(sublime_plugin.TextCommand):
    """Command to generate the source template."""

    def run(self, edit: sublime.Edit, syntax: str) -> None:
        """Command body."""
        obj_test = SrcTemplate()

        cursor_position = self.view.sel()[0].begin()
        self.view.insert(edit, cursor_position, obj_test.insert())

        self.view.set_syntax_file(syntax)

        logger.info("run")


class TbTemplateCommand(sublime_plugin.TextCommand):
    """Command to generate the testbench template."""

    def run(self, edit: sublime.Edit, syntax: str) -> None:
        """Command body."""
        obj_test = TbTemplate()

        cursor_position = self.view.sel()[0].begin()
        self.view.insert(edit, cursor_position, obj_test.insert())

        self.view.set_syntax_file(syntax)


class CreateStructProjectCommand(sublime_plugin.WindowCommand):
    """Command to generate the structure of hdl-project."""

    def run(self) -> None:
        """Command body."""
        path2prj = self.window.project_file_name()

        if path2prj is None:
            sublime.message_dialog("Project file is not found. Please check that the project is open")
            return
        path2prj = os.path.dirname(path2prj)

        for entry in os.listdir(path2prj):
            if os.path.isdir(os.path.join(path2prj, entry)):
                sublime.message_dialog("Project is not empty")
                return

        self.create_folder_structure(path2prj)
        self.add_folder_to_prj(path2prj)
        self.add_files(path2prj)

    @staticmethod
    def create_folder_structure(path: str) -> None:
        """Form folders structure."""
        os.makedirs(os.path.join(path, "doc"), exist_ok=True)
        os.makedirs(os.path.join(path, "script"), exist_ok=True)
        os.makedirs(os.path.join(path, "src"), exist_ok=True)
        os.makedirs(os.path.join(path, "tb"), exist_ok=True)

    def add_folder_to_prj(self, path: str) -> None:
        """
        Create file of subl-project.

        more info: https://www.sublimetext.com/docs/projects.html
        """
        project_data = self.window.project_data()

        folders = [{"path": path, "file_exclude_patterns": ["*.sublime-project", "*.sublime-workspace"]},
                   {"settings": {"tab_size": 4}}]
        project_data["folders"] = folders

        self.window.set_project_data(project_data)

    def add_files(self, path: str) -> None:
        """Create any files for core project."""
        git_tmp = GitignoreTemplate()

        with open(os.path.join(path, ".gitignore"), "w") as f:
            f.write(git_tmp.insert())


class DeleteStructProjectCommand(sublime_plugin.WindowCommand):
    """Command to delete the project files. Only for debug."""

    def __init__(self, window: sublime.Window) -> None:
        """Init."""
        super().__init__(window)

        self.__SUBLIME_PROJECT_EXT__ = ".sublime-project"
        self.__SUBLIME_WORKSPACE_EXT__ = ".sublime-workspace"

        self.exclude = (self.__SUBLIME_PROJECT_EXT__, self.__SUBLIME_WORKSPACE_EXT__)

    def run(self) -> None:
        """Delete all files in the specified directory except those with .sublime-* extensions."""
        path2prj = self.window.project_file_name()

        if path2prj is None:
            sublime.message_dialog("Project file is not found. Please check that the project is open")
            return
        path2prj = os.path.dirname(path2prj)

        for filename in os.listdir(path2prj):
            file_path = os.path.join(path2prj, filename)

            if os.path.isfile(file_path) and not filename.endswith(self.exclude):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
