"""Command to create a sample project."""

import os

try:
    from loguru import logger
except ImportError:
    from Automatons.src.mocks.mock_loguru import MockLogger
    logger = MockLogger()

import sublime
import sublime_plugin

try:
    from Automatons.src.lib.manager_src import SrcListGenerator
except ImportError:
    from src.lib.manager_src import SrcListGenerator


class UpdateSrcCommand(sublime_plugin.WindowCommand):
    """Command to update source list."""

    def __init__(self, window: sublime.Window) -> None:
        """Init."""
        super().__init__(window)

        self.dir_script = "script"
        self.dir_src = "src"

        self.path2prj = ""

    def run(self) -> None:
        """Command body."""
        self.path2prj = self.window.project_file_name()

        if self.path2prj is None:
            sublime.message_dialog("Project file is not found. Please check that the project is open")
            return
        self.path2prj = os.path.dirname(self.path2prj)

        path2script = os.path.join(self.path2prj, self.dir_script, "get_list_sources.tcl")

        src_list_script = SrcListGenerator()
        src_list_script.read_tcl_script(path2script)

        for root, _, files in os.walk(os.path.join(self.path2prj, self.dir_src)):
            for file in files:
                if file.endswith((".v", ".sv", ".vhd")):
                    src_list_script.add_auto_src(os.path.join(root, file))

        src_list_script.write_tcl_script(path2script)
