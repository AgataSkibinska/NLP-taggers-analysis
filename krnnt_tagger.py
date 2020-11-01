import requests


def tag_data_using_krnnt(input_file_path, output_file_path):
    url = ' http://localhost:9003'

    text = open(input_file_path, "r", encoding="utf8").read()

    r = requests.post(url, data=text.encode("utf-8"))
    output = r.content.decode('utf-8')

    with open(output_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(output)
