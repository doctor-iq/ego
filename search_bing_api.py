GNU nano 2.9.3                  search_bing_api.py                            

from requests import exceptions
import argparse
import requests
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
        help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True,
        help="path to output directory of images")
args = vars(ap.parse_args())

API_KEY = "API_KEY_HIER"
MAX_RESULTS = 100
GROUP_SIZE = 50

URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

EXCEPTIONS = set([IOError, exceptions.RequestException, exceptions.HTTPError, exceptions.ConnectionError, exceptions.Timeout])

term = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}

print("[EGO] suche Bing API nach '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()

results = search.json()
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
print("[EGO] {} Ergebnisse gesamt fur '{}'".format(estNumResults,
        term))

total = 0

for offset in range(0, estNumResults, GROUP_SIZE):
        print("[EGO] erstelle Gruppenanfrage fur {}-{} von {}...".format(
                offset, offset + GROUP_SIZE, estNumResults))
        params["offset"] = offset
        search = requests.get(URL, headers=headers, params=params)
        search.raise_for_status()
        results = search.json()
        print("[EGO] speicher Bilder fur Gruppe {}-{} von {}...".format(
                offset, offset + GROUP_SIZE, estNumResults))

        for v in results["value"]:

                try:
                        print("[EGO] beziehe: {}".format(v["contentUrl"]))
                        r = requests.get(v["contentUrl"], timeout=30)

                        ext = v["contentUrl"][v["contentUrl"].rfind("."):]
                        p = os.path.sep.join([args["output"], "{}{}".format(
                                str(total).zfill(8), ext)])

                        f = open(p, "wb")
                        f.write(r.content)
                        f.close()

                except Exception as e:
                        if type(e) in EXCEPTIONS:
                                print("[EGO] uberspringe: {}".format(v["contentUrl"]))
                                continue

                image = cv2.imread(p)

                if image is None:
                        print("[EGO] losche: {}".format(p))
                        os.remove(p)
                        continue

                total += 1
                image = cv2.imread(p)

                if image is None:
                        print("[EGO] losche: {}".format(p))
                        os.remove(p)
                        continue

                total += 1
