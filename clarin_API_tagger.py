import json
import requests


def tag_data_using_clarinAPI(tagger, input_file_path, output_file_path):

    clarinpl_url = "http://ws.clarin-pl.eu/nlprest2/base"
    user_mail = ""

    url = clarinpl_url + "/process"
    lpmn = tagger

    text = open(input_file_path, "r", encoding="utf8").read()

    payload = {'text': text, 'lpmn': lpmn, 'user': user_mail}
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    ccl = r.content.decode('utf-8')

    with open(output_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(ccl)


if __name__ == '__main__':
    # taggers = ["wcrft2", "morphoDita"]
    taggers = ["wcrft2"]

    for tagger in taggers:
        tag_data_using_clarinAPI(tagger, "pol_eval_data/test-raw.txt", f"pol_eval_data/test-tagged-{tagger}.ccl")