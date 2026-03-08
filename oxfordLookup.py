
from dotenv import load_dotenv
from os import getenv

import requests

load_dotenv()


APP_ID = getenv('APP_ID')
APP_KEY = getenv('APP_KEY')
language = "en-gb"



def getDefinitions(word_id):
    url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/entries/{language}/{word_id}"

    headers = {
        "app_id": APP_ID,
        "app_key": APP_KEY
    }

    response = requests.get(url, headers=headers)
    print("Status:", response.status_code)
    data = response.json()
    if 'error' in data.keys():
        # error_message = "bunday so'z topilmadi!"
        # return error_message
        return False

    output = {}
    definitions = []
    data = response.json()
    # print(data['results'])
    entries = data["results"][0]["lexicalEntries"]
    # pprint(entries)
    for entry in entries:
        for sense in entry["entries"][0]["senses"]:
            # print(sense.get("definitions", []))
            # print(sense)
            # print(sense["definitions"][0])
            definitions.append(f"{sense['definitions'][0]}")
        output["definitions"] = "\n".join(definitions)
        audio = entry["entries"][0]["pronunciations"][0]["audioFile"]
        output["audio"] = audio
        # print(entry["entries"][0]["pronunciations"][0]["audioFile"])
    print("++++++++++++++++++++")

    return output

if __name__ == "__main__":
    from pprint import pprint
    pprint(getDefinitions('applfe'))