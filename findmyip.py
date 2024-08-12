import requests

# Get the public IP address
ip = requests.get('https://api.ipify.org').text
print(f"My public IP address is: {ip}")
