"""Entrypoint file of plugin."""

try:
    from loguru import logger
except ImportError:
    from Automatons.src.mocks.mock_loguru import MockLogger
    logger = MockLogger()

import sublime
import sublime_plugin

try:
    from Automatons.src.commands.create_struct_project import CreateStructProjectCommand
    from Automatons.src.commands.delete_struct_project import DeleteStructProjectCommand
    from Automatons.src.commands.update_src import UpdateSrcCommand
    from Automatons.src.lib.gen_template import (
        SrcTemplate,
        TbTemplate,
    )
except ImportError:
    from src.commands.create_struct_project import CreateStructProjectCommand
    from src.commands.delete_struct_project import DeleteStructProjectCommand
    from src.commands.update_src import UpdateSrcCommand
    from src.lib.gen_template import (
        SrcTemplate,
        TbTemplate,
    )

__all__ = ["CreateStructProjectCommand", "DeleteStructProjectCommand", "UpdateSrcCommand"]


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


