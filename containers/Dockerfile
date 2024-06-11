FROM python:3.10-slim

WORKDIR /code

COPY ./ /code/

ADD ./containers/requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

EXPOSE 8081

CMD ["python", "data_pipeline.py"]