import spacy
nlp = spacy.load("nl_core_news_md")

def text_preprocessing(text):
    #some manual preprocessing
    text = ' '.join(text.split()) #remove occurences of multiple white space
    text = text.replace('\n', ' ')
    text = text.replace('lij k', 'lijk')
    text = text.replace('ministerie van', 'Ministerie van')

    return text

def create_ner_dict(doc):
    NER_dict = {}

    for ent in doc.ents:
        #many are just numbers, skip these because they are not useful
        if ent.text.isnumeric():
            pass
        else:
            if ent.label_ not in NER_dict:
                NER_dict[ent.label_] = {}
            if ent.text not in NER_dict[ent.label_]:
                NER_dict[ent.label_][ent.text] = {}
            if ent.start_char not in NER_dict[ent.label_][ent.text]:
                NER_dict[ent.label_][ent.text][ent.start_char] = ent.end_char

    return NER_dict


f = open("C:/Users/clieshou/PycharmProjects/nlp-demo/data/txt/tk-bijlage-wob-iccb-2-deelbbesluit-met-handtekening.txt", "r", encoding="utf8")
text = f.read()
text = text_preprocessing(text)
doc = nlp(text)

print(create_ner_dict(doc))


# text = "Het gaat om Colin Lieshout, (interne) e-mailberichten en conceptteksten van of met het ministerie van Justitie en Veiligheid."
# # text = "Apple is looking at buying U.K. startup for $1 billion"
# doc = nlp(text)
# print(doc)
# print([(w.text, w.pos_) for w in doc])