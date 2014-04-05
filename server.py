import logging
import tornado.httpserver
import tornado.ioloop

class Server:
    def __init__(self, server_settings, handler):
        self.settings = server_settings
        self.handler = handler

    def start(self):
        self.http_server = tornado.httpserver.HTTPServer(self.handler.handle)

        logging.info('{} instances, listening on...'.format(len(self.settings.ports)))
        for name in self.settings.listen:
            for port in self.settings.ports:
                self.http_server.bind(port, address=name)
                logging.info('{}:{}'.format(name, port))
        
        self.http_server.start(0)
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        self.http_server.stop()
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('Server has been shut down.')