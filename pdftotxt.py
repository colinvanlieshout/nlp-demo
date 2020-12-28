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
- send output to transformer
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
        # convertedfile = convertapi.convert('txt', {'File': filepath}, from_format = 'pdf').save_files(path_txt)
        # convertedfile = str(convertedfile[0])

    # with open(convertedfile, encoding='utf8') as filehandle:
    #     lines = filehandle.read() #use read instead of readlines
    #     sent_split = nltk.sent_tokenize(lines)


    #with open(convertedfile, 'w', encoding='utf8') as filehandle:
        #lines = filter(lambda x: x.strip(), lines)
        #filehandle.writelines(lines)
        #txt = 
        #print(lines)
        #sent_split = sent_tokenize(lines)
    # return sent_split  

def check_if_txt_exists(path_txt, filename):
    """
    doing this to save API credits, if you want to overwrite set overwrite to true
    """
    file_name = filename.split('.')[0]
    txt_files = [f.split('.')[0] for f in listdir(path_txt) if isfile(join(path_txt, f))]

    if file_name in txt_files:
        print('exists')
        return True
    else:
        print('does not exist')
        return False







### Main script ###

# path_pdf= 'data/pdf'
# path_txt = 'data/txt'
# filename = 'tk-besluit-op-bezwaar-op-grond-van-de-wob-inzake-poch-en-stand-van-zaken-onderzoek-commissie-dossier-j-a-poch.pdf'
# pdffile = 'data/pdf/tk-bijlage-scan-geanonimiseerd-besluit-en-inventarislijst-wob-zelfonderzoek-door-advocaten.pdf'

# check_if_txt_exists(path_pdf, path_txt, filename)

# convertedfilename = convertpdftotxt(filename, path_txt, path_pdf) #returns list of tokenized sentences

# print(convertedfilename)

# print(convertedfilename)

# convertedfilename.write('test.txt')



