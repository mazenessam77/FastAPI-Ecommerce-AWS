

FROM public.ecr.aws/lambda/python:3.11

# Copy requirements first for better Docker layer caching
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy application code
COPY app/ ${LAMBDA_TASK_ROOT}/app/
COPY main.py ${LAMBDA_TASK_ROOT}/
COPY alembic/ ${LAMBDA_TASK_ROOT}/alembic/
COPY alembic.ini ${LAMBDA_TASK_ROOT}/
COPY migrate.py ${LAMBDA_TASK_ROOT}/

# The Mangum handler entrypoint
CMD ["app.handler.handler"]
