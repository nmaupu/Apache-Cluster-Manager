## Package acm.acm
##
from core import *
from utils import *
from urllib2 import URLError

def readConf(filename, globals):
  execfile(filename, dict(), gdict)

gdict = dict()
readConf('./acm/acm.conf', gdict)

cluster = None
for i in iter(gdict):
  try:
    o = gdict[i]
    if isinstance(o, Cluster):
      cluster = gdict[i]
  except:
    pass

#print cluster
#for srv in iter(cluster.servers):
#  print srv


# testing
for srv in iter(cluster.servers):
  for vh in iter(srv.vhosts):
    b    = BalancerManagerParser()
    try:
      page = fetch_balancer_manager_page(srv.ip, srv.port, vh.name, vh.balancerUrlPath)
      b.feed(page)
      vh.lbs = b.lbs[:]
    except URLError, e:
      srv.error = True
    except:
      pass

for srv in iter(cluster.servers):
  print(srv)
  for vh in iter(srv.vhosts):
    print(vh)
    for lb in iter(vh.lbs):
      print (lb)
      for w in iter(lb.workers):
        print (w)
