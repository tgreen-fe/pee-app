import http.client
import json

filmTitle = "departed"

conn = http.client.HTTPSConnection("api.opensubtitles.com")

headers = {
    'Content-Type': "application/json",
    'Api-Key': "YOUR_OPENSUBTITLES_API_KEY"
    }

conn.request("GET", "/api/v1/subtitles?query=departed", headers=headers)

res = conn.getresponse()
data = res.read()

jsonData = json.loads(data)

#print(res)
#print(data)
#print(jsonData)
print(jsonData['data'][0]['attributes']['files'][0]['file_id'])
