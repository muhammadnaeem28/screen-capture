FROM registry.hallmarklabs.com/devops/images/python:3.8-alpine3.14

WORKDIR /app
ADD requirements.txt /app

# Install bash in the image for the entrypoint script
RUN apk add --no-cache --upgrade bash

# Install chromium in the image for the entrypoint script
RUN apk add --no-cache chromium chromium-chromedriver
ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_PATH=/usr/lib/chromium/

# Add some extra dependencies for the cryptography package
RUN apk add --no-cache gcc libressl-dev musl-dev libffi-dev openssl-dev

# Install python dependencies to run the tests
RUN pip3 install -r requirements.txt

# Install the awscli for the entrypoint script
RUN pip3 install awscli

# Install the webdriver-manager for the entrypoint script
RUN pip3 install webdriver-manager

# Install jq for the entrypoint script
RUN apk add --no-cache jq

# Add all sources files to the /app dir in the container
ADD . /app

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["pytest"]
