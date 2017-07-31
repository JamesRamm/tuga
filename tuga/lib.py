import requests


class TuclusterClient:

    def __init__(self, host):
        self._host = host

    def create(self, name, data=None, description=None, email=None):
        pass


    def update(self, name, file=None, description=None, new_name=None, email=None):
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
