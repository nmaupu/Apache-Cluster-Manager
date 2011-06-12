## Package acm.parser
##
from HTMLParser import HTMLParser
from urllib2 import Request,urlopen
from core import LoadBalancer,Worker
import re

class BalancerManagerParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.lbs = []
    self.curtags = []
    self.reinit()
    self.curlb = None

  def handle_starttag(self, tag, attrs):
    self.curtags.append(tag)
    self.attrs = attrs
    if tag == 'hr':
      self.reinit()
    elif tag == 'table':
      self.tables += 1
    elif tag == 'h3':
      lb = LoadBalancer()
      self.curlb = lb
      self.lbs.append(lb)
    elif tag == 'tr' and self.tables == 1:
      self.lbptr = -1
    elif tag == 'tr' and self.tables == 2 and len(self.wattrs) > 0:
      self.wptr = -1
      w = Worker()
      self.curworker = w
      self.curlb.workers.append(w)
    elif tag == 'td' and self.tables == 1:
      self.lbptr += 1
    elif tag == 'td' and self.tables == 2:
      self.wptr += 1
    elif tag == 'a' and self.tables == 2:
      self.curworker.actionURL = self.attrs[0][1]

  def handle_endtag(self, tag):
    try:
      self.curtags.pop()
    except:
      pass

  def handle_data(self, datap):
    ## Triming data value
    data = datap.strip(' ')
    dataValue = data.replace(' ', '_')
    
    if self.get_curtag() == 'h3':
      r = re.compile('^LoadBalancer Status for balancer://(.*)$')
      str = r.search(data).group(1)
      self.curlb.name = str
    elif self.get_curtag() == 'th' and self.tables == 1:
      self.lbattrs.append(dataValue)
    elif self.get_curtag() == 'th' and self.tables == 2:
      self.wattrs.append(dataValue)
    elif self.get_curtag() == 'td' and self.tables == 1:
      attr = self.lbattrs[self.lbptr]
      setattr(self.curlb, attr, dataValue)
    elif self.get_curtag() == 'td' and self.tables == 2:
      attr = self.wattrs[self.wptr]
      setattr(self.curworker, attr, dataValue)
    elif self.get_curtag() == 'a' and self.tables == 2:
      attr = self.wattrs[self.wptr]
      setattr(self.curworker, attr, dataValue)

  def get_curtag(self):
    try:
      return self.curtags[-1]
    except:
      return None

  def reinit(self):
    self.tables = 0
    self.attrs = ''
    self.lbattrs = []
    self.wattrs  = []
    self.lbptr = -1
    self.wptr  = -1


def fetch_balancer_manager_page(ip, port='80', vhost_name='', urlpath='balancer-manager'):
  try:
    req = Request('http://%s:%s/%s' % (ip, port, urlpath))
    req.add_header('Host', vhost_name)
    r = urlopen(req)
    return r.read()
  except:
    print ("Error occured - %s" % sys.exc_info()[0])
    raise


## testing
#b=BalancerManagerParser()
#page=fetch_balancer_manager_page('127.0.0.1')
#b.feed(page)
#
#for i in range (len(b.lbs)):
#  lb = b.lbs[i]
#  print (lb.toString())
#  for j in range (len(lb.workers)):
#    w = lb.workers[j]
#    print (w.toString())
