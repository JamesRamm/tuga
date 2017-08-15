# Tuga Specification

TuGa - TUflow and anuGA.

TuGa is a command line client for [Tucluster](https://github.com/JamesRamm/tucluster) - cloud based distributed flood modelling using ANUGA hydro and/or Tuflow.

.. note::
  TuGa is undergoing *heavy* redevelopment with focus on creating a client library.

## Proposed API
Tuga is currently a command line client, which is fairly clunky to use. We plan to redevelop tuga, refocussing on a clean, simple API for interacting with tucluster from python.
The skeleton of the proposed API is below


```
class Model

    def __init__(self, name, datapath=None, description=None, email=None):
        '''Create a new TuGa model. A model has a name and a data folder.

        This folder will be uploaded to TuCluster.
        '''

    @classmethod
    def find(cls, name):
        '''Find an existing ``Model`` with the given name
        '''

    @staticmethod
    def all():
        '''Returns the names of all existing ``Model`` objects
        '''

    def add_data(self, path):
        '''Add new data to the model. ``path`` can be a file or folder.
        '''

    def create_run(self, script):
        '''Create a new model run. This will queue the given script
        for processing on the tucluster cloud.

        Returns a ``Run`` object
        '''

    def get_runs(self):
        '''Return a list of any runs associated with this model
        '''

class Run

    def status(self):
        '''Get the status of the model run task
        '''

    def download_results(self):
        '''Download the results of the model run, if available
        '''

    def download_log(self):
        '''Download any log files associated with the run, if available.
        '''
```





## Data Model
Understanding the data model that is used by Tucluster on the remote server is useful for understanding how Tuga works and
how it differs from just running TuFlow/Anuga directly. Happily, the data model is very simple.

There are 2 concepts - a `Model` and a `ModelRun`. Broadly, a ``Model`` represents a geographical domain over which we will
produce one or more flood models (a Model Run).
A model has a name, description and a folder where input data files are stored.

A Model Run represents an actual flood modelling task, performed by Anuga or Tuflow. It has an entry point which is either the anuga python script or tuflow control file which defines the flood model, and a results folder.
Flood modelling tasks are added to a queue and farmed out to one of the computers in the cluster by tucluster. Exactly when the task is run depends on how many other models are ahead of you in the queue.

Below are the command line arguments we plan to support.


### `tuga create <name>`
  Create a new Model

Arguments:
* `name`: The name to give to the model.

Options:
* `--data <data.zip>` Initialize the model with input data extracted from the given zip archive
* `--description <description>` The model description
* `--email <email>` Email contact for the model owner

<hr>

### `tuga update <name>`
  Update a model

Arguments:
* `name`: The name of the model.

Options:

* `--data <file.ext>` New data/scripts to add to the model
* `--description <description>` New description for the model
* `--name <name>` New name for the model
* `--email <email>` New email contact for the model

<hr>

### `tuga anuga <name>`
  Run Anuga for a script in a previously created model.

Arguments:
* `name`: The name of the model.

Options:

* `--script <name>` Script name (previously uploaded)
* `--notify` Email updates
* `--watch` Stream output directly to the command line

<hr>

### `tuga tuflow <name>`
  Run Tuflow for a script in a previously created model.

Options:

* `--script <name>` Control file name
* `--notify` Email updates
* `--watch` Stream output directly to the command line

<hr>

### `tuga results`
  View all results. Will return a description of all Model Runs.

Options:
* `--model <name>` Limit to results for a specific model
* `--script <name>` Show a single result for a specific control file (only possible if `--model` also specified)
* `--download` Download all available result files.
* `--tree` Also output a representation of the result folder tree. This description will show file identifiers for each file which can be used to download specific files.

<hr>

### `tuga file <fid>`
   Download a specific file, given by its file identifier - `fid`.



