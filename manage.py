import os

import click
from flask_alembic import alembic_click
from flask_migrate.cli import db as db_cli
from app import create_app
from app.utils import common


@click.group()
def cli():
    pass


@click.command()
def run():
    app = create_app()

    host = app.config['HOST']
    port = int(app.config['PORT'])
    debug = app.config['DEBUG']

    app.run(host=host, port=port, debug=debug)


@click.command()
@click.argument('env', type=click.Choice(['dev', 'test', 'staging', 'prod']), default='dev')
def generate_key(env):

    config_path = 'app/settings/{env}.ini'.format(env=env)
    config = common.import_config(config_path)

    config['FLASK']['SECRET_KEY'] = os.urandom(12).hex()

    common.export_config(config, config_path)


cli.add_command(run)
cli.add_command(generate_key)
cli.add_command(db_cli)

if __name__ == "__main__":
    cli()
