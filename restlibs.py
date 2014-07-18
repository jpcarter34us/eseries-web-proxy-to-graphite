from pprint import pprint
import time
import json
import contextlib
from configuration import base_url, resources, session

class ArrayInaccessibleException(Exception):
    def __init__(self, message):
        self.message = message

@contextlib.contextmanager
def array_controller(ip1, ip2, wwn=None, retries=10, remove=True):
    addresses = [ip1, ip2]

    postData = {'controllerAddresses' : addresses, 'wwn' : wwn}
    array = generic_post('storage-systems', postData)
    try:
        for i in range(retries):
            array = generic_get('storage-system', array_id=array['id'])
            status = array['status']
            if(status == 'neverContacted'):
                time.sleep(5)
            else:
                break
        if(status == 'neverContacted' or status == 'inaccessible'):
            raise ArrayInaccessibleException("Unable to access array!")
        yield array
    except Exception:
        raise
    finally:
        if(remove):
            generic_delete('storage-system',array_id=array['id'])

def generic_get (object_type, query_string=None, **params):
    """Performs a GET request on the provided object_type

    :param object_type  -- an object type from the resources listing in the configuration file
    :param params       -- keyword arguments (when required) to complete the URL
    :param query_string -- dict that specifies the query string arguments

    Returns: json

    """

    url = base_url + resources[object_type].format(**params)

    req = session.get(url, params=query_string)
    req.raise_for_status()
    try:
        return req.json()
    except ValueError:
        return req.content

def generic_delete (object_type, query_string=None, **params):
    """Performs a DELETE request on the provided object_type

    :param object_type  -- an object type from the resources listing in the configuration file
    :param params       -- keyword arguments (when required) to complete the URL
    :param query_string -- dict that specifies the query string arguments

    RETURNS: Status code for the http request

    """

    url = base_url + resources[object_type].format(**params)
    req = session.delete(url, params=query_string)
    req.raise_for_status()
    return req.status_code

def generic_post (object_type, data, query_string=None, **params):
    """Performs a POST request on the provided object_type

    :param object_type  -- an object type from the resources listing in the configuration file
    :param data         -- parameters provided as a dict to create the object in question
    :param params       -- keyword arguments (when required) to complete the URL
    :param query_string -- dict that specifies the query string arguments

    RETURNS: json

    """

    url = base_url + resources[object_type].format(**params)

    req = session.post(url, data=json.dumps(data), params=query_string)
    req.raise_for_status()
    return req.json()

def main():
    with array_controller('127.0.0.1', None) as array:
        pprint(array)

if __name__ == "__main__":
    main()