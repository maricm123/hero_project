FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /hero
COPY requirements.txt /hero/
RUN pip install -r requirements.txt
COPY . /hero/