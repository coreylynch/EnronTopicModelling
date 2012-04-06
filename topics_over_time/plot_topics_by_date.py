import matplotlib.pyplot as plt
import datetime
import matplotlib
import numpy
from pymongo import Connection
from pymongo.errors import ConnectionFailure
from datetime import datetime

if __name__ == '__main__':

  # Connect to Mongo                                                            
  try:
    c = Connection(host="localhost", port=27017)
    print "Connected successfully"
  except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)
  db = c['enron']
  
  # Build date vector
  format = '%b %Y'
  months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  years = [str(i) for i in range(1999,2003)]
  dates = []
  for i in years:
    for j in months:
      dates.append(datetime.strptime(j+' '+i,'%b %Y'))
  dates = sorted(dates)

  # Build partition count vector
  #totals = []
  #for date in dates:
   # (month,year)=date.strftime('%b %Y').split()
    #total = db.emails50batch_with_dates.find({'month':month,'year':year}).count()
    #totals.append(total)

  # Plot normalized topic frequency over time for each topic, write to disk
  for topic in xrange(0,51):
    # Build topic-specific count vector
    print 'Building topic-specific count vector for topic %i' % topic 
    counts = []
    for date in dates:
      (month,year)=date.strftime('%b %Y').split()
      count = db.emails50batch_with_dates.find({'topic':str(topic),'month':month,'year':year}).count()
      counts.append(count)

   
    # Normalize the count vector
    #normalized_counts = numpy.divide(counts,totals)

    # Plot the topics over time, save the graph
    print 'Plotting...'
    plt.plot_date(dates,counts,linestyle='-',xdate=True,ydate=False)
  
    plt.xlabel('Time')
    plt.ylabel('Topic Frequency')
    plt.title('Topic '+str(topic)+' Over Time')
    print 'Saving figure to disk...'
    plt.savefig('topic_'+str(topic)+'_over_time.png')
    plt.clf()

