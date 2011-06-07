## Package acm.parser
##
from HTMLParser import HTMLParser
from urllib2 import Request,urlopen
from core import LoadBalancer,Worker
import re

class BalancerManagerParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.reinit()

  def handle_starttag(self, tag, attrs):
    if tag == 'hr':
      self.reinit()
    self.curtags.append(tag)
    self.attrs = attrs
    if tag == 'h3':
      lb = LoadBalancer()
      self.curlb = lb
      self.lbs.append(lb)
    elif tag == 'table':
      self.tables += 1
      if self.tables == 2:
        w = Worker()
        self.curworker = w
        self.curlb.append(w)
    elif tag == 'th' and self.tables == 1:
      pass
    elif tag == 'th' and self.tables == 2:
      pass
    elif tag == 'td' and self.tables == 2:
      pass

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
      setattr(self.curlb, dataValue, '')
    elif self.get_curtag() == 'th' and self.tables == 2:
      setattr(self.curworker, dataValue, '')

  def get_curtag(self):
    if len(self.curtags) > 0:
      return self.curtags[-1]
    else:
      return None

  def reinit(self):
    self.tables = 0
    self.curtags = []
    self.attrs = ''
    self.lbs = []
    self.curlb = None
    self.curworker = None


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
b=BalancerManagerParser()
page=fetch_balancer_manager_page('127.0.0.1')
b.feed(page)
print b.lbs
