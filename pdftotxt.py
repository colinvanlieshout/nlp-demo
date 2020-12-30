import os
from os import listdir
from os.path import isfile, join

import convertapi
import nltk
import glob
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
    text = ' '.join(text.split()) #remove occurences of multiple white space
    text = text.replace('\n', ' ')
    text = text.replace('lij k', 'lijk')
    text = text.replace('ministerie van', 'Ministerie van')

    return text


