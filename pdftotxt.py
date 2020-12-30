import os
from os import listdir
from os.path import isfile, join
import convertapi
import nltk
import glob
import re
# nltk.download('punkt') #run this the first time

"""
observations Colin:
- sometimes the sidebar containing address and such is mixed in with the text
- sometimes the sentence is split up in two

todo:
- imrpove conversion
- catch large files
"""


def convertpdftotxt(filename, path_txt, path_pdf = None, overwrite = False):
    
    #check if already converted
    exists = check_if_txt_exists(path_txt, filename)

    if exists and overwrite == False:
        pass
        # convertedfile = os.path.join(path_txt, filename.split('.')[0]) + '.txt'
    else:
        if path_pdf != None:
            filepath = os.path.join(path_pdf, filename)
        else:
            filepath = filename
        convertapi.api_secret = 'GQohrMpAMRIVg4JS'  #QKLmVCcVJHkpZ8AN
        convertapi.convert('txt', {'File': filepath}, from_format = 'pdf').save_files(path_txt)

def check_if_txt_exists(path_txt, filename):
    """
    doing this to save API credits, if you want to overwrite set overwrite to true
    """
    file_name = filename.split('.')[0]
    txt_files = [f.split('.')[0] for f in listdir(path_txt) if isfile(join(path_txt, f))]

    if file_name in txt_files:
        print('File already exists, pass overwrite = True if you want to overwrite')
        return True
    else:
        print('File does not yet exist, is now converted and stored')
        return False

def text_preprocessing(text):
    #some manual preprocessing
    text = text.replace('lij k', 'lijk')
    text = text.replace('ministerie van', 'Ministerie van')
    text = regular_expressions(text)

    return text

def regular_expressions(text):
    """
    doing a few regular expressions here for text processing. Not much experience with this so may be innefficient.
    Somehow it doesn't find everything at once, so I am doing a loop until no improvements are found anymore.    
    """
    prev_len = len(text)-1 #otherwise they are the same at the start
    while prev_len != len(text):
        prev_len = len(text)

        # removes all ICCbnumber occurences. difference is necessary because the numbers change when deleting something
        difference = 0
        for match in re.finditer('(?<= ICCb)\w+', text):
            text = text[:match.start()-4] + text[match.end():]
            difference += match.end() - match.start()

        #remove occurences of e.g. Pagina 1 van 5
        difference = 0
        for match in re.finditer('(?<=Pagina)\s\d+\s\w+\s\d+', text):
            text = text[:match.start()-6] + text[match.end():]
            difference += match.end() - match.start()

        new_lines = re.compile('\n{2,9}')
        text = re.sub(new_lines, '\n\n\n', text.strip())

    return text


# f = open("C:/Users/clieshou/PycharmProjects/nlp-demo/data/txt/tk-bijlage-wob-iccb-2-deelbbesluit-met-handtekening.txt", "r", encoding="utf8")
# text = f.read()
# text = text[:3000]
