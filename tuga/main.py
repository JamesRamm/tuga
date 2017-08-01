import click
import os
import json
from .lib import TuclusterClient

@click.group()
@click.option('--host', default='http://localhost:8000', help="Host name of the tucluster API")
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, host, debug):
    ctx.obj = TuclusterClient(host)

@click.command()
@click.argument('host', type=str)
@click.pass_obj
def set_host(client, host):
    '''Change/set the host name from the default (http://localhost:8000)
    '''
    client.host = host
    click.secho('Host URL set to {}'.format(host), fg='green')

@cli.command()
@click.argument('name', type=str)
@click.option('--data', type=click.Path(exists=True), help="Path to zip archive containing input data")
@click.option('--description', '-d', type=str, help="Description of model")
@click.option('--email', '-e', type=str, help="Email address of model owner/contact for notifications")
@click.pass_obj
def create(client, name, data=None, description=None, email=None):
    '''Create a new model
    '''
    try:
        if data:
            # Post the data file then patch the resulting model with
            # the meta data.

            # Get the size of the input file to display progress
            with open(data, 'rb') as fobj:
                size = fobj.seek(0, 2)
            with click.progressbar(length=size, label='Uploading data') as progress:
                post_result = client.post_model_zip(data, progress_fn=progress.update)

            click.secho('Upload successful', fg='green')
            click.secho('Updating metadata...', fg='blue')

            model_dict = post_result.json()
            client.update_model(
                model_dict['name'],
                new_name=name,
                description=description,
                email=email
            )

        else:
            ## Create a new model without any data
            result = client.create_empty_model(name, description, email)

        click.secho('Model {} created!'.format(name), fg='green')
    except Exception as error:
        click.secho(str(error), fg='white', bg='red', bold=True)


@cli.command()
@click.argument('name', type=str)
@click.option('--file', '-f', 'files', type=click.Path(exists=True), multiple=True)
@click.option('--description', '-d', type=str)
@click.option('--name', '-n', 'new_name', type=str)
@click.option('--email', '-e', type=str)
@click.pass_obj
def update(client, name, files=None, description=None, new_name=None, email=None):
    '''Update an existing model
    '''
    if description or new_name or email:
        click.secho('Updating metadata...', fg='blue')
        client.update_model(name, description, new_name, email)

    if files:
        for path in files:
            msg = 'Uploading {}...'.format(os.path.basename(path))
            with open(path, 'rb') as fobj:
                size = fobj.seek(0, 2)
            with click.progressbar(length=size, label=msg) as progress:
                result = client.add_model_file(path, progress_fn=progress.update)

    click.secho('Model {} updated!'.format(name), fg='green')
    if new_name:
        click.secho(
            'The model has been renamed to {}. Use this name for future queries'.format(new_name),
            fg='blue'
        )


def _print_run_results(results):
    for r in results:
        if r.status_code == 201:
            data = r.json()
            msg = 'Run for {} created. Task ID for results is: {}'.format(data['entry_point'], data['task_id'])
            click.secho(msg, fg='green')
        else:
            click.secho('Run creation failed', fg='white', bg='red', bold=True)


@cli.command()
@click.argument('name', type=str)
@click.option('--script', '-s', type=str)
@click.option('--notify', '-n', type=bool)
@click.option('--watch', '-w', type=bool)
@click.pass_obj
def anuga(client, name, script=None, notify=False, watch=False):
    '''Queue a modelling task to run with Anuga
    '''
    results = client.create_run(name, script, notify, watch, 'anuga')
    _print_run_results(results)


@cli.command()
@click.argument('name', type=str)
@click.option('--script', '-s', type=str)
@click.option('--notify', '-n', type=bool)
@click.option('--watch', '-w', type=bool)
@click.pass_obj
def tuflow(client, name, script=None, notify=False, watch=False):
    '''Queue a modelling task to run with Tuflow
    '''
    results = client.create_run(name, script, notify, watch, 'tuflow')
    _print_run_results(results)


@cli.command()
@click.argument('name', type=str)
@click.option('--tree', '-t', type=bool)
@click.pass_obj
def model(client, name, tree=False):
    '''View a model and its' data tree
    '''
    try:
        result = client.get_model(name, tree)
        click.secho('Model Info:')
        click.secho(json.dumps(result, sort_keys=True,
                               indent=4, separators=(',', ': ')))
    except Exception as error:
        click.secho(str(error), fg='white', bg='red', bold=True)

@cli.command()
@click.option('--model', '-m', type=str)
@click.option('--script', '-s', type=str)
@click.option('--download', '-d', type=str)
@click.option('--tree', '-t', type=str)
@click.pass_obj
def results(client, model=None, script=None, download=False, tree=False):
    '''View the results for a model, if available
    '''
    result = client.results(model, script, download, tree)


@cli.command()
@click.argument('fid', type=str)
@click.pass_obj
def file(client, fid):
    '''Download a file by its' FID
    '''
    result = client.file(fid)
