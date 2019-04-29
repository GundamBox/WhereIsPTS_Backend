import getpass
import os
import unittest
from string import Template

import click
from flask_alembic import alembic_click
from flask_migrate.cli import db as db_cli

from app import create_app
from app.commom import utils
from tests.v1.api import build_api_test_suite


@click.group()
def cli():
    pass


@click.command()
def run():

    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.run(host="0.0.0.0")


@click.command()
def test():
    suite = build_api_test_suite()
    with open('UnittestTextReport.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)


cli.add_command(run)
cli.add_command(db_cli)
cli.add_command(test)

if __name__ == "__main__":
    cli()
