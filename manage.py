#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from trainerai.env_configuration import env

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trainerai.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # this is to run the server from the dotenv
    if len(sys.argv) == 1 and sys.argv[1] == "runserver":
        url = env("URL")
        port = env("PORT")
        sys.argv.append(f'{url}:{port}')

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
