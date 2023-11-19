import json
from time import sleep

import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"

headers = {
    "User-Agent": USER_AGENT,
}
LISTINGS_FILENAME = "flatfox_listings/flatfox_listings_100_{i}.json"


if __name__ == "__main__":
    next_url = "https://flatfox.ch/api/v1/public-listing/"
    i = 0
    while next_url:
        result = requests.get(
            next_url,
            headers=headers,
        )
        result_dict = json.loads(result.text)
        with open(LISTINGS_FILENAME.format(i=i), "w") as f:
            f.write(json.dumps(result_dict, indent=4))

        next_url = result_dict.get("next")
        i += 1
        sleep(1)
