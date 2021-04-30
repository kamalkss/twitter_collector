FROM python:alpine3.9
COPY . /app
WORKDIR /app
RUN pip install twython
RUN pip install pymongo
RUN pip install Flask
CMD python ./app.py