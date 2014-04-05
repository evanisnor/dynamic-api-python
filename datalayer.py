import re

def is_registered_customer(customer_id):
    return customer_id in customers.keys()

def __get_collection(customer_id, path, method):
    resources = customers[customer_id]['resources']
    for r in resources.keys():
        resource = resources[r]
        if re.match(resource['uri'], path) and resource['method'] == method:
            col = resource['data_model']['collection']
            return customer_data[col], resource

def get_data(customer_id, path):
    collection, resource = __get_collection(customer_id, path, "GET")
    if collection:
        return collection

    raise UnknownRouteError()

def insert_data(customer_id, path, data):
    collection, resource = __get_collection(customer_id, path, "POST")
    if collection and resource:
        key = resource['data_model']['key']
        data[key] = len(collection)
        collection.append(data)
        return data[key]

    raise UnknownRouteError()

def update_data(customer_id, path, data):
    collection, resource = __get_collection(customer_id, path, "PUT")
    if collection and resource:
        key = resource['data_model']['key']
        data_id = __get_id_from_path(resource, key, path)
        if not data_id:
            raise UnknownRouteError()

        for i in range(0, len(collection)):
            item = collection[i]
            if str(item[key]) == str(data_id):
                collection[i].update(data.items())
                collection[i][key] = data_id # Just to be sure
                return

    raise UnknownRouteError()

def delete_data(customer_id, path):
    collection, resource = __get_collection(customer_id, path, "DELETE")
    if collection and resource:
        key = resource['data_model']['key']
        data_id = __get_id_from_path(resource, key, path)
        if not data_id:
            raise UnknownRouteError()

        for i in range(0, len(collection)):
            item = collection[i]
            if str(item[key]) == str(data_id):
                del collection[i]
                return

def __get_id_from_path(resource, key, path):
    for groupid in resource['data_model']['groups'].keys():
        value = resource['data_model']['groups'][groupid]
        if value == key:
            return re.match(resource['uri'], path).group(groupid)


class UnknownRouteError(BaseException):
    pass

####################
# Fake database.
####################
customers = {}
customer_data = {}


customers['megapong'] = {}
customers['megapong']['resources'] = {
    0 : {
        'uri' : 'leaderboard',
        'method' : 'GET',
        'data_model' : {
            'collection' : '09723603846',
            'key' : '_id',
            'groups' : {}
        }

    },
    1 : {
        'uri' : 'highscore',
        'method' : 'POST',
        'data_model' : {
            'collection' : '09723603846',
            'key' : '_id',
            'groups' : {}
        }
    },
    2 : {
        'uri' : 'highscore/(\d+)',
        'method' : 'PUT',
        'data_model' : {
            'collection' : '09723603846',
            'key' : '_id',
            'groups' : {
                1 : '_id'
            }
        }
    },
    3 : {
        'uri' : 'highscore/(\d+)',
        'method' : 'DELETE',
        'data_model' : {
            'collection' : '09723603846',
            'key' : '_id',
            'groups' : {
                1 : '_id'
            }
        }
    }
}

customer_data['09723603846'] = [
    { '_id' : '0', 'BEN' : 45093 },
    { '_id' : '1',  'GUY' : 44863 },
    { '_id' : '2',  'BEN' : 42944 },
    { '_id' : '3',  'FRD' : 42493 },
    { '_id' : '4',  'BRB' : 35937 },
    { '_id' : '5',  'TED' : 32974 },
    { '_id' : '6',  'TED' : 15353 },
    { '_id' : '7',  'AAA' : 3425 }
]
