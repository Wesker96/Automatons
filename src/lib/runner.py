"""Example to run Vivado from terminal."""

import subprocess

from loguru import logger


def run_command_live(cmd: str) -> None:
    """
    Run command to terminal.

    :param cmd: command.
    """
    cmd = cmd.split()

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="cp866",
    )

    for line in iter(process.stdout.readline, ""):
        logger.info(line, end="")
    process.stdout.close()
    process.wait()


if __name__ == "__main__":
    run_command_live("%XILINX_VIVADO%/settings64.bat")
    run_command_live("vivado")
