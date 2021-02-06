from pathlib import Path

import pynvim
from pynvim import Nvim


def load_def_buffer() -> str:

    abs_file_path = Path("/home/aaron/Code/Python/VimTraining/default_buffer.txt")

    with open(abs_file_path, "r") as file:
        result = file.read()

    return result

    pass


@pynvim.plugin
class TestPlugin(object):
    def __init__(self, nvim: Nvim):
        self.nvim = nvim
        self.default_buffer = load_def_buffer()
        pass

    @pynvim.autocmd("BufEnter", pattern="*.py", eval='expand("<afile>")', sync=True)
    def on_bufenter(self, filename):
        pass

    @pynvim.autocmd("TextChanged", pattern="*.py", eval='expand("<afile>")', sync=True)
    def on_change(self, filename):

        str_list = ["halloss", "tschüss"]
        self.nvim.api.buf_set_lines(0, 0, 3, False, str_list)

        with open("/tmp/log.txt", "a") as file:
            file.write("Text changed \n\n")
        self.nvim.out_write("testplugin is in " + filename + "\n")

    @pynvim.autocmd("TextChangedI", pattern="*.py", eval='expand("<afile>")', sync=True)
    def on_change_i(self, filename):

        buffer_list = [str(el) for el in self.default_buffer]

        def map_white_space(el: str) -> str:
            if el == "\n":
                return ""
            return el

        white_spaced_list = list(map(map_white_space, buffer_list))
        self.nvim.api.buf_set_lines(
            0, 0, len(white_spaced_list), False, white_spaced_list
        )


if __name__ == "__main__":
    test_obj = TestPlugin(None)
