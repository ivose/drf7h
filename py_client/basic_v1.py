import requests

endpoint = "http://127.0.0.1:8000/api/products/"
endpoint = "https://httpbin.org/get"

#requests.get() # API -> Method
#get_response = requests.get(endpoint)
get_response = requests.get("https://httpbin.org/anything", json={"query":"Hello world"})
#print(get_response.text)
print(get_response.json())

# http request -> html
# rest api http request ->json
# javascript object notation ~ python dict

