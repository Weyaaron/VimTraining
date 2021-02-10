import sys
from pathlib import Path
from random import randrange
from typing import List

import pynvim
from pynvim import Nvim

abs_path = Path("/home/aaron/Code/Python/VimTraining")



from loguru import logger


default_conf = {
    "handlers": [
        {"sink": sys.stdout},
        {"sink": abs_path.joinpath("./default.log")},
    ]
}

logger.configure(**default_conf)


def load_lines_from_txt() -> List[str]:

    abs_file_path = abs_path.joinpath(Path("./buffers/default_buffer.txt")).resolve()
    result = []
    with open(abs_file_path, "r") as file:
        for el in file.readlines():
            result.append(el)
    return result



@pynvim.plugin
class TestPlugin(object):
    def __init__(self, nvim: Nvim):
        self.count = 0
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
        max_lenght = 10
     #   lines = randrange(min_length, max_lenght)
        lines = 10
     #   line_with_x = randrange(0, lines)
        line_with_x = 5
        print(lines, line_with_x)

        for i in range(0, lines):
            if i == line_with_x:
                white_spaced_list.append("x")
            else:
                white_spaced_list.append("")

        self.nvim.api.buf_set_lines(
            0, 0, len(white_spaced_list)-1, False, white_spaced_list
        )

    @pynvim.autocmd(
        "CursorMoved", pattern="*.movement", eval='expand("<afile>")', sync=True
    )
    def cursor_moved(self, filename):

        logger.info(self.nvim.current.line)

        if self.nvim.current.line == "x":
            self.count += 1
        else:
            self.count = 0

        lines = self.nvim.api.buf_get_lines(0,-2,-1, False)
        linecount = self.nvim.api.buf_line_count(0)

        self.nvim.api.buf_set_lines(
            0, linecount-1,  linecount, False, [f"Current Count is {self.count}"]
        )

        logger.info(f"{lines}")




    @pynvim.autocmd(
        "BufEnter", pattern="*.movement", eval='expand("<afile>")', sync=True
    )
    def on_bufenter(self, filename):
        self.nvim.out_write("Hallo")

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
    nvim = pynvim.attach('socket', path="/tmp/nvim.sock")

    test_obj = TestPlugin(nvim)
    test_obj.nvim.command('echo "hello world"')
    while True:
        pass
