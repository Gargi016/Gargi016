# fetch_data.py
import requests
import json
import os

GITHUB_USERNAME = "Gargi016"


GITHUB_TOKEN = os.getenv("PAT_TOKEN", "abc")

headers = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

query = """
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""

variables = {"username": GITHUB_USERNAME}
response = requests.post("https://api.github.com/graphql", json={'query': query, 'variables': variables}, headers=headers)

if response.status_code == 200:
    data = response.json()
    with open('contributions.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Successfully fetched and saved contribution data.")
else:
    raise Exception(f"Query failed: {response.status_code}. {response.text}")
