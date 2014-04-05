import logging, re, json

from httpresponse import HTTPResponse, HTTPStatusCode
from datalayer import get_data, insert_data, update_data, delete_data, is_registered_customer, UnknownRouteError

class Handler:
    def handle(self, request):
        logging.debug(str(request))
        try:
            customer_id, method, path, body = self.exract_request_params(request)
            logging.debug('{}: {} {}'.format(customer_id, method, path))
        except:
            response = HTTPResponse(request, HTTPStatusCode.NotAcceptable, content={ 'message': 'Incorrect data format' })
            response.send()
            return

        if not is_registered_customer(customer_id):
            response = HTTPResponse(request, HTTPStatusCode.NotFound, content={ 'message': 'Unknown customer ID ' })
        elif method == 'GET':
            try:
                data = get_data(customer_id, path)
                response = HTTPResponse(request, HTTPStatusCode.OK, content=data)
            except UnknownRouteError:
                response = HTTPResponse(request, HTTPStatusCode.NotFound, content={ 'message': 'Resource does not exist' })
        elif method == 'POST':
            try:
                insert_data(customer_id, path, body)
                response = HTTPResponse(request, HTTPStatusCode.OK)
            except UnknownRouteError:
                response = HTTPResponse(request, HTTPStatusCode.NotFound, content={ 'message': 'Resource does not exist' })
        elif method == 'PUT':
            try:
                update_data(customer_id, path, body)
                response = HTTPResponse(request, HTTPStatusCode.OK)
            except UnknownRouteError:
                response = HTTPResponse(request, HTTPStatusCode.NotFound, content={ 'message': 'Resource does not exist' })
        elif method == 'DELETE':
            try:
                delete_data(customer_id, path)
                response = HTTPResponse(request, HTTPStatusCode.OK)
            except UnknownRouteError:
                response = HTTPResponse(request, HTTPStatusCode.NotFound, content={ 'message': 'Resource does not exist' })
        else:
            response = HTTPResponse(request, HTTPStatusCode.MethodNotAllowed, content={ 'message' : 'Unknown method ' + method })
        response.send()

    def exract_request_params(self, request):
        values = re.match('^/~([a-zA-Z0-9]+)/([a-zA-Z0-9/]+)/?', request.uri)
        method = request.method
        customer_id = values.group(1)
        path = values.group(2)
        body = json.loads(request.body.decode('utf-8')) if request.body else None
        return customer_id, method, path, body