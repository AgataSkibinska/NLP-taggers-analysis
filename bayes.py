import pathlib
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import xml.etree.ElementTree as ET
from sklearn.metrics import accuracy_score, f1_score

text_categories = ['Albania', 'Amerykanscy-prozaicy', 'Arabowie', 'Astronautyka', 'Choroby', 'Egipt', 'Ekologia-roslin',
                   'Filmy-animowane', 'Galezie-prawa', 'Gry-komputerowe', 'Karkonosze', 'Katolicyzm', 'Komiksy',
                   'Komputery', 'Kotowate', 'Kultura-Chin', 'Monety', 'Muzyka-powazna', 'Narciarstwo', 'Narkomania',
                   'Niemieccy-wojskowi', 'Optyka', 'Pierwiastki-chemiczne', 'Pilka-nozna', 'Propaganda-polityczna', 'Rachunkowosc',
                   'Samochody', 'Samoloty', 'Sporty-silowe', 'System-opieki-zdrowotnej-w-Polsce', 'Szachy', 'Wojska-pancerne',
                   'Zegluga', 'Zydzi']


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
    filtered_df = ""
    for index, row in df.iterrows():
        tags = get_part_of_speech_tags(part)
        for tag in tags:
            if tag in str(row['tag']):
                filtered_df = filtered_df + " " + str(row['base'])
    arr = [filtered_df]
    return arr


def build_dir(text, count_vect):
    count_vect.fit(text)


def change_to_count_vector(list, count_vect):
    X_train_counts = count_vect.transform(list)
    return X_train_counts.toarray().flatten()


def build_directory(path_to_files, part):
    count_vect = CountVectorizer(max_features=1000)
    text = ""
    for path in pathlib.Path(path_to_files).iterdir():
        if path.is_file():
            df = create_df_for_file(path)
            filtered_list = filter_part_of_speech(part, df)
            text = text + filtered_list[0]
    build_dir([text], count_vect)
    return count_vect


def create_x_y(path_to_files, part, count_vect):
    X = []
    y = []
    for path in pathlib.Path(path_to_files).iterdir():
        if path.is_file():
            df = create_df_for_file(path)
            filtered_list = filter_part_of_speech(part, df)
            vector = change_to_count_vector(filtered_list, count_vect)
            for category in text_categories:
                if category in str(path):
                    label = category
                    y.append(label)
            X.append(vector)
    return X, y

#WCRFT2 NOUN
count_vect = build_directory('parsed_data_wcrft2', 'noun')
X, y = create_x_y('parsed_data_wcrft2', 'noun', count_vect)
X_test, y_test = create_x_y('parsed_test_data_wcrft2', 'noun', count_vect)
clf = MultinomialNB().fit(X, y)
y_pred = clf.predict(X_test)
print("acc: ", accuracy_score(y_test, y_pred))
print("f1: ", f1_score(y_test, y_pred, average = 'micro'))


#WCRFT2 VERB
count_vect = build_directory('parsed_data_wcrft2', 'verb')
X, y = create_x_y('parsed_data_wcrft2', 'verb', count_vect)
X_test, y_test = create_x_y('parsed_test_data_wcrft2', 'verb', count_vect)
clf = MultinomialNB().fit(X, y)
y_pred = clf.predict(X_test)
print("acc: ", accuracy_score(y_test, y_pred))
print("f1: ", f1_score(y_test, y_pred, average = 'micro'))


#WCRFT2 ADJ
count_vect = build_directory('parsed_data_wcrft2', 'adj')
X, y = create_x_y('parsed_data_wcrft2', 'adj', count_vect)
X_test, y_test = create_x_y('parsed_test_data_wcrft2', 'adj', count_vect)
clf = MultinomialNB().fit(X, y)
y_pred = clf.predict(X_test)
print("acc: ", accuracy_score(y_test, y_pred))
print("f1: ", f1_score(y_test, y_pred, average = 'micro'))
