# -*- coding: utf-8 -*-
"""
Created on 8.08.2024

@author: Dannya Chami
"""

import zeyrek
import sqlite3

from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from zemberek.morphology import TurkishMorphology
from zemberek.morphology.analysis.single_analysis import SingleAnalysis


from nltk.collocations import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder

import logging


#nltk.download('all')

#Kelimeler hakkında detaylı bir morfolojik analiz yapacağım için morfoloji nesnesi oluşturuyorum.

morphology = TurkishMorphology.create_with_defaults()

turkish_stopwords = stopwords.words('turkish')
turkish_stopwords.extend(['sayesinde', 'yapılan', 'almak', 'yoluyla', 'açısından', 'temelini','oluşturur', 'katkı', 'boyu', 'yerine', 'bulunur', 'sahip', 'süren', 'şekilde', 'alanındaki', 'dar', 'destekli', 'genel', 'ayrıca', 'getirdiği', 'rol', 'oynar', 'sadece', 'ötesine', 'geçerek', 'birçok', 'aynı', 'eder', 'alan', 'alır', 'alanın', 'kat',  'bir', 'iki', 'haline', 'birer', 'kadar', 'gibi', 'gelmiştir', 'olarak', 'sunar', 'olur', 'getirir', 'biridir', 'temel', 'alan' ])
analyzer = zeyrek.MorphAnalyzer()


logging.getLogger('zeyrek').setLevel(logging.ERROR)

logging.getLogger('gensim').setLevel(logging.ERROR)

def create_word_pairs(words):
    pairs = []
    for i in range(len(words) - 1):
        pairs.append((words[i], words[i + 1]))
    return pairs

def filter_similar_elements(elements):
    
    filtered_elements = []

    for i in range(len(elements)):
        keep = True
        for j in range(len(filtered_elements)):
            if similarity_ratio(elements[i], filtered_elements[j]) > 0.6:
                keep = False
                break
        if keep:
            filtered_elements.append(elements[i])

    return filtered_elements


def similarity_ratio(pair1, pair2):
    
    str1 = ''.join(pair1).lower()
    str2 = ''.join(pair2).lower()

  
    shorter_length = min(len(str1), len(str2))

    # Calculate the number of matching characters
    matches = sum(1 for a, b in zip(str1, str2) if a == b)

    return matches / shorter_length if shorter_length > 0 else 0

def find_alike_pairs(pairs):
    # Create a dictionary to hold pairs by their lowercase representation
    pair_dict = {}

    for pair in pairs:
        lower_pair = (pair[0].lower(), pair[1].lower())
        if lower_pair in pair_dict:
            pair_dict[lower_pair].append(pair)
        else:
            pair_dict[lower_pair] = [pair]

    # Create a list to store the final pairs with counts
    final_pairs = {}

    for key, values in pair_dict.items():
        if len(values) > 1:
            # If there are multiple occurrences, check for similarity
            for i in range(len(values)):
                for j in range(i + 1, len(values)):
                    if similarity_ratio(values[i], values[j]) >= 0.6:
                        # Increment the occurrence of the shorter pair
                        shorter_pair = values[i] if len(values[i]) < len(values[j]) else values[j]
                        if shorter_pair in final_pairs:
                            final_pairs[shorter_pair] += 1
                        else:
                            final_pairs[shorter_pair] = 1

    return final_pairs

def dict_to_list(pair_dict):
    
    pair_list = []
    for pair, count in pair_dict.items():
        pair_list.append(pair[0] + ' ' + pair[1])
    return pair_list


def check_word_similarity(word1, word2):
   
    word1 = word1.lower()
    word2 = word2.lower()
   
    max_length = max(len(word1), len(word2))
   
    common_letters = 0
    for i in range(max_length):
        if i < len(word1) and i < len(word2) and word1[i] == word2[i]:
            common_letters += 1
   
    similarity_score = common_letters / max_length
    return similarity_score


def remove_similar_words(words, similarity_threshold=0.5):
    result = []
    for i in range(len(words)):
       for j in range(i+1, len(words)):
        if(check_word_similarity(words[i], words[j])>0.45):
         pass


