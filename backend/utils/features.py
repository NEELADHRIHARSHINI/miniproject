import re
import socket
import whois
import datetime
import tldextract
import ipaddress
import dns.resolver
import requests

# ---------- BASIC URL FEATURES ----------

def url_length(url):
    return len(url)

def count_dots(url):
    return url.count('.')

def has_ip_in_url(url):
    return 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

def uses_https(url):
    return 1 if url.startswith("https") else 0

# ---------- DNS FEATURES ----------

def dns_exists(domain):
    try:
        dns.resolver.resolve(domain, 'A')
        return 1
    except:
        return 0

def dns_ip_count(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return len(answers)
    except:
        return 0

# ---------- DOMAIN AGE ----------

def domain_age(domain):
    try:
        w = whois.whois(domain)
        created = w.creation_date
        if isinstance(created, list):
            created = created[0]
        return (datetime.datetime.now() - created).days
    except:
        return 0

# ---------- ASN FEATURE ----------

def get_asn(ip):
    try:
        res = requests.get(
            f"https://api.iptoasn.com/v1/as/ip/{ip}",
            timeout=5
        )
        return int(res.json().get("as_number", 0))
    except:
        return 0

# ---------- IP REPUTATION ----------

def is_private_ip(ip):
    try:
        return 1 if ipaddress.ip_address(ip).is_private else 0
    except:
        return 1

# ---------- MAIN FEATURE EXTRACTOR ----------

def extract_url_features(url):
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"

    try:
        ip = socket.gethostbyname(domain)
    except:
        ip = "0.0.0.0"

    return [
        url_length(url),
        count_dots(url),
        has_ip_in_url(url),
        uses_https(url),
        dns_exists(domain),
        dns_ip_count(domain),
        domain_age(domain),
        is_private_ip(ip),
        get_asn(ip)
    ]
