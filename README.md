# Tuga Specification

TuGa - TUflow and anuGA.

TuGa is a command line client for Tucluster - cloud based distributed flood modelling using ANUGA hydro and/or Tuflow. 

## Data Model
Understanding the data model that is used by Tucluster on the remote server is useful for understanding how Tuga works and 
how it differs from just running TuFlow/Anuga directly. Happily, the data model is very simple. 

There are 2 concepts - a `Model` and a `ModelRun`. A Model is a 

Below are the command line arguments we hope to support.


### `tuga create <name>`
  Create a new Model
  
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
    
  
  

