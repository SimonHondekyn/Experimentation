import random
import string
import argparse
import requests
import time
from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser(description="Automate Brute Force Tests on DVWA")
    parser.add_argument('base_url', type=str, help="Base URL of the DVWA application (e.g., http://localhost)")
    return parser.parse_args()

def generate_random_string(length=50):
    """Generates a random string of uppercase letters and digits."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def initialize_session(base_url):
    """Initializes a session and extracts PHPSESSID & security cookies."""
    session = requests.Session()
    url = f"{base_url}/dv/login.php"
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    user_token_input = soup.find("input", {"name": "user_token"})
    user_token = user_token_input["value"] if user_token_input else "unknown_token"
    php_sessid = session.cookies.get("PHPSESSID", "unknown_session")
    security_level = session.cookies.get("security", "low")
    session.close()
    print(f"Initialized session with PHPSESSID={php_sessid}, security={security_level} and user_token={user_token}")
    return php_sessid, security_level, user_token

def send_bruteforce_request(base_url, session, user_token):
    """Sends a single bruteforce payload using an existing session."""
    url = f"{base_url}/dv/login.php"
    password = generate_random_string()
    payload = {
        "username": "admin",
        "password": password,
        "Login": "Login",
        "user_token": user_token
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": f"{base_url}/dv/login.php",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": str(len(payload)),
        "Cookie": f"security={session.cookies.get("security")}; PHPSESSID={session.cookies.get("PHPSESSID")}",
        "Connection": "keep-alive"
    }
    session.post(url, data=payload, headers=headers)

def send_benign_request(base_url, session):
    """Sends benign request to the DVWA application."""
    url = f"{base_url}/dv/vulnerabilities/xss_r/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": f"security={session.cookies.get("security")}; security={session.cookies.get("security")}; PHPSESSID={session.cookies.get("PHPSESSID")}",
        "Connection": "keep-alive"
    }
    session.get(url, headers=headers)

def test_bruteforce(base_url):
    """Runs bruteforce payloads in sequence using a persistent session."""
    php_sessid, security_level, user_token = initialize_session(base_url)
    session = requests.Session()
    session.cookies.set("PHPSESSID", php_sessid)
    session.cookies.set("security", security_level)
    for i in range(1817):
        print(f"Sending bruteforce payload...")
        send_bruteforce_request(base_url, session, user_token)
        time.sleep(1)
        send_benign_request(base_url, session)
        time.sleep(0.25)

def main():
    args = parse_args()
    base_url = args.base_url
    test_bruteforce(base_url)

if __name__ == "__main__":
    main()