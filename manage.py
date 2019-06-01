import getpass
import os
import unittest
from string import Template

import click
from flask_alembic import alembic_click
from flask_migrate.cli import db as db_cli

from app import create_app
from tests.v1.api import build_api_test_suite


@click.group()
def cli():
    pass


@click.command()
def run():

    app = create_app(os.getenv('FLASK_ENV') or 'default')
    app.run(host="0.0.0.0")


cli.add_command(run)
cli.add_command(db_cli)

if __name__ == "__main__":
    cli()
