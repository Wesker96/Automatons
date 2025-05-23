from datetime import datetime


class BaseTemplate:
    def __init__(self):
        self.body = ""
        self.date = ""

        self.comm_sym = "//"
        self.sep_sec_pattern = "="
        self.sep_code_pattern = "-"
        self.max_length = 120

        self.get_date()

    def insert(self):
        pass

    def get_date(self):
        now = datetime.now()
        self.date = now.strftime("%d.%m.%Y | %H:%M")

    def add_new_line(self, txt, pad_h=0, pad_v=0):
        self.body += (" " * pad_h) + txt + "\n" + ("\n" * pad_v)

    def sep_line(self, pattern: str):
        return self.comm_sym + pattern * self.max_length + "\n"

    def wrap_section(self, title: str):
        txt = self.sep_line(self.sep_sec_pattern)
        txt += self.comm_sym + " " * ((self.max_length - len(title) - 2) // 2) + title + "\n"
        txt += self.sep_line(self.sep_sec_pattern)

        return txt


class SrcTemplate(BaseTemplate):
    SECT_DESCRIPTION = "Description"
    SECT_CHECKING = "Checking parameters"
    SECT_VARS = "Vars and genvar signals"
    SECT_INCLUDE = "Includes"
    SECT_LOCAL = "Local parameters"
    SECT_REG = "Registers"
    SECT_INIT_REG = "Init registers"
    SECT_WIRE = "Wires"
    SECT_BEHAVIOR = "Behavior"

    def __init__(self):
        super().__init__()

    def insert(self):
        self.add_new_line("`timescale 1ns / 1ps", pad_v=1)
        self.add_new_line(self.wrap_section(self.SECT_DESCRIPTION))

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

    @staticmethod
    def get_module():
        txt = "module __name__ #(\n"
        txt += "    parameter SIM = 0\n"
        txt += ")(\n"
        txt += "    input                        RST,\n"
        txt += "    input                        CLK\n"
        txt += ");\n"

        return txt


class TbTemplate(BaseTemplate):
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

    def __init__(self):
        super().__init__()

        self.name_clk_period = "PERIOD"

    def insert(self):
        self.add_new_line("`timescale 1ns / 1ps", pad_v=1)
        self.add_new_line(self.wrap_section(self.SECT_DESCRIPTION))

        txt = "/*\n\nEngineer   : HammerMeow\nDate       : " + self.date
        txt += "\n\nDescription: lorem ipsum\n\n*/\n" + self.sep_line(self.sep_sec_pattern)

        self.add_new_line(txt)

        txt = "module __name__ _tb;"

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

    def get_parameters(self):
        return "parameter " + self.name_clk_period + " = 10000;"

    def get_initial(self):
        txt = "initial begin\n"
        txt += "    RST = 1;\n"
        txt += "    #(" + self.name_clk_period + "/2);\n"
        txt += "    #(" + self.name_clk_period + "*15);\n"
        txt += "    RST = 0;\n"
        txt += "    #(" + self.name_clk_period + "*50);\n\n\n"
        txt += "    // user code\n"
        txt += "end\n"

        return txt

    def get_clk(self):
        txt = "always begin\n"
        txt += "    CLK = 1'b1;\n"
        txt += "    #(" + self.name_clk_period + "/2);\n"
        txt += "    CLK = 1'b0;\n"
        txt += "    #(" + self.name_clk_period + "/2);\n"
        txt += "end\n"

        return txt


class GitignoreTemplate(BaseTemplate):
    SEC_USER = "User Section"
    SEC_SUBL = "Sublime Text Section"
    SEC_FOLDERS = "Folder Section"
    SEC_EXT = "Extensions Section"

    def __init__(self):
        super().__init__()

        self.comm_sym = "#"
        self.max_length = 60

    def insert(self):
        self.add_new_line(self.wrap_section(self.SEC_USER), pad_v=2)

        self.add_new_line(self.wrap_section(self.SEC_SUBL))
        self.add_new_line("*.sublime-workspace", pad_v=1)

        self.add_new_line(self.wrap_section(self.SEC_FOLDERS))
        self.add_new_line("build", pad_v=1)

        self.add_new_line(self.wrap_section(self.SEC_EXT))

        return self.body

