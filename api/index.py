"""Vercel Python serverless entrypoint for /api/* routes."""
from api.app import create_app

app = create_app()
