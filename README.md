# Tuga Specification

TuGa - TUflow and anuGA.

TuGa is a command line client for Tucluster - cloud based distributed flood modelling using ANUGA hydro and/or Tuflow. 

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

### `tuga update <name>`
  Update a model

  Options:

* `--data <file.ext>` New data/scripts to add to the model
* `--description <description>` New description for the model
* `--name <name>` New name for the model
* `--email <email>` New email contact for the model
     
### `tuga anuga <name>`
  Run Anuga for a script in a previously created model.

  Options:

* `--script <name>` Script name (previously uploaded)
* `--notify` Email updates 
* `--watch` Stream output directly to the command line

### `tuga tuflow <name>`
  Run Tuflow for a script in a previously created model. 

  Options:

* `--script <name>` Control file name 
* `--notify` Email updates 
* `--watch` Stream output directly to the command line

### `tuga results`
  View all results. Will return a description of all Model Runs.
  
  Options:
* `--model <name>` Limit to results for a specific model
* `--script <name>` Show a single result for a specific control file (only possible if `--model` also specified)
* `--download` Download all available result files. 
* `--tree` Also output a representation of the result folder tree. This description will show file identifiers for each file which can be used to download specific files. 
    
### `tuga file <fid>`
   Download a specific file, given by its file identifier - `fid`.
  
  

