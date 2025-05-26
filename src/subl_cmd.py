"""Entrypoint file of plugin."""

import os
import shutil
import subprocess

try:
    from loguru import logger
except ImportError:
    from Automatons.src.mocks.mock_loguru import MockLogger
    logger = MockLogger()

import sublime
import sublime_plugin

try:
    from Automatons.src.lib.gen_template import (
        BuildTemplate,
        ChangelogTemplate,
        GitignoreTemplate,
        ReadmeTemplate,
        SrcTemplate,
        TbTemplate,
    )
except ImportError:
    from src.lib.gen_template import (
        BuildTemplate,
        ChangelogTemplate,
        GitignoreTemplate,
        ReadmeTemplate,
        SrcTemplate,
        TbTemplate,
    )


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

    def __init__(self, window: sublime.Window) -> None:
        """Init."""
        super().__init__(window)

        self.dir_doc = "doc"
        self.dir_script = "script"
        self.dir_src = "src"
        self.dir_tb = "tb"
        self.dir_sdk = "sdk"
        self.dir_xdc = "xdc"

        self.__GIT_IGNORE_EXT__ = ".gitignore"

        self.path2prj = ""

    def run(self) -> None:
        """Command body."""
        self.path2prj = self.window.project_file_name()

        if self.path2prj is None:
            sublime.message_dialog("Project file is not found. Please check that the project is open")
            return
        self.path2prj = os.path.dirname(self.path2prj)

        for entry in os.listdir(self.path2prj):
            if os.path.isdir(os.path.join(self.path2prj, entry)):
                sublime.message_dialog("Project is not empty")
                return

        self.create_folder_structure(self.path2prj)
        self.add_folder_to_prj(self.path2prj)
        self.add_files(self.path2prj)

        self.init_git_repository()

    def create_folder_structure(self, path: str) -> None:
        """Form folders structure."""
        os.makedirs(os.path.join(path, self.dir_doc), exist_ok=True)
        os.makedirs(os.path.join(path, self.dir_script), exist_ok=True)
        os.makedirs(os.path.join(path, self.dir_src), exist_ok=True)
        os.makedirs(os.path.join(path, self.dir_tb), exist_ok=True)
        os.makedirs(os.path.join(path, self.dir_sdk), exist_ok=True)
        os.makedirs(os.path.join(path, self.dir_xdc), exist_ok=True)

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
        with open(os.path.join(path, self.__GIT_IGNORE_EXT__), "w") as f:
            git_tmp = GitignoreTemplate()
            f.write(git_tmp.insert())

        with open(os.path.join(path, self.dir_src, "main.v"), "w") as f:
            src_main = SrcTemplate()
            src_main.name = "main"
            f.write(src_main.insert())

        with open(os.path.join(path, self.dir_tb, "main_tb.v"), "w") as f:
            tb_main = TbTemplate()
            tb_main.name = "main"
            f.write(tb_main.insert())

        with open(os.path.join(path, "README.md"), "w") as f:
            readme = ReadmeTemplate()
            f.write(readme.insert())

        with open(os.path.join(path, "CHANGELOG.md"), "w") as f:
            changelog = ChangelogTemplate()
            f.write(changelog.insert())

        with open(os.path.join(path, self.dir_script, "build.tcl"), "w") as f:
            build_script = BuildTemplate()
            f.write(build_script.insert())

        with open(os.path.join(path, self.dir_script, "pcore_bd.tcl"), "w") as f:
            f.write("")

        with open(os.path.join(path, self.dir_xdc, "main.xdc"), "w") as f:
            f.write("")

    def init_git_repository(self) -> None:
        """Initialize a git repository in the specified directory."""
        try:
            subprocess.run(["git", "init"], cwd=self.path2prj, check=True)

            msg = "Git repository successfully initialized in " + self.path2prj
            logger.info(msg)
        except subprocess.CalledProcessError:
            logger.exception("Error initializing git repository")


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
