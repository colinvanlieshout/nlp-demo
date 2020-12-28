import os
import convertapi
from nltk import sent_tokenize


def convertpdftotxt(filename):
    convertapi.api_secret = 'QKLmVCcVJHkpZ8AN'
    convertedfile = convertapi.convert('txt', {'File': filename}, from_format = 'pdf').save_files('./')
    convertedfile = str(convertedfile[0])
    with open(convertedfile, encoding='utf8') as filehandle:
        lines = filehandle.read() #use read instead of readlines
        sent_split = sent_tokenize(lines)
    #with open(convertedfile, 'w', encoding='utf8') as filehandle:
        #lines = filter(lambda x: x.strip(), lines)
        #filehandle.writelines(lines)
        #txt = 
        #print(lines)
        #sent_split = sent_tokenize(lines)
    return sent_split  


### Main script ###

# Upload some pdf - pdffile
convertedfilename = convertpdftotxt(pdffile) #returns list of tokenized sentences



