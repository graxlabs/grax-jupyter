FROM ubuntu:latest

ARG port
ENV PORT=$port

WORKDIR /app/analysis

# Update and install system packages
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-full python3-pip python3-venv curl gnupg git

# Install Node.js and configurable-http-proxy
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g configurable-http-proxy

# Create and activate a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD requirements.txt /app/analysis/requirements.txt

# Install Python packages in the virtual environment
RUN pip install --upgrade pip && pip install -r requirements.txt && \
    jupyter lab build

# Add user admin
RUN useradd admin && echo admin:change.it! | chpasswd && mkdir /home/admin && chown admin:admin /home/admin

# Add Python supporting scripts
ADD jupyterhub_config.py /app/analysis/jupyterhub_config.py
ADD create-user.py /app/analysis/create-user.py
ADD grax_athena /app/analysis/grax_athena

RUN pip install ./grax_athena

ENV PYTHONPATH="${PYTHONPATH}:/app/analysis"
ENV AWS_REGION=${AWS_REGION}
ENV AWS_ACCESS_KEY=${AWS_ACCESS_KEY}
ENV AWS_SECRET_KEY=${AWS_SECRET_KEY}
ENV SCHEMA_NAME=${SCHEMA_NAME}
ENV S3_STAGING_DIR=${S3_STAGING_DIR}

EXPOSE $PORT

CMD jupyterhub --ip 0.0.0.0 --port $PORT --no-ssl
