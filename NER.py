import re
import streamlit as st
import spacy
nlp = spacy.load("nl_core_news_md")

def create_ner_dict(text):
    doc = nlp(text)

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

def find_sentences_with_entity(requested_entity, text):        
    accepted_splits = []
    
    for m in re.finditer(requested_entity, text):
        
        # print(m.start())

        #goal here is to get the sentence itself instead of cutting it off in the middle, doesn't work perfectly yet
        search_area = text[m.start()-300:m.end()+300]
        splits = search_area.split('.')
        # splits = splits[1:-1]
        for split in splits:
            if requested_entity in split:
                if split not in accepted_splits:
                    # st.write(split)
                    accepted_splits.append(split)
    
    accepted_splits = list(set(accepted_splits))

    return accepted_splits

# def display_sentences_with_entity(requested_entity, text):
#     accepted_splits = find_sentences_with_entity(requested_entity, text)

#     for i, split in enumerate(accepted_splits):
#         st.write("*Voorbeeld ", str(i), "*")
#         #make the relevant word bold
#         split = split.replace(requested_entity, "**" + requested_entity + "**")
#         st.write(split + '.')

# f = open("C:/Users/clieshou/PycharmProjects/nlp-demo/data/txt/tk-bijlage-wob-iccb-2-deelbbesluit-met-handtekening.txt", "r", encoding="utf8")
# text = f.read()

# print(create_ner_dict(text))


# text = "Het gaat om Colin Lieshout, (interne) e-mailberichten en conceptteksten van of met het ministerie van Justitie en Veiligheid."
# # text = "Apple is looking at buying U.K. startup for $1 billion"
# doc = nlp(text)
# print(doc)
# print([(w.text, w.pos_) for w in doc])