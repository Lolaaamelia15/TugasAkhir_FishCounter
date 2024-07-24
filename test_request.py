import requests

response = requests.get('https://fishcounterta.000webhostapp.com/status.php')
print(response.status_code)
print(response.json()["hitung"])
print(response.content)
f = open("demofile2.txt", "wb")
f.write(response.content)
f.close()