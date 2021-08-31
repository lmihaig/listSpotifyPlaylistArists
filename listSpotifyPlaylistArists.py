import requests
import json

output = open("artists.txt", "w")
print("Enter Spotify Playlist Link:")
playlistId = input().split("playlist/")[1].split("?")[0]
print("Enter Token:")
token = input()
response_json = []
counter = {}


numberofItems = requests.get(f"https://api.spotify.com/v1/playlists/{playlistId}/tracks?market=Ro&&fields=total",
                             headers={
                                 "Content-Type": "application.json",
                                 "Authorization": f"Bearer {token}"
                             }
                             ).json()["total"]
iterations = (numberofItems // 100) + 1


def getNames(offset):
    url = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks?market=Ro&fields=items(track(artists(name)))&offset={offset}"
    response = requests.get(url,
                            headers={
                                "Content-Type": "application.json",
                                "Authorization": f"Bearer {token}"
                            }
                            )

    global response_json
    response_json = response_json + response.json()["items"]


for i in range(iterations):
    getNames(i*100)

for i in response_json:
    name = i["track"]["artists"][0]["name"]
    if name in counter.keys():
        counter[name] += 1
    else:
        counter[name] = 1

for i in sorted(counter, key=counter.get, reverse=True):
    output.write(f"{counter[i]} songs from {i}\n")

output.close()
