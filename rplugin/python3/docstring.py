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
    indent = '    '
    indent_result = re.search(r'^\s+', method_string)
    if indent_result:
        indent += indent_result.group(0)

    search_result = re.search(r'\((.*)\)', method_string)
    arguments_string = search_result.group(1)
    arguments_string = arguments_string.replace(' ', '')

    docstrings = ['"""', '<`1:description`>']
    docstrings += ['', 'Parameters', '--------------']

    argument_strings = arguments_string.split(',')
    for index, argument_string in enumerate(argument_strings):
        elem = argument_string.split(':')
        if len(elem) == 2:
            argument, type_string = elem
        else:
            argument, = elem
            type_string = f'<`{index}:type`>'

        line = f'- {argument} ({type_string})'
        line += f': <`{index}:desc`>'
        docstrings.append(line)

    docstrings += ['"""']
    docstrings = list(map(lambda d: indent+d, docstrings))
    return docstrings



@neovim.plugin
class Main(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('Docstring', sync=True)
    def generate_docstring(self):
        # FIXME (himkt): how to get nvim_set_current_line using neovim client
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
            cursor += 1
            if method_string.endswith('):'):
                break

        docstrings = analyze_method(method_string)
        self.nvim.current.buffer.append(docstrings, current_line_number+cursor)
