"""Example to run Vivado from terminal."""

import os
import threading
import subprocess
import time

try:
    from loguru import logger
except ImportError:
    from Automatons.src.mocks.mock_loguru import MockLogger
    logger = MockLogger()


class Terminal:
    def __init__(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        self.proc = subprocess.Popen(
            ['cmd.exe'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            # encoding="cp866",
            bufsize=1,
            universal_newlines=True,
            startupinfo = startupinfo
        )

        self._stop_reader = threading.Event()
        self._cmd_done = threading.Event()
        self.thread = threading.Thread(target=self.reader)
        self.thread.daemon = True
        self.thread.start()
        logger.info("run")

    def run_script_0(self):
        self.send_command("echo off")

    def run_script_1(self, path):
        self.send_command('python --version')
        self.send_command(path)
        self.send_command("vivado")

    def send_command(self, command: str):
        if self.proc.stdin:
            self.proc.stdin.write(command + '\n')
            self.proc.stdin.write('echo __CMD_DONE__\n')
            self.proc.stdin.flush()

        while not self._cmd_done.is_set():
            pass
        self._cmd_done.clear()

    def reader(self):
        while not self._stop_reader.is_set():
            line = self.proc.stdout.readline()
            if not line:
                break
            line = line.strip()

            if line == "__CMD_DONE__":
                self._cmd_done.set()
                continue

            if line:
                logger.info(line)

            time.sleep(0.01)

    def stop(self):
        logger.info("Closing terminal")
        self._stop_reader.set()
        if self.proc.stdin:
            # try:
            self.proc.stdin.write('exit\n')
            self.proc.stdin.flush()
            # except Exception as e:
            #     pass
                # print(f"Error sending exit command: {e}")
        self.proc.wait()
        self.thread.join()
        logger.info("Terminal closed")

    def __del__(self):
        try:
            self.stop()
        except Exception:
            pass


# def run_command_live(cmd: str) -> None:
#     """
#     Run command to terminal.
#
#     :param cmd: command.
#     """
#     cmd = cmd.split()
#
#     process = subprocess.Popen(
#         cmd,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         encoding="cp866",
#         shell=True
#     )
#
#     for line in iter(process.stdout.readline, ""):
#         logger.info(line, end="")
#
#     process.stdout.close()
#     process.wait()


if __name__ == "__main__":
    vivado_path = os.environ.get("XILINX_VIVADO")
    if vivado_path is None:
        raise EnvironmentError("Переменная окружения XILINX_VIVADO не установлена")
    vivado_path = vivado_path + "\settings64.bat"
    # print(vivado_path)
    #
    # run_command_live(vivado_path)
    # run_command_live("vivado")

    obj = Terminal()
    obj.run_script_0()
    obj.run_script_1(vivado_path)
    obj.stop()
