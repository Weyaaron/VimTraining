import sys
from pathlib import Path
from random import randrange
from typing import List

import pynvim
from pynvim import Nvim

from loguru import logger

#from src.classes.basetask import BaseTask

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

    @pynvim.autocmd("BufEnter", pattern="*.movement",  sync=True)
    def buf_enter(self):
        self.current_task.buf_enter()

    @pynvim.autocmd(
        "CursorMoved", pattern="*.movement", sync=True
    )
    def cursor_moved(self):
        self.current_task.cursor_moved()



class BaseTask:

    def __init__(self):
        pass

    def setup(self):
        pass

    def isDone(self):
        pass

    def tearDown(self):
        pass


    def buf_enter(self):
        pass


    def cursor_moved(self):
        logger.info("Cursor Moved class")
