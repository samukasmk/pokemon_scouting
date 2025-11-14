"""WSGI entrypoint for uWSGI/Nginx deployments."""
from app import create_app

app = create_app()
