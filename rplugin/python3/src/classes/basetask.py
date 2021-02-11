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


    def buf_enter(self):
        pass


    def cursor_moved(self):
        logger.info("Cursor Moved class")
