FROM python:3.9

WORKDIR /cial

COPY requirements.txt config.py run.py ./
COPY app ./app

RUN pip install -r ./requirements.txt

EXPOSE 8000
CMD ["gunicorn", "-b", ":8000", "run:app"]