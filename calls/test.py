import requests

try:
    res = requests.post(
        url="http://0.0.0.0:8000/demystify",
        json={
            "file_url": "https://raw.githubusercontent.com/mfahadakbar/Caret_Multiple/master/call4.m4a"
        },
        timeout=300,  # Adjust as necessary
    )
    res.raise_for_status()  # Raises an exception for 4XX or 5XX errors
    print(res.json())
except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("OOps: Something Else", err)


# curl -X POST 'http://127.0.0.1:8000/demystify' -H 'Content-Type: application/json' -d '{"file_url": "https://www.mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Samples/AFsp/M1F1-Alaw-AFsp.wav"}'

# print(f"printing +++++ {res.json()}")
