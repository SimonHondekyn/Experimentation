# use my kali image
FROM kali:2017.1
# disable interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
# set permissions on tmp directory
RUN mkdir -p /tmp && chmod 1777 /tmp
# add GPG key
RUN curl -fsSL https://archive.kali.org/archive-key.asc | apt-key add -
# fix sources.list
RUN echo "deb http://old.kali.org/kali moto main non-free contrib" > /etc/apt/sources.list
# install the required packages
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*
# use older version of goldeneye
RUN git clone https://github.com/jseidl/GoldenEye.git /opt/goldeneye && \
    cd /opt/goldeneye && git checkout f6faf87
# set workdir
WORKDIR /opt/goldeneye
# set entrypoint
ENTRYPOINT ["python3", "goldeneye.py"]