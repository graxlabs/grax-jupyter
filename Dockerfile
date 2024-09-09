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

# Install Python packages in the virtual environment
RUN pip install --upgrade pip && \
    pip install jupyterhub notebook oauthenticator pandas scipy matplotlib && \
    pip install "dask[distributed,dataframe]" dask_labextension && \
    pip install --upgrade jupyterlab jupyterlab-git && \
    jupyter lab build

# Add user admin
RUN useradd admin && echo admin:change.it! | chpasswd && mkdir /home/admin && chown admin:admin /home/admin

# Add Python supporting scripts
ADD jupyterhub_config.py /app/analysis/jupyterhub_config.py
ADD create-user.py /app/analysis/create-user.py

EXPOSE $PORT

CMD ["jupyterhub", "--ip", "0.0.0.0", "--port", "$PORT", "--no-ssl"]