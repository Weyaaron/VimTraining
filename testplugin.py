import sys
from pathlib import Path
from random import randrange
from typing import List

import pynvim
from pynvim import Nvim


from loguru import logger


default_conf = {
    "handlers": [
        {"sink": sys.stdout},
        {"sink": Path("/home/aaron/Code/Python/VimTraining/default.log")},
    ]
}

logger.configure(**default_conf)


def load_lines_from_txt() -> List[str]:

    abs_file_path = Path("/home/aaron/Code/Python/VimTraining/default_buffer.txt")
    result = []
    with open(abs_file_path, "r") as file:
        for el in file.readlines():
            result.append(el)
    return result



@pynvim.plugin
class TestPlugin(object):
    def __init__(self, nvim: Nvim):
        self.nvim = nvim
        self.default_buffer_lines = load_lines_from_txt()
        pass

    def set_buffer(self):
        def map_white_space(el: str) -> str:
            if el == "\n":
                return ""
            return el.strip("\n")

        white_spaced_list = list(map(map_white_space, self.default_buffer_lines))

        min_length = 0
        max_lenght = 20
        lines = randrange(min_length, max_lenght)
        line_with_x = randrange(0, lines)
        print(lines, line_with_x)

        for i in range(0, lines):
            if i == line_with_x:
                white_spaced_list.append("x")
            else:
                white_spaced_list.append("")

        self.nvim.api.buf_set_lines(
            0, 0, len(white_spaced_list), False, white_spaced_list
        )

    @pynvim.autocmd(
        "CursorMoved", pattern="*.movement", eval='expand("<afile>")', sync=True
    )
    def cursor_moved(self, filename):
        if self.nvim.current.line == "x":
            self.nvim.out_write("Hallo")

    @pynvim.autocmd(
        "BufEnter", pattern="*.movement", eval='expand("<afile>")', sync=True
    )
    def on_bufenter(self, filename):
        pass

    @pynvim.autocmd(
        "TextChanged", pattern="*.movement", eval='expand("<afile>")', sync=True
    )
    def on_change(self, filename):
        self.set_buffer()

    @pynvim.autocmd(
        "TextChangedI", pattern="*.movement", eval='expand("<afile>")', sync=True
    )
    def on_change_i(self, filename):
        self.set_buffer()


if __name__ == "__main__":
    test_obj = TestPlugin(None)
    test_obj.set_buffer()
