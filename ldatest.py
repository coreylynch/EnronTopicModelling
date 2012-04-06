import logging, gensim, bz2, numpy, os
from pymongo import Connection
from pymongo.errors import ConnectionFailure
import sys

# HELPER FUNCTIONS
ARTICLE_MIN_CHARS = 500
def walk_os(root):
  for dirname, dirnames, filenames in os.walk(root):
    for filename in filenames:
      yield os.path.join(dirname,filename)

def gen_open(filenames):
  for name in filenames:
    with open(name) as f:
      yield f.read()

if __name__ == '__main__':

  # check and process input arguments
  # Example: 'ipython ldatest.py enron_mail_20110402 enron_lda50batch.pkl enron_tfidf.mm enron emails_with_dates'
  # would use the batch 50 topic model, tfidf reprs, and insert into a new collection
  input, model, tfidf,  database, collection = sys.argv[1:6]
  
  # Connect to Mongo                                                   
  try:
    c = Connection(host="localhost", port=27017)
    print "Connected successfully"
  except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)
  db = c[database]

  # Load the tf-idf vectors of emails
  mm = gensim.corpora.MmCorpus(tfidf)

  # Load the lda model
  lda = gensim.models.ldamodel.LdaModel.load(model)

  # Walk the file system, classify each email, store each email in mongo with it's corresponding topic
  filenames = walk_os(input)
  opened_files = gen_open(filenames)
  
  index = 1 # Start from index 1 to skip the first document, which isn't an email and has no date  
  for email in opened_files:
    if len(email) > ARTICLE_MIN_CHARS:
      topic = numpy.argmax(lda.inference([mm[index]])[0])
      (month,year)=email.split('\r')[1].split()[3:5]
      email_with_topic = {'index':str(index),
                          'email': unicode(email,
                          'utf-8', errors='ignore'),
                          'topic': str(topic),
                          'month': str(month),
                          'year': str(year)}
      db.collection.insert(email_with_topic, safe=True)
      print ' INFO : Email: %i, Topic: %i, Mon: %s, Yr: %s' % (index,topic,month,year)
      index +=1


