import pynvim
import os


@pynvim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    @pynvim.function('DoItPython')
    def doItPython(self, args):
        self.vim.command('echo "hello from DoItPython"')
        nvim = pynvim.attach('socket', os.environ['NVIM_LISTEN_ADDRESS'])
        print(nvim.current.buffer)
