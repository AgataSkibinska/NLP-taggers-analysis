import pathlib

from krnnt_tagger import *
from ktnnt_to_xml_parser import *


def parse_data_folder(data_type):
    data_path = f'wiki_{data_type}_34_categories_data'
    txt_data_path = 'out_raw_txt'
    final_data_path = f'wiki_tagged/{data_type}/krnnt'
    f = 1
    for path in pathlib.Path(data_path).iterdir():
        if path.is_file():
            print(f"file number:{f} {path.name}")
            f += 1
            out_path = txt_data_path+"/"+path.name
            tag_data_using_krnnt(input_file_path=path, output_file_path=out_path)
            tagged_out_path = final_data_path + "/" + path.name.split(".")[0] + ".ccl"
            parse_krnnt_output_to_xml(krnnt_file=out_path, output_file=tagged_out_path)


if __name__ == '__main__':
    parse_data_folder("train")
    parse_data_folder("test")