import nltk
from nltk.corpus import stopwords, wordnet as wn
from nltk import word_tokenize, sent_tokenize
import re
from nltk.tag.stanford import StanfordNERTagger
import numpy as np
import wordninja
import spacy


def fix_sent(sent):
    """
    Remove title and lower case words and perform some basic cleaning.
    """
    sent = re.sub(r"([A-Z]+[a-z]+)|[a-z]+", "", sent)
    sent = re.sub(r"\s+", " ", sent).strip()
    sent = re.sub(r"\s[\.\,]", "", sent).strip()
    # Removing lone numbers
    sent = re.sub(r"\s+", " ", re.sub(r"\s[\d]{1}\s", " ", sent))
    return sent

def word_distance(words, word1, word2):
    """
    Number of words between word1 and word2
    """
    index_w1 = np.where(np.array(words) == word1)[0]
    index_w2 = np.where(np.array(words) == word2)[0]
    return index_w2 - index_w1

class ExtractNERs:

    def __init__(self, eng_zip_path="../stanford-ner-2018-02-27/english.all.3class.distsim.crf.ser.gz",
    ner_jar_path="../stanford-ner-2018-02-27/stanford-ner.jar", java_path='C:/Program Files/Java/jdk1.8.0_101/bin/'):

        # Downloads for NER tagger
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        
        # Set JAVA path
        nltk.internals.config_java(java_path)

        # Initialize NER tagger
        self.st = StanfordNERTagger(eng_zip_path, ner_jar_path)

        # Load spacy model
        self.nlp = spacy.load('en')

    
    def stanford_NE_extraction(self, sent):
        """
        Extract named entity words via Stanford NER tagger.
        :params st: Stanford NER tagger
        :params sent: list of words in the sentense
        """
        # Words in sent
        words = [word for word in word_tokenize(sent)]   
        # Extract tags
        tags = self.st.tag(words)
        # Temp varibales
        names = []
        prev_ind = -1
        name = ""
        # Extract words tagged as "PERSON" and only join if they are consecutive
        for ind, tag in enumerate(tags):
            if tag[-1] == "PERSON":
                # If previous word was person, concatenate the text
                if prev_ind == (ind - 1) or name == "":
                    name = (name + " " + tag[0]).strip()
                prev_ind = ind
                continue
            # If current word is not null and tag is not "PERSON" append the name to the list
            if name != '':
                names.append(name)
                name = ""

        # If name is at the end of the text
        if name != '':
            names.append(name)
        
        # Return the name with most words
        return [np.array(names)[np.argmax([len(x.split(" ")) for x in names])]] if len(names) > 0 else []

    def spacy_NE_extraction(self, sent):
        """
        Extract named entity words via spacy.
        :params sent: sentence from which named entity is to be extracted
        """
        # Process the sentence
        doc = self.nlp(sent)
        # Extract all the words with label "PERSON"
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        # print (names)
        return names

    def infer_spaces(self, sent):
        """
        Infer where space is to be added in a sentence and return the sentence with space inserted.
        :params sent: sentence with words where spaces should be present
        """
        
        # Process the sentence
        doc = self.nlp(sent)
        
        # Split the words
        for word in word_tokenize(sent):
            # Remove punctuations and numbers
            word = re.sub(r"[^A-Z0-9]", " ", word)
            word = re.sub(r"\s+", " ", word)
            # If word is less than 2 or a stop word, we don't split it
            if len(word) < 2 or word.lower() in stopwords.words("english") or len(re.findall(r"[A-Z]+", word)) == 0:
                continue
            # We split the word if wordnet does not return similar words and spacy can't tag it either
            if len([x.name() for x in wn.synsets(word.lower())]) == 0 and word not in [w.text for w in doc.ents]:
                splitted = [w for w in wordninja.split(word.lower())]

                # If a single character has been seperated, we re-attach it
                if len(splitted) > 1:
                    w = len(splitted) - 1
                    while w > 0:
                        if len(splitted[w]) == 1 and len(re.sub(r'\d+', "", splitted[w])) > 0:
                            splitted[w - 1] = splitted[w - 1] + splitted[w]
                            splitted.remove(splitted[w])
                        w -= 1
                # We select the split if length of the shortest splitted word is at least 2 and number of splits is greater than 1
                if len(splitted) > 1 and len(min(splitted, key=len)) > 2:
                    sent = sent.replace(word, " ".join(splitted).upper())

        return sent

    def extract_names(self, sent):
        """
        Extract names from sentence.
        :params sent: Sentence with names
        """
        spacy_words = 0
        stanford_words = 0
        # Do spacy extraction because it is faster than Stanford
        spacy_names = self.spacy_NE_extraction(sent)
        if len(spacy_names) == 1:
            spacy_words = len(spacy_names[0].split(" "))

        # If we found last, middle and first name
        if spacy_words == 3:
            return spacy_names[0]

        # Do Stanford extraction
        stanford_names = self.stanford_NE_extraction(sent)
        if len(stanford_names) == 1:
            stanford_words = len(stanford_names[0].split(" "))

        # If we found last, middle and first name or if number of words extracted are greater than spacy's
        if stanford_words == 3 or stanford_words > spacy_words:
            return stanford_names[0]
        elif spacy_words > 0:
            return spacy_names[0]
        return ""
        
    def perform_extraction(self, sent):
        """
        Perform NE extraction
        """
        extracted = []
        # Look for a person in each sentence of the text
        for s in sent_tokenize(sent):
            # Remove lower/title case words
            s = fix_sent(s)
            # Continue ff sentence is too short
            if len(s) < 3:
                continue
            # Infer spaces
            splitted_sent = self.infer_spaces(s)
            # Extract names
            names = self.extract_names(splitted_sent)

            if len(names) > 0:
                extracted.extend([names])

        return extracted


