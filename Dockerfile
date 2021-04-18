FROM python:3.7-buster
ADD dist /tmp/tvscraper-dist
RUN pip install /tmp/tvscraper-dist/*.whl
ENTRYPOINT ["python3", "-m", "tvscraper"]