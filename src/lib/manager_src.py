"""A class to managing sources files for building."""

from __future__ import annotations

import re

try:
    from loguru import logger
except ImportError:
    from Automatons.src.mocks.mock_loguru import MockLogger
    logger = MockLogger()


class SrcListGenerator:
    """A class to generate TCL scripts for managing source file lists."""

    def __init__(self) -> None:
        """Initialize the SrcListGenerator with empty lists for user, exclude, and auto source files."""
        self.user_src_list: list[str] = []
        self.exclude_src_list: list[str] = []
        self.auto_src_list: list[str] = []

    def add_user_src(self, file_path: str) -> None:
        """Add a file path to the user source list."""
        if file_path not in self.user_src_list:
            self.user_src_list.append(file_path)

    def add_exclude_src(self, file_path: str) -> None:
        """Add a file path to the exclude source list."""
        if file_path not in self.exclude_src_list:
            self.exclude_src_list.append(file_path)

    def add_auto_src(self, file_path: str) -> None:
        """Add a file path to the auto source list."""
        if file_path not in self.auto_src_list:
            self.auto_src_list.append(file_path)

    def generate_tcl_script(self) -> str:
        """Generate a TCL script based on the current lists of source files."""
        return """proc get_user_src_list {{}} {{
    return {{
        {}
    }}
}}

proc get_exclude_src_list {{}} {{
    return {{
        {}
    }}
}}

proc get_auto_src_list {{}} {{
    return {{
        {}
    }}
}}

proc get_final_src_list {{}} {{
    set user_src_list [get_user_src_list]
    set exclude_src_list [get_exclude_src_list]
    set auto_src_list [get_auto_src_list]

    array set unique_paths {{}}

    foreach path $user_src_list {{ set unique_paths($path) 1 }}
    foreach path $auto_src_list {{ set unique_paths($path) 1 }}
    foreach path $exclude_src_list {{ unset unique_paths($path) }}

    return [lsort [array names unique_paths]]
}}
""".format(
            "\n        ".join(self.user_src_list),
            "\n        ".join(self.exclude_src_list),
            "\n        ".join(self.auto_src_list),
        )

    def write_tcl_script(self, file_path: str) -> None:
        """Write tcl script."""
        try:
            with open(file_path, "w") as file:
                file.write(self.generate_tcl_script())
        except FileNotFoundError:
            msg = "Not found tcl script: " + file_path
            logger.warning(msg)
            return

    def read_tcl_script(self, file_path: str) -> None:
        """Read an existing TCL script and extract the file lists."""
        try:
            with open(file_path) as file:
                content = file.read()
        except FileNotFoundError:
            msg = "Not found tcl script: " + file_path
            logger.warning(msg)
            return

        self.user_src_list = re.findall(r"get_user_src_list.*?return \{(.*?)\}", content, re.DOTALL)
        self.exclude_src_list = re.findall(r"get_exclude_src_list.*?return \{(.*?)\}", content, re.DOTALL)

        self.user_src_list = self.user_src_list[0].strip().split("\n")
        self.exclude_src_list = self.exclude_src_list[0].strip().split("\n")

        self.user_src_list = [item.strip() for item in self.user_src_list if item.strip()]
        self.exclude_src_list = [item.strip() for item in self.exclude_src_list if item.strip()]
