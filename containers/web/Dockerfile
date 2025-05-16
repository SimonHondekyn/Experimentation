FROM python:3.12-slim
RUN pip install --no-cache-dir requests beautifulsoup4
COPY scripts/sqli.py /
COPY scripts/xss.py /
COPY scripts/bruteforce.py /
COPY scripts/httploic.py /