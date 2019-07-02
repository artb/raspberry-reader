from urllib.request import urlopen
import urllib.parse
import urllib.request
import requests

provider = '5d128c2d4a839b002817366a'
reciver = '5d1af4894f62310027c964f7'
url = 'http://192.168.43.86:3333/transactions/transaction/'
value = {'type': 'checkout'}
header = {'Content-Type': 'application/json'}

data = urllib.parse.urlencode(value)
data = data.encode("utf-8")
print(data)
url = url + provider + '/' + reciver
print(url)

puta = requests.post(url,json={'type':'checkout'})
print(puta)
#r = urllib.request.Request(url, data)
#r = urllib.request.urlopen(r) #I added this
#content = r.read().decode()
#print(content)

#req = urllib.request.Request(url + provider + '/' + reciver)
#with urllib.request.urlopen(req,data=data) as f:
#    resp = f.read()
#    print(resp)


#old
#req = urllib.request.Request(url, data)
#response = urllib.request.urlopen(req)
#print(response)
#older
#response = urlopen(url + provider + reciver)
#html = response.read()
#print(html)
