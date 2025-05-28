"""Collection of file generators."""

import datetime


class BaseTemplate:
    """Base template. Contain general patterns."""

    def __init__(self) -> None:
        """Init, set base patterns."""
        self.body = ""
        self.date = ""

        self.comm_sym = "//"
        self.sep_sec_pattern = "="
        self.sep_code_pattern = "-"
        self.max_length = 120

        self.get_date()

    def insert(self) -> None:
        """Form full template."""

    def get_date(self) -> None:
        """Get date."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        now = now.astimezone()
        self.date = now.strftime("%d.%m.%Y | %H:%M")

    def add_new_line(self, txt: str, pad_h: int = 0, pad_v: int = 0) -> None:
        """Add new line of text."""
        self.body += (" " * pad_h) + txt + "\n" + ("\n" * pad_v)

    def sep_line(self, pattern: str, end: str = "\n") -> str:
        """Generate dividing line."""
        return self.comm_sym + pattern * self.max_length + end

    def wrap_section(self, title: str, end: str = "\n") -> str:
        """Wrap title section."""
        txt = self.sep_line(self.sep_sec_pattern)
        txt += self.comm_sym + " " * ((self.max_length - len(title) - 2) // 2) + title + "\n"
        txt += self.sep_line(self.sep_sec_pattern, end=end)

        return txt


class SrcTemplate(BaseTemplate):
    """Template of verilog source."""

    SECT_DESCRIPTION = "Description"
    SECT_CHECKING = "Checking parameters"
    SECT_VARS = "Vars and genvar signals"
    SECT_INCLUDE = "Includes"
    SECT_LOCAL = "Local parameters"
    SECT_REG = "Registers"
    SECT_INIT_REG = "Init registers"
    SECT_WIRE = "Wires"
    SECT_BEHAVIOR = "Behavior"

    def __init__(self) -> None:
        """Init."""
        super().__init__()

        self.name = "__name__"

    def insert(self) -> str:
        """Form full template."""
        self.add_new_line("`timescale 1ns / 1ps", pad_v=1)
        self.add_new_line(self.wrap_section(self.SECT_DESCRIPTION, end=""))

        txt = "/*\n\nEngineer   : HammerMeow\nDate       : " + self.date
        txt += "\n\nDescription: lorem ipsum\n\n*/\n" + self.sep_line(self.sep_sec_pattern)

        self.add_new_line(txt)

        self.add_new_line(self.get_module())
        self.add_new_line(self.wrap_section(self.SECT_CHECKING), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_VARS), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_INCLUDE), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_LOCAL), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_REG), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_INIT_REG), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_WIRE), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_BEHAVIOR))

        self.add_new_line(self.sep_line(self.sep_code_pattern))

        self.add_new_line("endmodule")

        return self.body

    def get_module(self) -> str:
        """Form base module entity."""
        txt = "module " + self.name + " #(\n"
        txt += "    parameter SIM = 0\n"
        txt += ")(\n"
        txt += "    input                        RST,\n"
        txt += "    input                        CLK\n"
        txt += ");\n"

        return txt


class TbTemplate(BaseTemplate):
    """Template of testbench verilog source."""

    SECT_DESCRIPTION = "Description"
    SECT_PARAMETERS = "Parameters of UUT"
    SECT_IN = "Inputs"
    SECT_OUT = "Outputs"
    SECT_PARSIM = "Parameters for simulation"
    SECT_VARS = "Vars and genvar signals"
    SECT_INCLUDE = "Includes"
    SECT_UUT = "UUT"
    SECT_INIT = "Initial"
    SECT_SUPPORT = "Support logic"
    SECT_TASK = "Local tasks"

    def __init__(self) -> None:
        """Init."""
        super().__init__()

        self.name = "__name__"

        self.name_clk_period = "PERIOD"

    def insert(self) -> str:
        """Form full testbench template."""
        self.add_new_line("`timescale 1ns / 1ps", pad_v=1)
        self.add_new_line(self.wrap_section(self.SECT_DESCRIPTION, end=""))

        txt = "/*\n\nEngineer   : HammerMeow\nDate       : " + self.date
        txt += "\n\nDescription: lorem ipsum\n\n*/\n" + self.sep_line(self.sep_sec_pattern)

        self.add_new_line(txt)

        txt = "module " + self.name + "_tb;"

        self.add_new_line(txt, pad_v=1)

        self.add_new_line(self.wrap_section(self.SECT_PARAMETERS), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_IN), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_OUT), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_PARSIM))
        self.add_new_line(self.get_parameters(), pad_v=1)

        self.add_new_line(self.wrap_section(self.SECT_VARS), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_INCLUDE), pad_v=2)
        self.add_new_line(self.wrap_section(self.SECT_UUT), pad_v=2)

        self.add_new_line(self.wrap_section(self.SECT_INIT))
        self.add_new_line(self.get_initial())

        self.add_new_line(self.wrap_section(self.SECT_SUPPORT))
        self.add_new_line(self.get_clk())

        self.add_new_line(self.wrap_section(self.SECT_TASK), pad_v=2)

        self.add_new_line("endmodule")

        return self.body

    def get_parameters(self) -> str:
        """Form parameters template."""
        return "parameter " + self.name_clk_period + " = 10000;"

    def get_initial(self) -> str:
        """Form initial entity."""
        txt = "initial begin\n"
        txt += "    RST = 1;\n"
        txt += "    #(" + self.name_clk_period + "/2);\n"
        txt += "    #(" + self.name_clk_period + "*15);\n"
        txt += "    RST = 0;\n"
        txt += "    #(" + self.name_clk_period + "*50);\n\n\n"
        txt += "    // user code\n"
        txt += "end\n"

        return txt

    def get_clk(self) -> str:
        """Form clock scheme."""
        txt = "always begin\n"
        txt += "    CLK = 1'b1;\n"
        txt += "    #(" + self.name_clk_period + "/2);\n"
        txt += "    CLK = 1'b0;\n"
        txt += "    #(" + self.name_clk_period + "/2);\n"
        txt += "end\n"

        return txt


class GitignoreTemplate(BaseTemplate):
    """Form .gitignore file."""

    SEC_USER = "User Section"
    SEC_SUBL = "Sublime Text Section"
    SEC_FOLDERS = "Folder Section"
    SEC_EXT = "Extensions Section"

    def __init__(self) -> None:
        """Init and change some patterns."""
        super().__init__()

        self.comm_sym = "#"
        self.max_length = 60

    def insert(self) -> str:
        """Form base .gitignore file."""
        self.add_new_line(self.wrap_section(self.SEC_USER), pad_v=2)

        self.add_new_line(self.wrap_section(self.SEC_SUBL))
        self.add_new_line("*.sublime-workspace", pad_v=1)

        self.add_new_line(self.wrap_section(self.SEC_FOLDERS))
        self.add_new_line("build", pad_v=1)

        self.add_new_line(self.wrap_section(self.SEC_EXT))

        return self.body


class ReadmeTemplate(BaseTemplate):
    """Form readme.md file."""

    def __init__(self) -> None:
        """Init and change some patterns."""
        super().__init__()

    def insert(self) -> str:
        """Form base .gitignore file."""
        self.add_new_line("Readme.")

        return self.body


class ChangelogTemplate(BaseTemplate):
    """Form changelog.md file."""

    def __init__(self) -> None:
        """Init and change some patterns."""
        super().__init__()

    def insert(self) -> str:
        """Form base .gitignore file."""
        txt = "# Changelog\n\n"
        txt += "All notable changes to this project will be documented in this file.\n\n"
        txt += "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), "
        txt += "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n"
        txt += "## [Unreleased]\n\n"
        txt += "### Added\n\n"
        txt += "### Changed\n\n"
        txt += "### Removed\n\n"
        txt += "## [0.0.1] - 2025-05-26\n\n"
        txt += "### Added\n\n"
        txt += "### Changed\n\n"
        txt += "### Removed\n\n"

        self.add_new_line(txt)

        return self.body


class BuildTemplate(BaseTemplate):
    """Form build.tcl file."""

    BAT = 0
    TCL = 0

    def __init__(self) -> None:
        """Init and change some patterns."""
        super().__init__()

        self.path2constrain = ""
        self.path2block_design = "pcore_bd.tcl"

        self.prj_name = "build_tmp"
        self.dir_prj = ""
        self.part = "xc7z020clg400-2"

        self.jobs = 10

        self.dir_tmp = "build"
        self.path2build = "..\\script\\build.tcl"

    def insert(self, file_type: int = TCL) -> str:
        """Form base .gitignore file."""
        if file_type == self.TCL:
            self.add_new_line(self.build_tcl())
        elif file_type == self.BAT:
            self.add_new_line(self.build_bat())
        else:
            pass

        return self.body

    def build_tcl(self) -> str:
        """Generate build.tcl file."""
        txt = ""

        txt += "proc add_sources {source_list} {\n"
        txt += "    set i 0\n"
        txt += "    foreach j $source_list {\n"
        txt += "        add_files $j\n"
        txt += "        incr i\n"
        txt += "    }\n"
        txt += "}\n\n"

        txt += 'set glob_dir_build_scripts "../script"\n'
        txt += 'set path2constrain "../xdc/main.xdc"\n'
        txt += "set source_top main\n"
        txt += "set jobs 10\n\n"

        txt += 'source "$glob_dir_build_scripts/get_list_sources.tcl"'
        txt += "set list_sources [get_final_src_list]"

        txt += "# ---------------------------------------------------------\n\n"

        txt += "create_project -force " + self.prj_name + " -part " + self.part + "\n\n"

        txt += "add_sources list_sources\n"
        txt += "add_files -fileset constrs_1 -norecurse $path2constrain\n\n"

        txt += "set_property top $source_top [current_fileset]\n\n"

        txt += "source " + self.path2block_design + "\n\n"

        txt += "update_compile_order -fileset sources_1\n\n"

        txt += "# ---------------------------------------------------------\n\n"

        txt += "launch_runs synth_1 -jobs " + str(self.jobs) + "\n"
        txt += "wait_on_run synth_1\n\n"

        txt += "launch_runs impl_1 -to_step write_bitstream -jobs " + str(self.jobs) + "\n"
        txt += "wait_on_run impl_1\n"

        return txt

    def build_bat(self) -> str:
        """Generate build_run.bat file."""
        txt = ""

        txt += "chcp 65001\n"
        txt += "@echo off\n\n"

        txt += "@rem --------------------------------------------------------------------------\n"
        txt += "@rem declare constants (paths)\n\n"

        txt += f'set "dir_tmp={self.dir_tmp}"\n'
        txt += f'set "path2build={self.path2build}"\n\n'

        txt += "@rem --------------------------------------------------------------------------\n"
        txt += "@rem remove directory with built project\n\n"

        txt += "if not exist %dir_tmp% (\n"
        txt += "    md %dir_tmp%\n"
        txt += ") else (\n"
        txt += "    echo Found %dir_tmp%. Clear content.\n"
        txt += "    rmdir /s /q %dir_tmp%\n"
        txt += "    md %dir_tmp%\n"
        txt += ")\n\n"

        txt += "@rem --------------------------------------------------------------------------\n"
        txt += "@rem run build script\n\n"

        txt += "cd %dir_tmp%\n\n"

        txt += "@rem cmd /c allows to return to root script without closing terminal window\n\n"

        txt += "if DEFINED XILINX_VIVADO (\n"
        txt += "    cmd /c %XILINX_VIVADO%\\settings64.bat /quet\n"
        txt += "    cmd /c vivado -mode batch -nolog -nojournal -source %path2build% -notrace\n"
        txt += ") else (\n"
        txt += ("    echo don't found XILINX_VIVADO variable. Please set environment variable XILINX_VIVADO - path to "
                "Vivado, where placed settings64.bat. Or run .settings64-Vivado.bat, script that will set variables "
                "automatically.\n")
        txt += ")\n\n"

        txt += "echo Build done. Exit from Vivado.\n\n"

        txt += "exit\n"

        return txt

