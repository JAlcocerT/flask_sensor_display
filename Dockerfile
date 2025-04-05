FROM python:3.12.4-slim  
#https://hub.docker.com/_/python

LABEL org.opencontainers.image.source https://github.com/JAlcocerT/Streamlit-MultiChat
LABEL maintainer="Jesus Alcocer Tagua"
LABEL org.opencontainers.image.description="Flask Sensor Web App"
LABEL org.opencontainers.image.licenses=GPL-3.0

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . ./

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# Install production dependencies:
RUN pip install -r requirements.txt

EXPOSE 9999

###podman build -t flask_sensor .
#docker build -t flask_sensor .