import re
import spacy
nlp = spacy.load("nl_core_news_md")

def create_ner_dict(text):
    """
    To get a descent overview of what words are available for what label, I make a dictionary of the structure:
    NER_dict : {
        label : {
            text : {
                startchar : endchar,
                ... : ...
            }
            ...
        }
        ...
    }
    
    """

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
    """
    Receives the entity provided by the user, and returns every occurence of it in the entire file, 
    together with the whole sentence it occurs in. 
    
    Returns the sentences that contain the requested_entity
    """

    accepted_splits = []
    
    for m in re.finditer(requested_entity, text):        
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




# f = open("C:/Users/clieshou/PycharmProjects/nlp-demo/data/txt/tk-bijlage-wob-iccb-2-deelbbesluit-met-handtekening.txt", "r", encoding="utf8")
# text = f.read()

# print(create_ner_dict(text))
