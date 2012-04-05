import os
import string
import re
import pickle
from nltk.corpus import stopwords


# Build the corpus dictionary


# HELPER FUNCTIONS
punctre = re.compile('[%s]' % re.escape(string.punctuation))

def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

# walk the os using generators, put every email into a dict                     
def walk_os():
    for dirname, dirnames, filenames in os.walk('enron_mail_20110402'):
        for filename in filenames:
            yield os.path.join(dirname,filename)

def gen_open(filenames):
    for name in filenames:
        with open(name) as f:
            yield f.read().replace('\n',' ')

def strip_punct(files):
  for file in files:
    nopunct = punctre.sub('',file)
    yield nopunct

# Normalize ints by converting them all to '2', then build a dictionary
def build_dict(files,vocab):
  for file in files:
    for i in file.split():
      i=''.join('2' if is_int(j) else j for j in i).lower()
      print 'Updating %s' % i
      vocab[i] = vocab.setdefault(i,0)+1

def main():
  filenames = walk_os()
  opened_files = gen_open(filenames)
  stripped_files = strip_punct(opened_files)
  vocab = {}
  build_dict(stripped_files,vocab)
  sortedvocab = sorted(vocab.items(), key = lambda x: x[1],reverse=True)
  
  nostops = [i for i in sortedvocab if i[0] not in stopwords.words('english')]
  short = [i for i in nostops if len(i[0]<20]
  nocom = [i for i in short if 'com' not in i[0]]
  norare = [i for i in nocom if i[1]>5]
  nocommon = norare[40:]
  keys = [i[0] for i in nocommon]
  with open('dictnostops.txt', 'w') as f:
    for i in keys:
      f.write(i)
      f.write('\n')  

if __name__ == '__main__':
  main()
