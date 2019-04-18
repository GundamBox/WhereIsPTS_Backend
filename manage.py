import os
import click
from app import create_app
from app.models import db
from app.utils import common


@click.group()
def cli():
    pass


@click.command()
@click.argument('env', type=click.Choice(['dev', 'test', 'staging', 'prod']), default='dev')
def run(env):

    config_path = 'app/settings/{env}.ini'.format(env=env)
    app = create_app(config_path)

    host = app.config['HOST']
    port = int(app.config['PORT'])
    debug = common.str2bool(app.config['DEBUG'])

    db.init_app(app)
    db.create_all(app=app)

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

if __name__ == "__main__":
    cli()
