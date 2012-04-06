import logging, gensim, bz2

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
  
  # load id->word mapping (the dictionary), one of the results of step 2 above
  id2word = gensim.corpora.Dictionary.load_from_text('enron_wordids.txt')

  # load corpus iterator
  mm = gensim.corpora.MmCorpus('enron_tfidf.mm')
  print mm

  # extract 50 LDA topics, using 1 pass and updating once every 1 chunk (1,000 documents)
  lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=100, update_every=1, chunksize=1000, passes=1)
  lda.save('enron_lda100.pkl')
  lda.print_topics(100)

 
