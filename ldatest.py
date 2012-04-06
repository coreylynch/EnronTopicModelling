import logging, gensim, bz2, numpy, os
from pymongo import Connection
from pymongo.errors import ConnectionFailure

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

  # Connect to Mongo                                                            
  try:
    c = Connection(host="localhost", port=27017)
    print "Connected successfully"
  except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)
  db = c['enron']


  # Load the tf-idf vectors of emails
  mm = gensim.corpora.MmCorpus('enron_tfidf.mm')

  # Load the lda model
  lda = gensim.models.ldamodel.LdaModel.load('enron_lda100.pkl')

  # Walk the file system, classify each email, store each email in mongo with it's corresponding topic
  filenames = walk_os('enron_mail_20110402')
  opened_files = gen_open(filenames)
  
  index = 0  
  for email in opened_files:
    if len(email) > ARTICLE_MIN_CHARS:
      topic = numpy.argmax(lda.inference([mm[index]])[0])
      email_with_topic = {'email':email,'topic':str(topic)}
      db.emails.insert(email_with_topic, safe=True)
      print 'Inserted email %i with topic %i' % (index,topic)
      index +=1


