import whylabs_client
from whylabs_client import ApiClient, Configuration
from whylabs_client.api.models_api import ModelsApi
from whylabs_client.model.column_schema import ColumnSchema
import click

@click.command()
@click.option('--org_id', '-o', 
        help='Your WhyLabs Organization ID',
        envvar='WHYLABS_DEFAULT_ORG_ID'
)
@click.option('--api_key', '-k',
        help='Your WhyLabs API key',
        envvar='WHYLABS_API_KEY'
)
@click.option('--dataset_id', '-i',
        help='Your WhyLabs Dataset ID',
        envvar='WHYLABS_DEFAULT_DATASET_ID'
)
@click.option('--column_name', '-n',
        help='Name of the column in WhyLabs you want to modify.'
)
@click.option('--classifier', '-c',
        help='The classifier you want this column to be',
        type=click.Choice(['input', 'output'])
)
@click.option('--datatype', '-t',
        help='The dataType you want this column to be',
        type=click.Choice(['integral', 'fractional', 'string'])
)
@click.option('--discreteness', '-d',
        help='The discreteness you want this column to be',
        type=click.Choice(['continuous','discrete'])
)

def update_column_schema(column_name, classifier, datatype, discreteness, org_id, dataset_id, api_key):
    """Gets current schema of a column and updates it to the values passed in."""
    if not org_id or not api_key or not dataset_id:
        ctx = click.get_current_context()
        ctx.fail("no auth set, try again.")
    api = get_whylabs_client()
    current_config = api.get_entity_schema_column(org_id, dataset_id, column_name)
    click.echo("Current schema for {}:\n{}\n".format(column_name, current_config))
    if classifier or datatype or discreteness:
        updated_config = make_updated_schema(current_config, classifier, datatype, discreteness)
        if updated_config == current_config:
            click.echo("nothing to change, exiting.")
            exit()
        else:
            click.echo("Updated schema for {}:\n{}\n".format(column_name, updated_config))
            if click.confirm('Do you want to continue?'):
                column_schema = ColumnSchema(
                        classifier=updated_config['classifier'],
                        data_type=updated_config['dataType'],
                        discreteness=updated_config['discreteness']
                )
                response = api.put_entity_schema_column(org_id, dataset_id, column_name, column_schema)
                click.echo('\ndone!\n')
            else:
                click.echo('ok! exiting.')
                exit()
    else:
        click.echo('no modificiation options defined, leaving as is.')

@click.pass_context
def get_whylabs_client(ctx):
    configuration = Configuration(
        host = "https://api.whylabsapp.com"
    )
    configuration.api_key = {"ApiKeyAuth": ctx.params['api_key']}
    configuration.discard_unknown_keys = True
    client = ApiClient(configuration)
    return ModelsApi(api_client=client)

def make_updated_schema(current, classifier, datatype, discreteness):
    updated_schema = current.copy()
    if classifier:
      updated_schema['classifier'] = classifier
    if datatype:
      updated_schema['dataType'] = datatype
    if discreteness:
      updated_schema['discreteness'] = discreteness
    return updated_schema

if __name__ == '__main__':
    update_column_schema()