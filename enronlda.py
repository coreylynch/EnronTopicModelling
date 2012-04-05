import cPickle, string, numpy, getopt, sys, random, time, re, pprint
import onlineldavb
import os 

# HELPER FUNCTIONS                                                              
punctre = re.compile('[%s]' % re.escape(string.punctuation))

def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

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


def main():
  
  batchsize=10
  D = 500000
  K = 50

  if (len(sys.argv) < 2):
    documentstoanalyze = int(D/batchsize)
  else:
    documentstoanalyze = int(sys.argv[1])

  # Our vocabulary
  vocab = file('./dictnostops.txt').readlines()
  W = len(vocab)
  # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
  olda = onlineldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.7)
  
  #Loop over every doc in the collection and update lambdas
  filenames = walk_os()
  opened_files = gen_open(filenames)
  stripped_files = strip_punct(opened_files)
  counter = 0
  for f in stripped_files:
    counter+=1
    print 'Iteration %i' % counter
    docset = []
    f = ''.join('2' if is_int(j) else j for j in f).lower()
    docset.append(f)
    (gamma, bound) = olda.update_lambda(docset)
    #(wordids, wordcts) = onlineldavb.parse_doc_list(docset, olda._vocab)
    #perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
    #print '%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
    #(iteration, olda._rhot, numpy.exp(-perwordbound))

    if (counter % 100 == 0):
      numpy.savetxt('lambda-%d.dat' % counter, olda._lambda)
      numpy.savetxt('gamma-%d.dat' % counter, gamma)

if __name__ == '__main__':
  main()
