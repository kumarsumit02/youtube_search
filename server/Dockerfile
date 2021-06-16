FROM python:3.8-slim

LABEL summary="Base Python-Django container" \
    name="gale-python-django" \
    version="1.0" \
    maintainer="Gale" \
    build="docker build -t gale-python-django:1.0 ."

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV HOME /root
ENV APP_HOME /application/server
ENV C_FORCE_ROOT=true
ENV PYTHONUNBUFFERED 1

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

CMD ["/bin/bash"]

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

RUN set -ex \
    && buildDeps=' \
    libpq-dev \
    python3-dev' \
    && apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends \
    $buildDeps \
    build-essential \
    gcc \
    vim \
    python-psycopg2


# Add working dir
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Install pip packages
ADD requirements.txt $APP_HOME
RUN pip install -r requirements.txt


# Copy code into Image
ADD . $APP_HOME

EXPOSE 8000

WORKDIR ${APP_HOME}
