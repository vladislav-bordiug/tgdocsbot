FROM python:3.12

COPY app/ /app/

WORKDIR /

RUN pip install -r /app/requirements.txt

CMD ["python", "-m", "app.application"]