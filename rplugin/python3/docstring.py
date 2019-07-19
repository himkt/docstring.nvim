"""Docstring.nvim"""
import re
from os import getenv
from typing import List

import neovim

LOOP_LIMIT = int(getenv("LOOP_LIMIT", "1000"))
TABSTOP = int(getenv("INDENT", "4"))  # NOQA


def add_indent(strings: List[str], tabstop: int):
    """
    Add indents for strings

    Parameters
    ---
    strings: List[str]
        input strings
    tabstop: int
        size of indent
    """
    res = []
    for string in strings:
        if string:
            res.append(" " * tabstop + string)
        else:
            res.append(string)
    return res


def generate_arguments(arguments_string: str):
    """
    Create part of docstring for arguments

    Parameters
    ---
    arguments_string (str)
        string which contains arguments information
    """
    res = []
    argument_strings = arguments_string.split(",")

    for index, argument_string in enumerate(argument_strings):
        if not arguments_string:
            continue

        elem = argument_string.split(":")
        if len(elem) == 2:
            argument, type_string = elem
            type_string = type_string.strip(' ')
        else:
            argument, = elem
            type_string = f"<`{index}:type`>"

        argument = argument.strip(' ')
        if argument == 'self':
            continue

        res.append(f"{argument} ({type_string})")
        res.append(" " * TABSTOP + f"<`{index}:desc`>")

    if res:
        # headings
        res = ["", "Parameters", "---"] + res
    return res


def generate_return(return_string: str):
    """
    Create part of docstring for return value

    Parameters
    ---
    return_string: str
        return annotation
    """
    res = ["", "Result", "---"]
    res.append(return_string.strip())
    return res


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
    indent = TABSTOP

    indent_result = re.search(r"^\s+", method_string)
    if indent_result:
        indent += len(indent_result.group(0))

    method_string = re.sub(r"def\s+", "", method_string)
    method_string = re.sub(r"\s*\:\s*$", "", method_string)

    docstrings = ['"""', "<`0:desc`>"]

    arguments_search_result = re.search(r"\((.*)\)", method_string)
    arguments_string = arguments_search_result.group(1)
    arguments_string = arguments_string.replace(" ", "")
    docstrings += generate_arguments(arguments_string)

    return_search_result = re.search(r"->(.*)", method_string)
    if return_search_result:
        return_string = return_search_result.group(1)
        docstrings += generate_return(return_string)

    docstrings += ['"""']
    docstrings = add_indent(docstrings, indent)
    return docstrings


@neovim.plugin
class Main(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command("Docstring", sync=True)
    def generate_docstring(self):
        # FIXME (himkt): how to get nvim_set_current_line using neovim client
        command = 'echo line(".")'  # FIXME: couldn't find suitable neovim API
        current_line_number = self.nvim.command_output(command)  # FIXME
        current_line_number = int(current_line_number) - 1
        current_line = self.nvim.current.line

        if 'def' not in current_line:
            return

        method_string = ""
        for cursor in range(LOOP_LIMIT):
            method_string += self.nvim.current.buffer[
                current_line_number + cursor
            ]  # NOQA
            if method_string.endswith(":"):
                break

            # if it reaches the limit
            if cursor == LOOP_LIMIT - 1:
                return

        docstrings = analyze_method(method_string)
        self.nvim.current.buffer.append(
            docstrings, current_line_number + cursor + 1
        )  # NOQA
