import http.client
import sys

conn = http.client.HTTPSConnection("api.hasdata.com")

headers = {'x-api-key': "d819b3e9-ba95-4c3b-b585-489d6ffdac34"}
conn.request("GET", f"/scrape/google-trends/search?q={sys.argv[1]}&date={sys.argv[2]}%20{sys.argv[3]}&geo={sys.argv[4]}&hl=en-us", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))