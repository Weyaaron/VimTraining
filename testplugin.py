import pynvim
from pynvim import Nvim


@pynvim.plugin
class TestPlugin(object):

    def __init__(self, nvim:Nvim):
        self.nvim = nvim

    @pynvim.function('TestFunction', sync=True)
    def testfunction(self, args):
        self.nvim.out_write("5")
        return 5

    @pynvim.command('TestCommand', nargs='*', range='')
    def testcommand(self, args, range):
        self.nvim.current.line = ('Command with args: {}, range: {}'
                                  .format(args, range))

    @pynvim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")', sync=True)
    def on_bufenter(self, filename):
        #result = self.nvim.api.strwidth("some text")

        #self.nvim.out_write(str(result))

        print("5")
        length = self.nvim.request("nvim_buf_line_count", self.nvim.current.buffer)
        with open("/tmp/log.txt", 'a') as file:
            file.write(str(length))
        self.nvim.out_write('testplugin is in ' + filename + '\n')

    @pynvim.autocmd('TextChanged', pattern='*.py', eval='expand("<afile>")', sync=True)
    def on_change(self, filename):
        with open("/tmp/log.txt", 'a') as file:
            file.write("Text changed \n\n")
        self.nvim.out_write('testplugin is in ' + filename + '\n')

    @pynvim.autocmd('TextChangedI', pattern='*.py', eval='expand("<afile>")', sync=True)
    def on_change_i(self, filename):
        with open("/tmp/log.txt", 'a') as file:
            file.write("Text changed with i\n")
