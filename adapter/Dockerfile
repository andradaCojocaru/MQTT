FROM python:3.10

COPY ./adapter/requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

WORKDIR /adapter
COPY ./adapter/adapter.py /adapter

CMD ["python", "adapter.py"]
