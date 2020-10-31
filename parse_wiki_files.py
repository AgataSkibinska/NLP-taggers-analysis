import json
import pathlib

import requests
import xml.etree.ElementTree as ET

clarinpl_url = "http://ws.clarin-pl.eu/nlprest2/base"
user_mail = ""

url = clarinpl_url + "/process"

def ccl_base_tag(ccl):
    tree = ET.fromstring(ccl)
    return {tok.find('./lex/base').text: tok.find("./lex/ctag").text for tok in tree.iter('tok')}


def tag_data(lpmn, data_path, out_path):
    for path in pathlib.Path(data_path).iterdir():
        if path.is_file():
            current_file = open(path, "r", encoding='utf-8')
            text = current_file.read()
            payload = {'text': text, 'lpmn': lpmn, 'user': user_mail}
            headers = {'content-type': 'application/json'}

            r = requests.post(url, data=json.dumps(payload), headers=headers)
            ccl = r.content.decode('utf-8')
            path = str(path).replace(".txt", "").replace("data\\", "")
            f = open(out_path +"\\" + path, "x",  encoding='utf-8')
            f.write(ccl)
            f.close()
            current_file.close()


#wcrft2
tag_data("wcrft2", "data", "parsed_data")
tag_data("wcrft2", "test_data", "parsed_data")

# MorphoDiTa
tag_data("morphoDita", "data", "parsed_test_data")
tag_data("morphoDita", "test_data","parsed_test_data")