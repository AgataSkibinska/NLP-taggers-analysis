#%%

f = open("Albania_59.txt", "r",encoding="utf8")
#print(f.read())
def segmentation(text):
    text = text.split()
    sep1 = [".",",","!","?",":",";",")","\"", "]"]
    sep2 = ["(", "[", "\""]
    result = []
    for index, word in enumerate(text):
        if word[-1] in sep1 and word[0] in sep2:
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
    return result

text  = segmentation(f.read())

for word in text:
    print(word)