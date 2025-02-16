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
# install the required packages for ftp_login and ssh_login
RUN apt-get update && apt-get install -y \
    git \
    python-pip \
    && rm -rf /var/lib/apt/lists/*
# install the required dependencies as mentioned in this specific version of patator
RUN pip install \
    paramiko==2.0.0
# use older version of patator
RUN git clone https://github.com/lanjelot/patator.git /opt/patator && \
    cd /opt/patator && git checkout 02783fb
# set workdir
WORKDIR /opt/patator
# use first x lines of some password file
RUN head -n 300 /usr/share/wordlists/metasploit/password.lst > passwords.txt
# set entrypoint
ENTRYPOINT ["python", "patator.py"]