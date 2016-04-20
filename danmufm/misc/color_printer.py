import logging
logger = logging.getLogger("danmufm")
class ColorPrinter:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_PURPLE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'

    @classmethod
    def red(cls, s):
        logger.info(cls.RED + s + cls.END)
        print(cls.RED + s + cls.END, flush=True)

    @classmethod
    def green(cls, s):
        logger.info(cls.GREEN + s + cls.END)
        print(cls.GREEN + s + cls.END, flush=True)

    @classmethod
    def yellow(cls, s):
        logger.info(cls.YELLOW + s + cls.END)
        print(cls.YELLOW + s + cls.END, flush=True)

    @classmethod
    def lightPurple(cls, s):
        logger.info(cls.LIGHT_PURPLE + s + cls.END)
        print(cls.LIGHT_PURPLE + s + cls.END, flush=True)

    @classmethod
    def purple(cls, s):
        logger.info(cls.PURPLE + s + cls.END)
        print(cls.PURPLE + s + cls.END, flush=True)
