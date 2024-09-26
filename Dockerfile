FROM python:3.10

ENV PYTHONUNBUFFERED 1

ARG AMADEUS_CLIENT_ID
ARG AMADEUS_CLIENT_SECRET
ARG AMADEUS_HOSTNAME

RUN mkdir /code

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt

RUN python amadeus_demo_api/manage.py collectstatic --noinput

ENTRYPOINT ["python", "amadeus_demo_api/manage.py"]

CMD ["runserver", "0.0.0.0:8000"]

EXPOSE 8000
