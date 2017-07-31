import zipfile
import os
import json
import requests

def read_in_chunks(file_object, chunksize=4096, callback=None):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    size = file_object.seek(0, 2)
    file_object.seek(0)
    while True:
        data = file_object.read(chunksize)
        percent_complete = file_object.tell() / size * 100
        if callback:
            callback(percent_complete)
        if not data:
            break
        yield data


class TuclusterClient:
    '''Programmatic client interface to TuCluster
    '''
    def __init__(self, host):
        self._host = host

    def post_model_zip(self, data, progress_fn=None):
        '''Post a zip file to create a new model
        '''
        # Check the path exists
        if not os.path.exists(data):
            raise FileNotFoundError('{} does not exist'.format(data))
        # Check it is a zipfile
        if not zipfile.is_zipfile(data):
            raise zipfile.BadZipFile('{} is not a zipfile'.format(data))

        # POST the data
        headers = {'content-type': 'application/zip'}
        with open(data, 'rb') as stream:
            post_result = requests.post(
                "{}/models".format(self._host),
                headers=headers,
                data=read_in_chunks(stream, callback=progress_fn)
            )

        return post_result

    def create_empty_model(self, name, description, email):
        data = {}
        if description:
            data['description'] = description

        if email:
            data['email'] = email

        if name:
            data['name'] = name

        headers = {'content-type': 'application/json'}
        return requests.post(
            "{}/models".format(self._host),
            headers=headers,
            data=data
        )


    def update_model(self, name, description=None, new_name=None, email=None):
        ''' Update an existing model
        '''
        data = {}
        if description:
            data['description'] = description

        if email:
            data['email'] = email

        if new_name:
            data['name'] = new_name

        headers = {'content-type': 'application/json'}
        return requests.patch(
            "{}/models/{}".format(self._host, name),
            headers=headers,
            data=data
        )

    def update_model_files(self, name, files=None):
        pass


    def anuga(self, name, script=None, notify=False, watch=False):
        pass


    def tuflow(self, name, script=None, notify=False, watch=False):
        pass


    def model(self, name, tree=False):
        pass


    def results(self, model=None, script=None, download=False, tree=False):
        pass


    def file(self, fid):
        pass