def get_pos(word):
  global morphology
  analiz = morphology.analyze(word)
  if analiz.analysis_results:
        string = str(analiz.analysis_results[0])
        if '→' in string:
          #print('yes')
          index1=string.index('→')
          if '|' in string and string.index('|')>index1:
            index2=string.index('|')
            string2=string[index1+1:index2]
            return(string2)
          elif '+' in string and string.index('+')>index1:
            index2=string.index('+')
            string2=string[index1+1:index2]
            return(string2)
          else:
            string2=string[index1+1:]
            return string2
        else:
          first_index = int(string.find(':'))
          second_index = int(string.find(':', first_index + 1))
          third_index=int(string.find('+'))
          string3=string[second_index+1: third_index]
          if(string3):
            return string3
          else:
            return('unknown')

  else:
    return('unknown')


def sohbet_genel_konu(konular):
    genel_konu=""
    vowels = set('aeiouıüö')
    ketcap= set('ktçp')
  
    if (get_pos(konular[0])=='Noun' or len(konular[0].split())>1 or get_pos(konular[0])=='Verb') :
         
     if(konular[0].endswith('mak') or konular[0].endswith('mek')):
       konular[0]=konular[0][:-1]
            
     if konular[0][-1] in vowels:
        var=find_last_vowel(konular[0])
        if(var==1):
            gecici=konular[0]+'sı'
        elif(var==2):
            gecici=konular[0]+'si'
        elif(var==3):
            gecici=konular[0]+'su'
        elif(var==4):
            gecici=konular[0]+'sü'
     else:
        if konular[0][-1] in ketcap:
            if konular[0][-1] == 'k':
                konular[0] = konular[0][:-1] + 'ğ'
            elif konular[0][-1] == 'p':
                konular[0] = konular[0][:-1] + 'b'
            elif konular[0][-1] == 'ç':
                konular[0] = konular[0][:-1] + 'c'
            elif konular[0][-1] == 't':
                konular[0] = konular[0][:-1] + 'd'
                
        var=find_last_vowel(konular[0])
        if(var==1):  
            gecici=konular[0]+'ı'
        elif(var==2):
            gecici=konular[0]+'i'
        elif(var==3):
            gecici=konular[0]+'u'
        elif(var==4):
            gecici=konular[0]+'ü'
    

     genel_konu=konular[1]+" "+gecici
    
    else:
     genel_konu=konular[1]+" "+konular[0]
        
    
    if len(konular)==2 :
        return genel_konu
    elif len(konular)==3 :
        genel_konu=konular[2]+" hakkında "+genel_konu
        return genel_konu
    elif len(konular)==4:
        if (get_pos(konular[2])=='Noun' or len(konular[2].split())>1) or get_pos(konular[2])=='Verb':
            if(konular[2].endswith('mak') or konular[2].endswith('mek')):
              konular[2]=konular[2][:-1]
              
            if konular[2][-1] in vowels:
                var=find_last_vowel(konular[2])
                if(var==1):
                    gecici=konular[2]+'sı'
                elif(var==2):
                    gecici=konular[2]+'si'
                elif(var==3):
                    gecici=konular[2]+'su'
                elif(var==4):
                    gecici=konular[2]+'sü'
            else:
                if konular[2][-1] in ketcap:
                    if konular[2][-1] == 'k':
                        konular[2] = konular[2][:-1] + 'ğ'
                    elif konular[2][-1] == 'p':
                        konular[2] = konular[2][:-1] + 'b'
                    elif konular[2][-1] == 'ç':
                        konular[2] = konular[2][:-1] + 'c'
                    elif konular[2][-1] == 't':
                        konular[2] = konular[2][:-1] + 'd'
                        
                var=find_last_vowel(konular[2])
                if(var==1):  
                    gecici=konular[2]+'ı'
                elif(var==2):
                    gecici=konular[2]+'i'
                elif(var==3):
                    gecici=konular[2]+'u'
                elif(var==4):
                    gecici=konular[2]+'ü'
                    
            genel_konu=konular[3]+" "+gecici+" hakkında "+genel_konu
            return genel_konu
        else:
            genel_konu=konular[3]+" "+konular[2]+" hakkında "+genel_konu
            return genel_konu    
        
        
    

