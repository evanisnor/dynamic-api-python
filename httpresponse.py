import gzip, re, io, json

class HTTPResponse:
    def __init__(self, request, code, headers={}, content=None, http_protocol_version = '1.1'):
        self.http_protocol_version = http_protocol_version
        self.request = request
        self.code = HTTPStatusCode.from_code(code) if isinstance(code, int) else code
        self.headers = headers
        self.content = content

        if 'Accept-Charset' in self.request.headers.keys():
            self.charset = self.request.headers['Accept-Charset'].split(',')[0]
        else:
            self.charset = 'utf-8'

    def compose(self):
        content = json.dumps(self.content).encode(self.charset) if self.content else None

        if content and 'Accept-Encoding' in self.request.headers.keys() and 'gzip' in self.request.headers['Accept-Encoding'].split(','):
            self.headers['Content-Encoding'] = 'gzip'
            content = gzip.compress(content)
        
        self.headers['Content-Length'] = len(content) if content else 0
        head = 'HTTP/{} {} {}\r\n{}\r\n\r\n'.format(
            self.http_protocol_version, \
            self.code[0], \
            self.code[1], \
            '\r\n'.join('{}: {}'.format(key, val) for (key, val) in self.headers.items()))
        return head.encode(self.charset) + content if content else head.encode(self.charset)

    def send(self, auto_close=True):
        self.request.write(self.compose())
        if auto_close:
            self.request.finish()


class HTTPStatusCode:
    Continue = (100, 'Continue')
    SwitchingProtocols = (101, 'Switching Protocols')
    Checkpoint = (103, 'Checkpoint')
    OK = (200, 'OK')
    Created = (201, 'Created')
    Accepted = (202, 'Accepted')
    NonAuthoritativeInformation = (203, 'Non-Authoritative Information')
    NoContent = (204, 'No Content')
    ResetContent = (205, 'Reset Content')
    PartialContent = (206, 'Partial Content')
    MultipleChoices = (300, 'Multiple Choices')
    MovedPermanently = (301, 'Moved Permanently')
    Found = (302, 'Found')
    SeeOther = (303, 'See Other')
    NotModified = (304, 'Not Modified')
    SwitchProxy = (306, 'Switch Proxy')
    TemporaryRedirect = (307, 'Temporary Redirect')
    ResumeIncomplete = (308, 'Resume Incomplete')
    Unauthorized = (401, 'Unauthorized')
    PaymentRequired = (402, 'Payment Required')
    Forbidden = (403, 'Forbidden')
    NotFound = (404, 'Not Found')
    MethodNotAllowed = (405, 'Method Not Allowed')
    NotAcceptable = (406, 'Not Acceptable')
    ProxyAuthenticationRequired = (407, 'Proxy Authentication Required')
    RequestTimeout = (408, 'Request Timeout')
    Conflict = (409, 'Conflict')
    Gone = (410, 'Gone')
    LengthRequired = (411, 'Length Required')
    PreconditionFailed = (412, 'Precondition Failed')
    RequestEntityTooLarge = (413, 'Request Entity Too Large')
    RequestURITooLong = (414, 'Request-URI Too Long')
    UnsupportedMediaType = (415, 'Unsupported Media Type')
    ExpectationFailed = (417, 'Expectation Failed')
    NotImplemented = (501, 'Not Implemented')
    BadGateway = (502, 'Bad Gateway')
    ServiceUnavailable = (503, 'Service Unavailable')
    GatewayTimeout = (504, 'Gateway Timeout')
    HTTPVersionNotSupported = (505, 'HTTP Version Not Supported')
    NetworkAuthenticationRequired = (511, 'Network Authentication Required')

    @classmethod
    def from_code(cls, code):
        for attr in dir(cls):
            if getattr(cls, attr)[0] == code:
                return getattr(cls, attr)