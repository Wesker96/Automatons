"""Command to delete project. Mainly for debugging."""

import os
import shutil

try:
    from loguru import logger
except ImportError:
    from Automatons.src.mocks.mock_loguru import MockLogger
    logger = MockLogger()

import sublime
import sublime_plugin


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
