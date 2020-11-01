

def segmentation(text):
    text = text.split()
    sep1 = [".", ",", "!", "?", ":", ";", ")", "\"", "]", ":"]
    sep2 = ["(", "[", "\""]
    result = []

    for index, word in enumerate(text):
        if not is_word_a_short(word) and not is_word_one_letter_short(word):
            if word[-1] in sep1 and word[0] in sep2:
                separated_word = word[1:-1]
                result.append(word[0])
                result.append(word[1:-1])
                result.append(word[-1])
            elif word[-1] in sep1:
                result.append(word[:-1])
                result.append(word[-1])
            elif word[0] in sep2:
                result.append(word[0])
                result.append(word[1:])
            else:
                result.append(word)
        else:
            result.append(word)
    return result


def is_word_a_short(word):
    shorts = ["np.", "itd.", "tzn.", "itp.", "m.in.", "ect.", "tys.", "lek.", "lic.", "inż.", "ul.", "al.", "def.",
              "dot.", "śp.", "tzw.", "tys."]
    res = False
    if word in shorts:
        res = True
    return res


def is_word_one_letter_short(word):
    res = False
    if len(word) == 2 and word[1] == ".":
        res = True
    return res



if __name__ == '__main__':
    # f = open("Albania_59.txt", "r", encoding="utf8")
    #
    # text = segmentation(f.read())

    text = "w. 2 tys. (mamama jj kk)."
    text = segmentation(text)

    for word in text:
        print(word)
