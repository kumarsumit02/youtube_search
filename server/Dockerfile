FROM python:3.8-slim

ENV APP_HOME /application/server
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils libpq-dev python3-dev gcc

# Add working dir
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Install pip packages
ADD requirements.txt $APP_HOME
RUN pip install -r requirements.txt

# Copy code into Image
ADD . $APP_HOME

WORKDIR ${APP_HOME}
