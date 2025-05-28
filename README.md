# Automatons
Automatons for Sublime Text 4. Based on Python 3.8.

Dependencies:
 - [Plugin: Verilog](https://packagecontrol.io/packages/Verilog)

Clone repo to 'user\AppData\Roaming\Sublime Text\Packages' or run `automatons_install.py` script from anywhere.
The environment variables must declare the `AUTOMATONS` variable with the path to where the plugin should be placed and `XILINX_VIVADO` with the path to Vivado (for example Vivado\2024.2)

#### Install

For install plugin from anywhere run:

```bash
python automatons_install.py
```

#### How to configure project

```bash
uv sync --extra dev --link-mode=copy
```

For run Ruff:

```bash
uv run ruff check .
```
