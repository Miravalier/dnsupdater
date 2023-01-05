FROM python:3.10

ENV TINI_VERSION="v0.19.0"
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

ENV PYTHONUNBUFFERED=1
RUN pip install requests

COPY ./src /app
WORKDIR /app
CMD ["python3", "main.py"]
