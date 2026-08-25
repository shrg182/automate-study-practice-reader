from urllib.request import Request

def make_request(url, token=None):
    headers = {"Accept": "application/json"}
    if token: headers["Authorization"] = f"Bearer {token}"
    return Request(url, headers=headers)

if __name__ == "__main__": print(dict(make_request("https://example.com/data").header_items()))