# if __name__ == "__main__":
#     sentences = ["TAL SECURIT SOCIALS CALLY 132-70-9008 THIS NUMBER HAS BEEN ESTABLISHED FOR ALICIA D. CLARKE Alicia tofanki SIGNATURE", # Works
#                 "SOCIAL SEC SECURITY HEALTH 078-52-4542 THIS MUSSEN HAS BEEN ESTABLISHED FOR NADJA FLOWER OGLVIN laukums, lai", # Works
#                 "SOCIAL SECURI 151-92-0554 THIS NUMBER HAS BEEN ESTABLISHED FORERICK HERRERA RODRIGUEZ SIGNATURE01/25/2018 USA", # Works
#                 # partially works
#                 "AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATON UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA ERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES 507-25-6801 THIS NUMBER HAS BEEN ESTABLISHED FOR KATE ALLYSONVIPPSTREUS Tatsuppheus mum USA CIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERIC SIGNATURE SIGNATURE 09/30/2010 A0000 muerte W VILTUM N ALULUNUMUNUN UNITED STATES OP AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OR SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY",
#                 # works
#                 "YOUR SOCIAL SECURITY CARD ADULTS: Sign this card in ink immediately. CHILDREN: Do not sign until age 18 or your first job, whichever is earlier. Keep your card in a safe place to prevent loss or theft. DO NOT CARRY THIS CARD WITH YOU. Do not laminate. AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL CURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES 069-78-6917 THIS NUMBER HAS BEEN ESTABLISHED FOR DEQUANNA ALLISON BROWN NISTRA AL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATUS GereSOCIAL SECURITY ADMINISTRATION M ED SIGNATURE SIGNATURE 07/25/2011 A HUOMIOTUM W 001001111 AND VOOS VOLVO SIVAS ON NOVUSINI",
#                 # works
#                 "YOUR SOCIAL SECURITY CARD ADULTS: Sign this card in ink immediately. CHILDREN: Do not sign until age 18 or your first job, whichever is earlier. Keep your card in a safe place to prevent loss or theft. DO NOT CARRY THIS CARD WITH YOU. Do not laminate. AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL CURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES 069-78-6917 THIS NUMBER HAS BEEN ESTABLISHED FOR DEQUANNA ALLISONBROWN NISTRA AL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATUS GereSOCIAL SECURITY ADMINISTRATION M ED SIGNATURE SIGNATURE 07/25/2011 A HUOMIOTUM W 001001111 AND VOOS VOLVO SIVAS ON NOVUSINI",
#                 # Works
#                 "YOUR SOCIAL SECURITY CARD ADULTS: Sign this card in ink immediately CHILDREN: Do not sign until age 18 or your first job, whichever is earlier Keep your card in a safe place to prevent loss or theft DO NOT CARRY THIS CARD WITH YOU Do not laminate VALID FOR WORK ONLY WITH DHS AUTHORIZATION497-69-3198 VE THIS NUMBER HAS BEEN ESTABLISHED FOR GIACOMO DOMENICONI SIGNATURE 05/19/2017 OVO SU ON OLLING OG",
#                 # Partially works
#                 "SECURITY 893-12-0381 THIS NUMRE HAS BEEN ESTABLISHED FORRAJIBURRAHMAN Vasan2015 SIGNATURE01/05/2015",
#                 # Partially works
#                 "SECURITY 893-12-0381 THIS NUMRE HAS BEEN ESTABLISHED FOR RAJI BUR RAHMAN Vasan2015 SIGNATURE01/05/2015",
#                 # Does not work
#                 "SECURIT SOCIAL SECU 663-39-1734 THIS NUMBER HAS BEEN ESTABLISHED FOR RIMA BEGUM RomaSIGNATURE TIS 01/05/2015",
#                 # Does not work
#                 "NAEROA SOCIAL SCOUNITY S OF AMERICA SOCIAL SECURITY ADMINISTRAT N UNITED STATETATE OF AMCAiOA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA CURIT RICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATE 154-80-7493 THIS NUMBER HAS BEEN ESTABLISHED FOR RUTH RITA 2 CENAT AL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMER SIGNATURE UMUM UNITED STATES OF AMERICA SOQIAL SECURITY ADMINISTRATION UNITED STATES OR MOTOM OTOROM USA 06/03/2010 | Anon SOCIAL SECURITY ADMINISTRATION UNITED STATES OF AMERICA SOCIAL SECURITYmummon",
#
#                 "OCIAL SECURITY 152-86-2670 THIS NUMBER HAS BEEN ESTABLISHED FOR VOLTA V COSTELLO SIGNATURE"]
#
#     ner = ExtractNERs()
#     for s in sentences:
#         print (s)
#         print (ner.perform_extraction(s))