FROM python:3.10-slim 

WORKDIR /code
ENV PYTHONPATH=/code/scripts

COPY ./ /code/

ADD ./containers/requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8081

# Optional health check
HEALTHCHECK CMD ["ping", "-c", "1", "google.com"]

CMD ["python", "scripts/data_pipeline.py"] 