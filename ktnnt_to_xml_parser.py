from lxml import etree


def parse_krnnt_output_to_xml(krnnt_file, output_file):
    krnnt_text = open(krnnt_file, 'r', encoding='utf-8')

    root = etree.Element('chunkList')

    current_chunk_id = 1
    current_chunk = etree.Element('chunk', id=f"{current_chunk_id}", type='p')
    root.append(current_chunk)

    current_sentence_id = 1
    current_sentence = etree.Element('sentence', id=f"{current_sentence_id}")
    current_chunk.append(current_sentence)

    for line in krnnt_text:
        line = line.replace("\n", "")
        split = line.split("\t")

        # Pusta linijka oddziela zdania
        if len(split) == 1 and split[0] == '':
            current_sentence_id += 1
            current_sentence = etree.Element('sentence', id=f"{current_sentence_id}")
            current_chunk.append(current_sentence)
        else:
            # Druga linijka opisująca słowo
            if split[0] == '':
                lex = etree.Element('lex', disamb='1')

                base = etree.Element('base')
                base.text = split[1]
                lex.append(base)

                ctag = etree.Element('ctag')
                ctag.text = split[2]
                lex.append(ctag)
                current_tok.append(lex)
                current_sentence.append(current_tok)
            else:
                # kropka przyklejona do slowa wczesniej
                if split[1] == 'none':
                    current_sentence.append(etree.Element('ns'))
                # wszystko reszta - pierwsza linijka opisująca slowo
                current_tok = etree.Element('tok')
                orth = etree.Element('orth')
                orth.text = split[0]
                current_tok.append(orth)

    s = etree.tostring(root, pretty_print=True, encoding='utf-8')
    with open(output_file, "wb") as text_file:
        text_file.write(s)
    return

if __name__ == '__main__':
    parse_krnnt_output_to_xml(output_file='pol_eval_data/test-tagged-krnnt.ccl',
                              krnnt_file="pol_eval_data/test-krnnt-output.txt")

