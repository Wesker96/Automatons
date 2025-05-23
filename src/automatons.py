"""Entrypoint file of plugin."""

import os
import subprocess
import threading

import sublime
import sublime_plugin

from Automatons.src.lib.gen_template import GitignoreTemplate, SrcTemplate, TbTemplate
from Automatons.src.lib.runner import Terminal


class RunVivadoCommand(sublime_plugin.TextCommand):
    """Command to run cmt with vivado."""

    def run(self, edit):
        python_path = "python"

        # Путь к вашему внешнему скрипту
        script_path = "C:/Users/shishkov_ps/AppData/Roaming/Sublime Text/Packages/Automatons/src/lib/runner.py"

        thread = threading.Thread(target=self.run_script, args=(python_path, script_path, self.handle_output))
        thread.start()

    def run_script(self, python_path, script_path, callback):
        vivado_path = os.environ.get("XILINX_VIVADO")
        if vivado_path is None:
            raise EnvironmentError("Переменная окружения XILINX_VIVADO не установлена")
        vivado_path = vivado_path + "\settings64.bat"

        obj = Terminal()
        obj.run_script_0()
        obj.run_script_1(vivado_path)
        obj.stop()

        # process = subprocess.Popen([python_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                            bufsize=1, universal_newlines=True, startupinfo=startupinfo)
        # stdout, stderr = process.communicate()
        # callback(stdout, stderr)

    def handle_output(self, stdout, stderr):
        print("stdout:", stdout)
        print("stderr:", stderr)


class SrcTemplateCommand(sublime_plugin.TextCommand):
    """Command to generate the source template."""

    def run(self, edit, syntax):
        obj_test = SrcTemplate()

        cursor_position = self.view.sel()[0].begin()
        self.view.insert(edit, cursor_position, obj_test.insert())

        self.view.set_syntax_file(syntax)


class TbTemplateCommand(sublime_plugin.TextCommand):
    """Command to generate the testbench template."""

    def run(self, edit, syntax):
        obj_test = TbTemplate()

        cursor_position = self.view.sel()[0].begin()
        self.view.insert(edit, cursor_position, obj_test.insert())

        self.view.set_syntax_file(syntax)


class CreateStructProjectCommand(sublime_plugin.WindowCommand):
    """Command to generate the source template."""

    def run(self):
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
    def create_folder_structure(path):
        os.makedirs(os.path.join(path, "doc"), exist_ok=True)
        os.makedirs(os.path.join(path, "script"), exist_ok=True)
        os.makedirs(os.path.join(path, "src"), exist_ok=True)
        os.makedirs(os.path.join(path, "tb"), exist_ok=True)

    def add_folder_to_prj(self, path):
        project_data = self.window.project_data()

        # folders = project_data.get("folders", [])

        # more info: https://www.sublimetext.com/docs/projects.html
        folders = [{"path": path, "file_exclude_patterns": ["*.sublime-project", "*.sublime-workspace"]},
                   {"settings": {"tab_size": 4}}]
        project_data["folders"] = folders

        self.window.set_project_data(project_data)

    def add_files(self, path):
        git_tmp = GitignoreTemplate()

        with open(os.path.join(path, ".gitignore"), "w") as f:
            f.write(git_tmp.insert())

