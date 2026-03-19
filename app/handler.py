"""
Mangum handler — wraps the FastAPI application for AWS Lambda + API Gateway.
This is the Lambda entry point referenced in the Dockerfile CMD.
"""

from mangum import Mangum
from app.main import app

handler = Mangum(app, lifespan="auto")
