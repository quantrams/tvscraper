FROM python:3.7-buster
ADD dist /tmp/alpaca2pg-dist
RUN pip install /tmp/alpaca2pg-dist/*.whl
ENTRYPOINT ["python3", "-m", "alpaca2pg"]