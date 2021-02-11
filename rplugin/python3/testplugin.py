import sys
from pathlib import Path
from random import randrange
from typing import List

import pynvim
from pynvim import Nvim

from loguru import logger


# this allows for imports, probably not an elegant solution
# but i dont mind
file_path = Path(__file__).absolute()
root_path = file_path.parent
sys.path.append(str(root_path))


from src.classes.basetask import BaseTask

abs_path = Path(__file__).absolute().parent.parent.parent

default_conf = {
    "handlers": [
        {"sink": sys.stdout},
        {"sink": abs_path.joinpath(Path("./default.log"))},
    ]
}

logger.configure(**default_conf)


@pynvim.plugin
class TestPlugin(object):

    def __init__(self, nvim: Nvim):
        self.count = 0
        self.nvim = nvim
       # self.default_buffer_lines = load_lines_from_txt()
        self.current_task = BaseTask()
        logger.info(f"{sys.path}")

    @pynvim.autocmd("BufEnter", pattern="*.movement",eval='expand("<afile>")',  sync=True)
    def buf_enter(self, filename):
        self.current_task.buf_enter()

    @pynvim.autocmd(
        "CursorMoved", pattern="*.movement", sync=True
    )
    def cursor_moved(self):
        self.current_task.cursor_moved()
