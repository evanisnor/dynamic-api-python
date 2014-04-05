
class ServerSettings:
    listen = [ '127.0.0.1' ]
    ports = [ 8000, 8001 ]

class DatabaseSettings:
    master_server = 'localhost'

class Logging:
    format = '[%(threadName)s @ %(asctime)s] %(levelname)s: %(message)s'
    level = 'INFO'
    console_output = True
    output_file = None