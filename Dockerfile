FROM python:3.10
# stdder stddin
ENV PYTHONUNBUFFERED=1
# python dont create .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Dockerfile
ENV OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

WORKDIR /bot


RUN apt-get update && apt-get install -y \
    ffmpeg

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /bot/
