FROM python:3.13-slim-bullseye


RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  default-libmysqlclient-dev \
  pkg-config \
  && pip install --no-cache-dir --upgrade pip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY ./requirements.txt /app
# RUN pip install --no-cache-dir --requirement /app/requirements.txt
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "main.py"]
