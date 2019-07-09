import neovim
import os
import re


def analyze_method(method_string: str):
    """
    Analyze an method string to get arguments infomation.

    Parameters
    ---
    method_string: str
        method string

    Example
    ---
    input: def hoge     (     num: int,     nam: str):
    """
    # TODO (himkt): use re
    return method_string.strip()


@neovim.plugin
class Main(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('Docstring', sync=True)
    def generate_docstring(self):
        command = 'echo line(".")'  # FIXME: couldn't find suitable neovim API
        current_line_number = self.nvim.command_output(command) # FIXME
        current_line_number = int(current_line_number)-1
        self.nvim.command(f'echo {current_line_number}')

        current_line = self.nvim.current.line
        self.nvim.command(f'echo {dir(self.nvim.current)}')
        self.nvim.command(f'echo "{current_line}"')
        self.nvim.command(f'echo {dir(self.nvim.current.buffer)}')

        if not current_line.startswith('def '):
            return

        cursor = 0
        method_string = ""
        while True:
            method_string += self.nvim.current.buffer[current_line_number+cursor]
            if method_string.endswith('):'):
                break
            cursor += 1

        signature = analyze_method(method_string)
        self.nvim.command(f'echo "{signature}"')

        # self.nvim.current.buffer.append(docstring, current_line_number)