def find_last_vowel(word):
   
    vowels = set('aeiouıüö')
    reversed_word=word[::-1]

   
    for char in reversed_word.lower():
        
        if char in vowels:
          if ((char=='a') or (char=='ı')):
            return 1
          elif ((char=='e') or (char=='i')):
            return 2
          elif ((char=='o') or (char=='u')):
            return 3
          elif ((char=='ü') or (char=='ö')):
            return 4


def obtain_lemma(word):
    global analyzer
    lemmas = analyzer.lemmatize(word)
    if word.endswith(('nun', 'nin', 'nün', 'nın', 'dir', 'dur', 'dır', 'dür', 'da', 'de', 'ini', 'ını', 'unu', 'ünü', 'ar', 'ur', 'er', 'ür', 'yü', 'yi', 'yu','yı', 'ın', 'in', 'un', 'ün' )) and word!='sorun' :
        if(len(lemmas[0][1])==1) :
          return lemmas[0][1][0]
        elif(len(lemmas[0][1])>1) :
          for i in range(len(lemmas[0][1])):
            if(lemmas[0][1][i][0]).islower():
              return lemmas[0][1][i]
              break
    else:
        return word

topic_1_words=[]
main_topic=''

#------------------MAIN_TOPICS---------------------------------------------------

def obtain_main_topic(metin):

  cumleler = sent_tokenize(metin, language='turkish')
  kelimeler= [word_tokenize(cumle.lower()) for cumle in cumleler]
  # print(cumleler)
  # print(kelimeler)
  global turkish_stopwords
  temiz_kume=[ [kelime for kelime in cumle if kelime.isalpha() and kelime not in turkish_stopwords] for cumle in kelimeler]
  # print(temiz_kume)
  temiz_kume2=[]
  for cumle in temiz_kume:
   for kelime in cumle:
    temiz_kume2.append(kelime)

  # print(temiz_kume2)
  global analyzer
  sonuc = [[analyzer.lemmatize(kelime) for kelime in sentence] for sentence in temiz_kume]
  # print(sonuc)
  new_list = [[obtain_lemma(kelime) for kelime in sentence] for sentence in temiz_kume]
  dictionary = Dictionary(new_list)

# Create a corpus from the document
  corpus = [dictionary.doc2bow(text) for text in new_list]
# Build the LDA model
  lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=1, passes=50, iterations=200)

  # Get the topic words for the first topic (index 0)
  topic_words = lda_model.get_topic_terms(topicid=0, topn=10)
  # Convert the topic words to a list of words
  global topic_1_words
  topic_1_words= [dictionary[word_id[0]] for word_id in topic_words]

  # print('ok')
  # print(topic_1_words)

  for i, word in enumerate(topic_1_words):
   if ('ler' in word) and ( 'Verb' not in get_pos(word)):
      index3=word.index('ler')
      new_word=word[:index3+3]
      topic_1_words[i] = new_word

   elif ('lar' in word) and ('Verb' not in get_pos(word)):
      index4=word.index('lar')
      new_word=word[:index4+3]
      topic_1_words[i] = new_word

  # print(topic_1_words)

  for i, word in enumerate(topic_1_words):
    if ('Ad' in get_pos(word)) :
        last_vowel = find_last_vowel(word)
        if last_vowel == 1:
            topic_1_words[i] = word + 'lık'
        elif last_vowel == 2:
            topic_1_words[i] = word + 'lik'
        elif last_vowel == 3:
            topic_1_words[i] = word + 'luk'
        elif last_vowel == 4:
            topic_1_words[i] = word + 'lük'
    elif  'Verb' in get_pos(word):
        if (('mak' not in word) or ('mek' not in word)) and word.endswith(('er', 'ur', 'ar', 'ür','ır', 'ir', 'iyor', 'uyor', 'ıyor', 'üyor',  )):
            analiz = morphology.analyze(word)
            string=str(analiz.analysis_results[0])
            index1=string.index('[')
            index2=string.index(':')
            topic_1_words[i] = string[index1+1:index2]


  # print('the words now are : ')
  # print(topic_1_words)

  global main_topic

  for i in range(3):
    if topic_1_words[i] == kelimeler[0][0] or check_word_similarity(topic_1_words[i], kelimeler[0][0])>=0.5:
      main_topic=topic_1_words[i]
      break;
    else:
      main_topic=topic_1_words[0]

  return main_topic

