import os
from string import Template
import getpass
import click
from flask_alembic import alembic_click
from flask_migrate.cli import db as db_cli

from app import create_app
from app.commom import utils


@click.group()
def cli():
    pass


@click.command()
def run():

    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.run()


cli.add_command(run)
cli.add_command(db_cli)

if __name__ == "__main__":
    cli()
