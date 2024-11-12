# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.209.6/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3.10"
FROM --platform=linux/amd64 mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi


# [Optional] Uncomment this section to install additional OS packages.
ENV DEBIAN_FRONTEND=noninteractive

# install networking tools
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends net-tools iputils-ping curl htop tree 
#krb5-user libpam-krb5

# mssql obdc client
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends unixodbc unixodbc-dev \
   # Install ms sql server driver
   && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
   && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
   && apt-get update \
   && ACCEPT_EULA=Y apt-get -y install msodbcsql17 \
   #
   # Clean up
   && apt-get autoremove -y \
   && apt-get clean -y \
   && rm -rf /var/lib/apt/lists/*

# put krb5.conf in place
COPY krb5.conf /etc/

# Install Oracle ODBC client 21.3 - The latest avialable on 2021-11-02.  Just in case 18.5 isn't modern enough
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends alien libaio1 wget g++ && \
    sudo wget https://download.oracle.com/otn_software/linux/instantclient/213000/oracle-instantclient-basiclite-21.3.0.0.0-1.el8.x86_64.rpm && \
    sudo wget https://download.oracle.com/otn_software/linux/instantclient/213000/oracle-instantclient-devel-21.3.0.0.0-1.x86_64.rpm && \
    sudo alien -i oracle-instantclient-basiclite-21.3.0.0.0-1.el8.x86_64.rpm && \
    sudo alien -i oracle-instantclient-devel-21.3.0.0.0-1.x86_64.rpm
ENV LD_LIBRARY_PATH="/usr/lib/oracle/21.3/client64/lib:${LD_LIBRARY_PATH}"
ENV DEBIAN_FRONTEND=dialog

# move tns names file
# sudo mkdir -p /opt/oracle/ && sudo cp tnsnames.ora /opt/oracle
COPY tnsnames.ora /opt/oracle/
ENV TNS_ADMIN="/opt/oracle/"
RUN sudo chmod 644 /opt/oracle/tnsnames.ora

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
RUN pip3 install --upgrade pip
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp


# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1
