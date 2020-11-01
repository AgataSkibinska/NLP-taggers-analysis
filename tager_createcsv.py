import json
import pathlib
import pandas as pd

import requests
import xml.etree.ElementTree as ET

clarinpl_url = "http://ws.clarin-pl.eu/nlprest2/base"
user_mail = ""

url = clarinpl_url + "/process"
# lpmn = "morphoDita"


def ccl_orths(ccl):
    tree = ET.fromstring(ccl)
    return [orth.text for orth in tree.iter('orth')]


def ccl_poses(ccl):
    tree = ET.fromstring(ccl)
    return [tok.find('./lex/ctag').text.split(":")[0] for tok in tree.iter('tok')]


def ccl_base_tag(ccl):
    tree = ET.fromstring(ccl)
    return {tok.find('./lex/base').text: tok.find("./lex/ctag").text for tok in tree.iter('tok')}


def tag_data(lpmn, data_path):
    main_df = pd.DataFrame(columns=("base", "tag"))
    for path in pathlib.Path(data_path).iterdir():
        if path.is_file():
            current_file = open(path, "r", encoding='utf-8')
            text = current_file.read()
            payload = {'text': text, 'lpmn': lpmn, 'user': user_mail}
            headers = {'content-type': 'application/json'}

            r = requests.post(url, data=json.dumps(payload), headers=headers)
            ccl = r.content.decode('utf-8')
            print(ccl)
            bases_tags = ccl_base_tag(ccl)
            print(bases_tags)
            df = pd.DataFrame(bases_tags.items(), columns=("base", "tag"))
            main_df = main_df.append(df, ignore_index=True)
            print(main_df)
            current_file.close()
    main_df.to_csv(lpmn + '.csv')
            #print(ccl)
            #orths = ccl_orths(ccl)
            #print("Tokeny " + str(orths))

            #poses = ccl_poses(ccl)
            #print("Positions "+str(poses))


#wcrft2
tag_data("wcrft2", "poleval_data")

#MorphoDiTa
tag_data("morphoDita", "poleval_data")
