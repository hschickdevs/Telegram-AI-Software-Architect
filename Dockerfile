# Docker image location:
# https://hub.docker.com/repository/docker/hschickdevs/ai-software-architect/general

# How to install docker engine on Ubuntu:
# https://docs.docker.com/engine/install/ubuntu/ 

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
# Ensure that readme is included for docker hub
COPY README.md /app/README.md

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run the bot when the container launches
CMD ["python3", "-m", "src"]

# ------- Docker Deployment Commands: -------
# docker build -t ai-software-architect .
# docker tag ai-software-architect hschickdevs/ai-software-architect:latest
# docker push hschickdevs/ai-software-architect:latest
# docker rmi -f $(docker images -aq)

# FOR TESTING:
# docker run --env-file .env ai-software-architect

# ------- Docker Pull & Run Commands: -------
# docker pull hschickdevs/ai-software-architect:latest
# docker run -d --name ai-software-architect \
#   -e API_KEY=<YOUR_APIKEY> \
#   -e BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN> \
#   -e MODEL=<LLM-MODEL> \
#   -e MODEL_CODE=<LLM_MODEL_CODE> \
#   hschickdevs/ai-software-architect
# docker attach ai-software-architect