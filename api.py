import sys
import requests
import certifi
from pytrends.request import TrendReq

# Proxy configuration
proxy_url = "brd.superproxy.io:33335"
proxy_user = "brd-customer-hl_2b81b19b-zone-residential_proxy1"
proxy_password = "u2d1jngl6jk3"

# Create a properly configured session with verification
session = requests.Session()
session.proxies = {
    'http': f"http://{proxy_user}:{proxy_password}@{proxy_url}",
    'https': f"http://{proxy_user}:{proxy_password}@{proxy_url}"
}
session.verify = certifi.where()  # Use certifi's trusted certificates

# Initialize pytrends with the custom session
pytrends = TrendReq(
    hl='en-US',
    tz=360,
    timeout=(10, 25),
    retries=2,
    backoff_factor=0.1,
    requests_args={'verify': certifi.where()},  # Properly verify HTTPS requests
)

# Build payload and fetch data
kw_list = [sys.argv[1]]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
data = pytrends.interest_over_time()
print(data)