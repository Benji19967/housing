import requests

if __name__ == "__main__":
    result = requests.get("https://flatfox.ch/api/v1/public-listing/")
    print(result.json())
