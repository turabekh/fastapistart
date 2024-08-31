# Add the parent directory of 'app' to the Python path
import sys
from pathlib import Path

import click
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

sys.path.append(str(Path(__file__).parents[2].resolve()))

from app.core.config import settings
from app.models.base import Base


def get_alembic_config():
    alembic_cfg = Config(str(Path(__file__).parent / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(Path(__file__).parent / "migrations"))
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))
    return alembic_cfg


def get_engine():
    return create_engine(str(settings.DATABASE_URL))


@click.group()
def cli():
    pass


@cli.command()
def init():
    """Initialize Alembic migrations"""
    alembic_cfg = get_alembic_config()
    command.init(alembic_cfg, str(Path(__file__).parent / "migrations"), template="generic")
    click.echo("Alembic migrations initialized")


@cli.command()
@click.option("--message", "-m", required=True, help="Migration message")
def make_migrations(message):
    """Generate a new migration"""
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, autogenerate=True, message=message)


@cli.command()
def migrate():
    """Apply all pending migrations"""
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, "head")


@cli.command()
def create_db():
    """Create the database if it doesn't exist"""
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url)
        click.echo(f"Database created at {engine.url}")
    else:
        click.echo(f"Database already exists at {engine.url}")


@cli.command()
def drop_db():
    """Drop the database"""
    if click.confirm("Are you sure you want to drop the database? This action cannot be undone."):
        engine = get_engine()
        if database_exists(engine.url):
            drop_database(engine.url)
            click.echo(f"Database at {engine.url} has been dropped")
        else:
            click.echo(f"Database at {engine.url} does not exist")


if __name__ == "__main__":
    cli()
