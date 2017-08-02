import zipfile
import os
import json
import requests

def read_in_chunks(file_object, chunksize=4096, callback=None):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunksize)
        if callback:
            callback(file_object.tell())
        if not data:
            break
        yield data


class TuclusterClient:
    '''Programmatic client interface to TuCluster
    '''
    def __init__(self, host):
        self._host = host

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

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

        # Raise an error if it occurred
        post_result.raise_for_status()
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
        result = requests.post(
            "{}/models".format(self._host),
            headers=headers,
            data=data
        )

        result.raise_for_status()
        return result


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
        result = requests.patch(
            "{}/models/{}".format(self._host, name),
            headers=headers,
            data=json.dumps(data)
        )

        result.raise_for_status()
        return result

    def add_model_file(self, name, path, progress_fn=None):
        '''Upload a file to an existing model
        '''
        headers = {
            'content-disposition': 'attachment; filename="{}"'.format(os.path.basename(path)),
            'content-type': 'application/octet-stream'
        }
        with open(path, 'rb') as stream:
            result = requests.patch(
                "{}/models/{}".format(self._host, name),
                headers=headers,
                data=read_in_chunks(stream, callback=progress_fn)
            )

        result.raise_for_status()
        return result

    def create_run(self, name, script=None, notify=False, watch=False, engine='anuga'):
        '''Create a ModelRun using ``engine`` as the modelling engine
        '''
        data = {
            'engine': engine,
            'modelName': name,
            'entrypoint': script
        }

        if not script:
            # Get the model to loop through the entry points
            model = self.get_model(name)
            entrypoints = model['entry_points']
        else:
            entrypoints = [script]

        results = []
        for entrypoint in entrypoints:
            data['entrypoint'] = entrypoint
            result = requests.post(
                '{}/runs'.format(self._host),
                data=json.dumps(data)
            )
            results.append(result)

        return results


    def get_model(self, name, tree=False):
        response = requests.get('{}/models/{}'.format(self._host, name))
        response.raise_for_status()
        model = response.json()
        if tree:
            response = requests.get('{}/files/tree/{}'.format(self._host, model['folder']))
            response.raise_for_status()
            file_tree = response.json()
            model['folder'] = file_tree

        return model

    def get_models(self):
        response = requests.get('{}/models'.format(self._host))
        response.raise_for_status()
        return response.json()


    def get_results(self, task=None, model=None, script=None):
        if task:
            response = requests.get('{}/tasks/{}'.format(self._host, task))
            response.raise_for_status()
            task = response.json()
            return task

        params = {}
        if model:
            params['model'] = model
        if script:
            params['entrypoint'] = script

        # Retrieve the ModelRun
        response = requests.get('{}/runs'.format(self._host), params=params)
        response.raise_for_status()
        run = response.json()

        if len(run) == 1:
            run = run[0]
            task_id = run.pop('task_id', None)
            if task_id:
                response = requests.get('{}/tasks/{}'.format(self._host, task_id))
                response.raise_for_status()
                task = response.json()
                run['task_status'] = task

        return run

    def file(self, fid):
        pass
