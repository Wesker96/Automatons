"""Install plugin script."""
from __future__ import annotations

import os
import shutil

try:
    from loguru import logger
except ImportError:
    from src.mocks.mock_loguru import MockLogger
    logger = MockLogger()

__NAME_ENV_AUTOMATONS__ = "AUTOMATONS"
__PATTERN_OF_SUBL_FOLDER__ = "Sublime Text"


def get_path_to_subl() -> str | None:
    """Search path to Sublime Text into path environment. The path variable must be set in advance."""
    automations_path = os.getenv(__NAME_ENV_AUTOMATONS__)

    if automations_path:
        paths = automations_path.split(os.pathsep)

        for path in paths:
            if __PATTERN_OF_SUBL_FOLDER__ in path:
                return path
    return None


def delete_previous_plugin(dir_path: str, dir_name: str) -> None:
    """Delete previous plugin."""
    previous_plugin_path = os.path.join(dir_path, dir_name)

    if os.path.exists(previous_plugin_path) and os.path.isdir(previous_plugin_path):
        try:
            shutil.rmtree(previous_plugin_path)
            logger.info("Previous plugin founded and delete.")
        except OSError:
            logger.info("Previous plugin founded and try delete, but failed.")
    else:
        logger.info("Previous plugin not founded.")


def install() -> None:
    """Install plugin for Sublime Text."""
    path2subl = get_path_to_subl()

    if path2subl:
        msg = "Find path to Sublime Text: " + path2subl
        logger.info(msg)
    else:
        msg = "Not found path to Sublime Text. Check env path: " + __NAME_ENV_AUTOMATONS__
        logger.info(msg)

    name_prj = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    delete_previous_plugin(path2subl, name_prj)


if __name__ == "__main__":
    install()
