import requests

# Type GET request
r = requests.get('https://google.com')

# Printing object type - Response
# print("Type :", type(r))

# Printing Status Code
print("Status Code :", r.status_code)

# Printing the content of the response
print(r.text)