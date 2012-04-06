import logging, gensim, bz2, sys

"""
Trains and saves a batch or online LDA model for a specified number of topics.
Example: 'ipython enronlda.py 100 batch' will build a batch LDA model with 100 topics
"""

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
  
  # load id->word mapping (the dictionary), one of the results of step 2 above
  id2word = gensim.corpora.Dictionary.load_from_text('enron_wordids.txt')

  # load corpus iterator
  mm = gensim.corpora.MmCorpus('enron_tfidf.mm')
  print mm

  num_topics = sys.argv[0]
  
  if sys.argv[1] == 'batch':
    type = 'batch'
    passes = 20
    update_every = 0
    lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=num_topics, update_every=update_every, passes=passes)
  else:
    type = 'online'
    passes = 1
    update_every = 1
    lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=num_topics, update_every=update_every, chunksize=1000, passes=passes)
    
  lda.save('enron_lda'+str(num_topics)+type+'.pkl')
  lda.print_topics(num_topics)

 
