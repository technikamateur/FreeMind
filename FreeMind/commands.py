from FreeMind import app, db
import click

@app.cli.command('initdb')
def initdb():
    """Initialize the database."""
    click.echo('Initializing the Database...')
    db.create_all()
    click.echo('Created the Database...')
