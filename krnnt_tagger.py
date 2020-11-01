import requests

poleval_test_path = 'pol_eval_data/test-raw.txt'
url = ' http://localhost:9003'

text = open(poleval_test_path, "r", encoding="utf8").read()

r = requests.post(url, data=text.encode("utf-8"))
output = r.content.decode('utf-8')
print(output)

with open("pol_eval_data/test-krnnt-output.txt", "w", encoding="utf-8") as text_file:
    text_file.write(output)