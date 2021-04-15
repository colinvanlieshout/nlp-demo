import os
from os import listdir
from os.path import isfile, join
import convertapi
import nltk
import glob
import re
# nltk.download('punkt') #run this the first time

"""
We could still invest some time in optimizing the conversion
"""


def convertpdftotxt(filename, path_txt, path_pdf = None, overwrite = False):
    """ 
    Takes a pdf file and converts it into txt, using convertapi. Stores it locally.

    parameters:
    - filename: ...pdf
    - path_txt: where does the file need to be stored
    - path_pdf: None by default as we upload in Streamlit
    - overwrite: in case we optimize the conversion tool, we can overwrite existing files
    """
    
    if path_pdf != None:
        if not os.path.exists(path_pdf):
            os.makedirs(os.path.join(path_pdf, filename))
    if not os.path.exists(path_txt):
        os.makedirs(os.path.join(path_txt, filename))

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
        convertapi.api_secret = 'lQuFRRSxR70fEJ6x'  #QKLmVCcVJHkpZ8AN
        convertapi.convert('txt', {'File': filepath}, from_format = 'pdf').save_files(path_txt)

def check_if_txt_exists(path_txt, filename):

    """
    As API credits for conversionapi are limited, we don't want to convert each time we run. 
    Therefore, this function checks whether there is already a processed file for the pdf.
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
    """
    To make the NLP task easier we do some preprocessing.
    It just takes a text, applies some functions, and returns the text/.
    """

    #some manual preprocessing
    text = text.replace('lij k', 'lijk') #there are some mistransformations where there is a space in the middle of the word. There are some other occurences but this was most frequent.
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
        for match in re.finditer('(?<=Pagina)\s+\d+\s+\w+\s+\d+', text):
            text = text[:match.start()-6] + text[match.end():]
            difference += match.end() - match.start()

        #removes empty sentences if there are more than 2 at once
        new_lines = re.compile('\n{2,9}')
        text = re.sub(new_lines, '\n\n\n', text.strip())

    return text


# f = open("C:/Users/clieshou/PycharmProjects/nlp-demo/data/txt/tk-bijlage-wob-iccb-2-deelbbesluit-met-handtekening.txt", "r", encoding="utf8")
# text = f.read()
# text = text[:3000]
