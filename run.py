import settings, signal, logging, sys

from server import Server
from handler import Handler

class Runner:
    def __init__(self):
        self.server = None
        self.init_logging()
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def init_logging(self):
        if not hasattr(settings, 'Logging'):
            logging.basicConfig(format='[%(threadName)s @ %(asctime)s] %(levelname)s: %(message)s', level='DEBUG')
            return

        logger = logging.getLogger()
        logger.setLevel(settings.Logging.level)
        formatter = logging.Formatter(settings.Logging.format)

        if settings.Logging.output_file:
            fileHandler = logging.FileHandler(settings.Logging.output_file)
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

        if settings.Logging.console_output:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(formatter)
            logger.addHandler(consoleHandler)

    def start(self):
        handler = Handler()
        self.server = Server(settings.ServerSettings, handler)
        try:
            self.server.start()
        except Exception as e:
            logging.error('Caught error: {}'.format(str(e)))
            if self.server:
                self.server.stop()
            sys.exit(1)

    def stop(self, signal, frame):
        if self.server:
            self.server.stop()
            sys.exit(0)
        else:
            logging.warning('Cannot stop server because it isn\'t running.')
            sys.exit(9)


if __name__ == '__main__':
    Runner().start()

