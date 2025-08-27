# 代码生成时间: 2025-08-28 03:43:50
#!/usr/bin/env python

"""
A database migration tool using the Pyramid framework.
This tool is designed to handle database migrations, ensuring that the
database schema is up-to-date with the latest changes in the application.
"""

import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command, script

# Define the path to the migration scripts
MIGRATION_SCRIPTS = os.path.join(os.path.dirname(__file__), 'migrations')


# Configure the Pyramid application
def main(global_config, **settings):
    """
    This function sets up the Pyramid application.
    It creates a Configurator object and configures the necessary components.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')  # Include Jinja2 for template rendering
    config.scan()  # Scan for Pyramid components
    return config.make_wsgi_app()


# Database connection settings
DATABASE_URL = 'sqlite:///migrations.db'  # Example SQLite database URL


# Create the engine and sessionmaker
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# Define the migration script directory
script_directory = MIGRATION_SCRIPTS


# Define the migration views
@view_config(route_name='apply_migration', renderer='json')
def apply_migration(request):
    """
    Apply the database migration.
    This view handles the application of a database migration.
    """
    try:
        # Run the migration
        command.upgrade(script_directory, 'head')
        return {'status': 'success', 'message': 'Migration applied successfully'}
    except Exception as e:
        # Handle any errors that occur during migration
        return {'status': 'error', 'message': str(e)}


@view_config(route_name='downgrade_migration', renderer='json')
def downgrade_migration(request):
    """
    Downgrade the database migration.
    This view handles the downgrade of a database migration.
    """
    try:
        # Run the downgrade
        command.downgrade(script_directory, '-1')
        return {'status': 'success', 'message': 'Migration downgraded successfully'}
    except Exception as e:
        # Handle any errors that occur during downgrade
        return {'status': 'error', 'message': str(e)}


@view_config(route_name='generate_migration', renderer='json')
def generate_migration(request):
    """
    Generate a new database migration script.
    This view handles the generation of a new migration script.
    """
    try:
        # Get the message from the request
        message = request.params.get('message')
        if not message:
            return {'status': 'error', 'message': 'Missing message parameter'}

        # Run the generate command
        command.revision(script_directory, message=message)
        return {'status': 'success', 'message': 'Migration script generated successfully'}
    except Exception as e:
        # Handle any errors that occur during script generation
        return {'status': 'error', 'message': str(e)}

