FROM python:3.10-slim

WORKDIR /code

ADD ./containers/requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scripts/data_pipeline.py"] 