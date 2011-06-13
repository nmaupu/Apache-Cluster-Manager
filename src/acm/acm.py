## Package acm.acm
##
from core import *
from parser import *
from urllib2 import URLError
from optparse import OptionParser, OptionGroup

parser = OptionParser()
group = OptionGroup(parser, 'Configuration options')
group.add_option('-a', '--add', dest='add', action='store_true', default=False, \
  help='Add a server to configuration')
group.add_option('-s', '--server', dest='server', \
  help='Server ip or address')
group.add_option('-p', '--port', dest='port', default='80', type='int', \
  help='Server port')
group.add_option('-v', '--vhost', dest="vhost", default='', \
  help='Virtual host name to connect to')
group.add_option('-b', '--burl', dest='burl', default='balancer-manager', \
  help='Url path to reach balancer manager')
group.add_option('-c', '--cluster', dest='cluster', \
  help='Cluster name')
parser.add_option_group(group)

(opts, args) = parser.parse_args()

if opts.add:
  if opts.server and opts.cluster:
    print ('from acm.core import *')
    print ('s1 = Server()')
    print ('s1.ip = "%s"' % opts.server)
    print ('s1.port = "%s"' % opts.port)
    print ('s1.add_vhost("%s")' % opts.vhost)
    print ('clu1 = Cluster()')
    print ('clu1.name = "%s"' % opts.cluster)
    print ('clu1.servers.append(s1)')
  else:
    print ('Specify a server and a cluster name, try --help for more information')


#####
#def readConf(filename, globals):
#  execfile(filename, dict(), gdict)
#
#gdict = dict()
#readConf('./acm/acm.conf', gdict)
#
#cluster = None
#for i in iter(gdict):
#  try:
#    o = gdict[i]
#    if isinstance(o, Cluster):
#      cluster = gdict[i]
#  except:
#    pass
#
##print cluster
##for srv in iter(cluster.servers):
##  print srv
#
#
## testing
#for srv in iter(cluster.servers):
#  for vh in iter(srv.vhosts):
#    b    = BalancerManagerParser()
#    try:
#      page = fetch_balancer_manager_page(srv.ip, srv.port, vh.name, vh.balancerUrlPath)
#      b.feed(page)
#      vh.lbs = b.lbs[:]
#    except URLError, e:
#      srv.error = True
#    except:
#      pass
#
#for srv in iter(cluster.servers):
#  print(srv)
#  for vh in iter(srv.vhosts):
#    print(vh)
#    for lb in iter(vh.lbs):
#      print (lb)
#      for w in iter(lb.workers):
#        print (w)
