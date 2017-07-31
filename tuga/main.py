import click
from .lib import TuclusterClient

@click.group()
@click.option('--host', default='localhost:8000', help="Host name of the tucluster API")
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, api_host, debug):
    ctx.obj = TuclusterClient(api_host)


@cli.command()
@click.argument('name', type=str)
@click.option('--data', type=click.Path(exists=True), help="Path to zip archive containing input data")
@click.option('--description', '-d', type=str, help="Description of model")
@click.option('--email', '-e', type=str, help="Email address of model owner/contact for notifications")
@click.pass_obj
def create(client, name, data=None, description=None, email=None):
    '''Create a new model
    '''
    if data:
        post_result = client.post_model_zip(data)

    model = post_result.json()
    patch_result = client.update_model(
        model['name'],
        new_name=name,
        description=description,
        email=email
    )


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
    result = client.update_model(name, files, description, new_name, email)


@cli.command()
@click.argument('name', type=str)
@click.option('--script', '-s', type=str)
@click.option('--notify', '-n', type=bool)
@click.option('--watch', '-w', type=bool)
@click.pass_obj
def anuga(client, name, script=None, notify=False, watch=False):
    '''Queue a modelling task to run with Anuga
    '''
    result = client.anuga(name, script, notify, watch)


@cli.command()
@click.argument('name', type=str)
@click.option('--script', '-s', type=str)
@click.option('--notify', '-n', type=bool)
@click.option('--watch', '-w', type=bool)
@click.pass_obj
def tuflow(client, name, script=None, notify=False, watch=False):
    '''Queue a modelling task to run with Tuflow
    '''
    result = client.tuflow(name, script, notify, watch)


@cli.command()
@click.argument('name', type=str)
@click.option('--tree', 't', type=str)
@click.pass_obj
def model(client, name, tree=False):
    '''View a model and its' data tree
    '''
    result = client.model(name, tree)


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
