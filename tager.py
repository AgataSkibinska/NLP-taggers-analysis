import json
import requests
import xml.etree.ElementTree as ET

clarinpl_url = "http://ws.clarin-pl.eu/nlprest2/base"
user_mail = ""

url = clarinpl_url + "/process"
lpmn = "wcrft2"

text = open("Albania_59.txt", "r", encoding="utf8").read()

payload = {'text': text, 'lpmn': lpmn, 'user': user_mail}
headers = {'content-type': 'application/json'}

r = requests.post(url, data=json.dumps(payload), headers=headers)
ccl = r.content.decode('utf-8')
print(ccl)



# Tokenizacja

def ccl_orths(ccl):
    tree = ET.fromstring(ccl)
    return [orth.text for orth in tree.iter('orth')]


orths = ccl_orths(ccl)
print("Tokeny "+str(orths))

def ccl_poses(ccl):
    tree = ET.fromstring(ccl)
    return [tok.find('./lex/ctag').text.split(":")[0] for tok in tree.iter('tok')]


poses = ccl_poses(ccl)
print("Positions "+str(poses))


