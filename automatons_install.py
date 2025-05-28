"""Install plugin script."""
from __future__ import annotations

import os
import shutil
import sys

try:
    from loguru import logger
except ImportError:
    from src.mocks.mock_loguru import MockLogger
    logger = MockLogger()

__NAME_ENV_AUTOMATONS__ = "AUTOMATONS"
__PATTERN_OF_SUBL_FOLDER__ = "Sublime Text"
__PLUGIN_TREE__ = [
    "src",
    "automatons.py",
    "automatons.sublime-commands",
    "rtl.sublime-build",
    "Main.sublime-menu",
    ".python-version",
    "CHANGELOG.md",
    "README.md",
    "LICENSE",
]


def get_path_to_subl() -> str | None:
    """Search path to Sublime Text into path environment. The path variable must be set in advance."""
    automations_path = os.getenv(__NAME_ENV_AUTOMATONS__)

    if automations_path:
        paths = automations_path.split(os.pathsep)

        for path in paths:
            if __PATTERN_OF_SUBL_FOLDER__ in path:
                return path
    return None


def delete_previous_plugin(dir_path: str) -> None:
    """Delete previous plugin."""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        try:
            shutil.rmtree(dir_path)
            logger.info("Previous plugin founded and delete.")
        except OSError:
            logger.info("Previous plugin founded and try delete, but failed.")
    else:
        logger.info("Previous plugin not founded.")


def make_dir_new_plugin(dir_path: str) -> None:
    """Create directory for plugin."""
    logger.info("Create directory for the plugin.")
    try:
        os.makedirs(dir_path)
        logger.info("Done.")
    except OSError:
        logger.info("Failed.")

        sys.exit(0)


def copy_new_plugin(source_path: str, destination_path: str) -> None:
    """Copy all needed sources to Sublime Text."""
    for plugin_node_path in __PLUGIN_TREE__:
        plugin_node_path_abs = os.path.join(source_path, plugin_node_path)

        try:
            msg = "Copy: " + plugin_node_path_abs
            logger.info(msg)

            if os.path.isfile(plugin_node_path_abs):
                shutil.copy(plugin_node_path_abs, destination_path)
            elif os.path.isdir(plugin_node_path_abs):
                dest_dir = os.path.join(destination_path, os.path.basename(plugin_node_path))
                shutil.copytree(plugin_node_path_abs, dest_dir)
            else:
                logger.warning("Path not file or folder.")
        except Exception:
            logger.exception("Found error.")


def install() -> None:
    """Install plugin for Sublime Text."""
    path2subl = get_path_to_subl()

    if path2subl:
        msg = "Find path to Sublime Text: " + path2subl
        logger.info(msg)
    else:
        msg = "Not found path to Sublime Text. Check env path: " + __NAME_ENV_AUTOMATONS__
        logger.info(msg)

    current_plugin_dir = os.path.dirname(os.path.abspath(__file__))
    name_prj = os.path.basename(current_plugin_dir)
    previous_plugin_path = os.path.join(path2subl, name_prj)
    new_plugin_path = previous_plugin_path

    delete_previous_plugin(previous_plugin_path)
    make_dir_new_plugin(new_plugin_path)

    copy_new_plugin(current_plugin_dir, new_plugin_path)


if __name__ == "__main__":
    install()
