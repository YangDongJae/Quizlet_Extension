import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from datetime import datetime
import re

class Crawling():
  def __init__(self):
    print(pd.__version__)
    self.name = None
    self.cont = None

  def set_word(self, vocab):
    self.name = vocab
    res = requests.get("https://dictionary.cambridge.org/dictionary/english/{}".format(self.name), headers = {"User-Agent":'Mozilla/5.0'})
    self.cont = bs(res.content, 'html.parser')

  def get_defi(self):
    defi = self.cont.find('div', class_='def ddef_d db').text
    return defi

  def get_POS(self):
    POS = POS = self.cont.find('span', class_='pos dpos').text
    return POS

  def get_example(self):
    example_list = []
    for example in self.cont.find_all('span', class_= 'eg deg'):
      example_list.append(example.text)
    
    return example_list
  
  def change_vocab_list(self, word):
    res = requests.get("https://dict.naver.com/search.dict?dicQuery={}&query=Instuitution&target=dic&ie=utf8&query_utf=&isOnlyViewEE=".format(word), headers = {"User-Agent":'Mozilla/5.0'})
    cont = bs(res.content, 'html.parser')
    new_word = cont.find('span', class_="c_b").text

    return new_word


class Main():
  def __init__(self):
    self.craw = Crawling()
    self.vocab_lst = list(pd.read_excel('/Users/yangdongjae/Desktop/2022/Project/Extesion of Quizlet/input.xlsx')["Table 1"])
    self.word = []
    self.defi = []
    self.POS = []
    self.examples = []
    self.cont = []

  def clean_example(self, word, exam):
    for i in range (len(exam)):
      if word in exam[i]:
        exam[i] = re.sub(word, "____", exam[i])
    return exam


  def run(self):
    for word in self.vocab_lst:
      # print(word)
      self.craw.set_word(word)
      self.word.append(word)
      
      try:
        self.defi.append(self.craw.get_defi())
        self.POS.append(self.craw.get_POS())
        self.examples.append(self.craw.get_example())
        

      except:
        self.defi.append('-')
        self.POS.append('-')
        self.examples.append('-')
    
    vocab = {
      'word' : self.word,
      'POS' : self.POS,
      'definition' : self.defi,
      'examples' : self.examples
    }

    res = pd.DataFrame(vocab)
    res.to_excel('Voca/{}_VOCA.xlsx'.format(datetime.today().strftime('%Y%m%d_')))


# Quizlet form 에 맞춘 형식개발 필요
## (POS)
## Example ( , 기준 줄바꿈 [] 제거 )
## 단어 뜻
# go with 안됨
# Criteria 안됨
x = Main()
x.run()