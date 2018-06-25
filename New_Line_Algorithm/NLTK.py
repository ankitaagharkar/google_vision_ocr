import spacy
import os
import json
import subprocess
import re
from pprint import pprint

import nltk
from nameparser.parser import HumanName
from nltk.corpus import wordnet, stopwords
from nltk.tag.stanford import StanfordNERTagger
from nltk.stem import PorterStemmer
import spacy
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

debug=True
nlpSpacy = spacy.load('en')
# doc = nlpSpacy( """
# YOUR SOCIAL SECURITY CARD ADULTS: Sign this card in ink immediately. CHILDREN: Do not sign until age 18 or your first job, whichever is earlier. Keep your card in a safe place to prevent loss or theft. DO NOT CARRY THIS CARD WITH YOU. Do not laminate. VALID FOR WORK ONLY WITH DHS AUTHORIZATION497-69-3198 VE THIS NUMBER HAS BEEN ESTABLISHED FOR GIACOMO DOMENICONI SIGNATURE 05/19/2017 OVO SU ON OLLING OG
# """)
doc = nlp( """
YOUR SOCIAL SECURITY CARD ADULTS: Sign this card in ink immediately. CHILDREN: Do not sign until age 18 or your first job, whichever is earlier. Keep your card in a safe place to prevent loss or theft. DO NOT CARRY THIS CARD WITH YOU. Do not laminate. AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL CURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES 069-78-6917 THIS NUMBER HAS BEEN ESTABLISHED FOR DEQUANNA ALLISONBROWN NISTRA AL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATUS GereSOCIAL SECURITY ADMINISTRATION M ED SIGNATURE SIGNATURE 07/25/2011 A HUOMIOTUM W 001001111 AND VOOS VOLVO SIVAS ON NOVUSINI

""")
result = []
countStart = 0
for index, entity in enumerate(doc.ents):
    # print(entity)
    if countStart > 3:
        break
    elif countStart > 0:
        countStart += 1
    # entityText = " ".join(re.split("\s+", entity.text, flags=re.UNICODE))
    entityText = ''.join(ent if ent.isalpha()
                         else '' for ent in entity.text.split(' '))
    if debug:
        print('len(entity)', len(entityText), entityText,entity.label_)
    if len(entityText) > 1:         # Checking of Number of characters in the text
        if entity.label_ == 'PERSON' or entity.label_ == 'CARDINAL':
            countStart += 1
            result.append(entity.text)
            if debug:
                print(entity.text)
print('before stopwords')
print(result)
