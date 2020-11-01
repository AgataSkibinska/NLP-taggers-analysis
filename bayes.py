import pathlib

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import xml.etree.ElementTree as ET
text_categories = ['Albania', 'Amerykanscy-prozaicy', 'Arabowie', 'Astronautyka','Choroby', 'Egipt', 'Ekologia-roslin'
                   'Filmy-animowane', 'Galezie-prawa', 'Gry-komputerowe', 'Karkonosze', 'Katolicyzm', 'Komiksy', 'Komputery'
                   'Kotowate', 'Kultura-Chin', 'Monety', 'Muzyka-powazna', 'Narciarstwo', 'Narkomania', 'Niemieccy-wojskowi'
                   'Optyka', 'Pierwiastki-chemiczne', 'Pilka-nozna', 'Propaganda-polityczna', 'Rachunkowosc', 'Samochody',
                   'Samoloty', 'Sporty-silowe', 'System-opieki-zdrowotnej-w-Polsce', 'Szachy', 'Wojska-pancerne', 'Zegluga',
                   'Zydzi']


def ccl_base_tag(ccl):
    tree = ET.fromstring(ccl)
    return {tok.find('./lex/base').text: tok.find("./lex/ctag").text for tok in tree.iter('tok')}


def create_df_for_file(data_path):
    current_file = open(str(data_path), "r", encoding='utf-8')
    text = current_file.read()
    bases_tags = ccl_base_tag(text)
    df = pd.DataFrame(bases_tags.items(), columns=("base", "tag"))
    current_file.close()
    return df


def get_part_of_speech_tags(part):
    if part == 'verb':
        return ['fin', 'bedzie', 'aglt', 'praet', 'impt', 'imps', 'inf', 'pcon',
                'pant', 'ger', 'pact', 'ppas', 'winien']
    elif part == 'noun':
        return ['subst', 'depr']
    elif part == 'adj':
        return ['adj', 'adja', 'adjp', 'adjc']


def filter_part_of_speech(part, df):
    filtered_df = []
    for index, row in df.iterrows():
        tags = get_part_of_speech_tags(part)
        for tag in tags:
            if str(row['tag']).__contains__(tag):
                filtered_df.append(row['base'])
    return filtered_df


def change_to_count_vector(list):
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(list)
    return X_train_counts


X = []
y = []
for path in pathlib.Path("paesed_data_wcrft2").iterdir():
    if path.is_file():
            df = create_df_for_file(path)
            filtered_list = filter_part_of_speech('noun', df)
            vector = change_to_count_vector(filtered_list)
            for category in text_categories:
                if str(path).__contains__(category):
                    label = category
                    y.append(label)
            X.append(vector)

clf = MultinomialNB().fit(X, y)