#------------------SUB_TOPICS---------------------------------------------------


def obtain_sub_topics(text):

  global turkish_stopwords

  # a_list=text.lower().split()

  # print(a_list)
  # a_list= [kelime for kelime in a_list if kelime not in turkish_stopwords]

  cumleler = sent_tokenize(text, language='turkish')
  kelimeler= [word_tokenize(cumle.lower()) for cumle in cumleler]
  # print(cumleler)
  # print(kelimeler)
  global turkish_stopwords
  temiz_kume=[ [kelime for kelime in cumle if kelime.isalpha() and kelime not in turkish_stopwords] for cumle in kelimeler]
  # print(temiz_kume)
  a_list=[]
  for cumle in temiz_kume:
   for kelime in cumle:
    a_list.append(kelime)
  #print(a_list)
  
  global topic_1_words
  global main_topic


  bigram_measures = BigramAssocMeasures()

  #We allow ony adjacent words to be collocated words
  finder = BigramCollocationFinder.from_words(a_list)

  #We then look for words that appear together 2 times or more
  finder.apply_freq_filter(2)
  
  all_bigrams=finder.ngram_fd.items()
  
  collocations_3_times = [bigram for bigram, freq in all_bigrams if freq >=4]
  
  collocations_3_times_strings = [" ".join(bigram) for bigram in collocations_3_times]


  #We apply this measure below and show the top 5 collocated tokens (occuring in a window of 2 tokens with a frequency of 2 or more)

  top_collocations = finder.nbest(bigram_measures.likelihood_ratio, 5)
  # Now 'top_collocations' contains the collocations
  #print(top_collocations)

  first_col_sayi=len(top_collocations)

  alt_konular=[]

  for tup in top_collocations:
    if tup[0][::-1][0]==',' or tup[0][::-1][0]=='.' or tup[0][::-1][0]==';':
      continue;
    elif tup[1][0]==',' or tup[1][0]=='.' or tup[1][0]==';':
      continue;
    else:
      alt_konular.append(tup)

  alt_konular=[[konu for konu in alt_konu] for alt_konu in alt_konular]

  for i,alt_konu in enumerate(alt_konular):
    if len(alt_konular[i])>1:
      alt_konular[i]=alt_konular[i][0]+' '+ alt_konular[i][1]

  
  # print(topic_1_words)

  for topic in topic_1_words:
    if topic!=main_topic and not(topic in main_topic or main_topic in topic):
     alt_konular.append(topic)

  for i, alt_konu in enumerate(alt_konular):
   if alt_konu.endswith(('dir', 'dur', 'dır', 'dür' )):
    alt_konular[i]=alt_konular[i][:-3]

  #print(a_list)

  a_list=[obtain_lemma(word) for word in a_list]

  #print(a_list)

  pairs=create_word_pairs(a_list)
  alike_pairs = find_alike_pairs(pairs)
  pair_list = dict_to_list(alike_pairs)

  #print(pair_list)

  for pair in pair_list:
    for alt_konu in alt_konular:
      if similarity_ratio(pair, alt_konu )>=0.4:
        break
      else:
        alt_konular.insert(first_col_sayi, pair)
        break

  #print(alt_konular)

  alt_konular=filter_similar_elements(alt_konular)
  
  if 'almak' in alt_konular:
      alt_konular.remove('almak')
  

  if len(collocations_3_times_strings)>=1:
      if collocations_3_times_strings[0] in alt_konular:
          #print("yes")
          index=alt_konular.index(collocations_3_times_strings[0])
          gecici=main_topic
          main_topic=collocations_3_times_strings[0]
          #print("main topic now")
          #print(main_topic)
          alt_konular[index]=gecici
      
  
  
  return alt_konular, main_topic























