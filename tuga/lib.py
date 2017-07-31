import zipfile
import os
import json
import requests

class TuclusterClient:
    '''Programmatic client interface to TuCluster
    '''
    def __init__(self, host):
        self._host = host

    def post_model_zip(self, data):
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
                data=stream
            )

        return post_result

    def update_model(self, name, file=None, description=None, new_name=None, email=None):
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
        return requests.post(
            "{}/models/{}".format(self._host, name),
            headers=headers,
            data=data
        )


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

