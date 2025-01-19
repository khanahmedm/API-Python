import requests

url = "https://api.github.com/users/khanahmedm/repos"

response = requests.get(url)

if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        print(f"Repository Name: {repo['name']}")
else:
    print(f"Error: {response.status_code}, {response.text}")
