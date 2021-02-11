import pynvim
from loguru import logger


class BaseTask:

    def __init__(self):
        pass

    def setup(self):
        pass

    def isDone(self):
        pass

    def tearDown(self):
        pass

    @pynvim.autocmd(
        "CursorMoved", pattern="*.movement", sync=True
    )
    def cursor_moved(self, filename):
        logger.info("Code run")
