# Copyright 2011 Nicolas Maupu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
## Package acm.parser
##
from HTMLParser import HTMLParser
from urllib2 import Request,urlopen,URLError
from core import LoadBalancer,Worker,Cluster,Server
from functional import curry
from configobj import ConfigObj
import re
import sys
from exceptions import SyntaxError

class BalancerManagerParser(HTMLParser):
  def __init__(self, srv, vhost):
    HTMLParser.__init__(self)
    self.lbs = []
    self.curtags = []
    self.reinit()
    self.curlb = None
    self.srv = srv
    self.vhost = vhost

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
      w = Worker(self.srv, self.vhost)
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

class ConfigParser():
  def __init__(self, filename):
    self.filename = filename

  def readConf(self):
    '''Read a configuration file (configobj format) and return a list of Clusters'''
    result = []
    config = ConfigObj(self.filename)

    clusters = self._getConfigValue(config, 'clusters')
    if not isinstance(clusters, list):
      raise SyntaxError('Configuration error [%s] - clusters is not a list. Add a coma to create one' % self.filename)

    for c in iter(self._getConfigValue(config, 'clusters')):
      cluster = Cluster()
      cluster.name = self._getConfigValue(config, c, 'name')
      #print ('Cluster found : %s' % cluster.name)

      for s in iter(self._getConfigValue(config, c, 'servers')):
        srv = Server()
        srv.ip = self._getConfigValue(config, s, 'ip')
        srv.port = self._getConfigValue(config, s, 'port')
        #print ('Server found : %s:%s' % (srv.ip, srv.port))
	##
	vhosts = self._getConfigValue(config, s, 'vhosts')
	if isinstance(vhosts, list):
	  ## If no vhost defined, switch to a default one
	  if len(vhosts) == 0: srv.add_vhost('')
          for vh in iter(self._getConfigValue(config, s, 'vhosts')):
            vhost_name = self._getConfigValue(config, vh, 'name')
            vhost_burl = self._getConfigValue(config, vh, 'burl')
            #print ('Vhost found : %s/%s' % (vhost_name, vhost_burl))
            srv.add_vhost(vhost_name, vhost_burl)
	else:
	  raise SyntaxError('Configuration error [%s] - [%s].vhosts is not a list. Add a coma to create one' % (self.filename, s))

        cluster.servers.append(srv)

      ## Appending cluster object to returned result
      result.append(cluster)
    return result

  def _getConfigValue(self, config, *keys):
    ret = config
    try:
      for k in iter(keys):
        ret = ret[k]
    except KeyError:
      return []
    return ret

def fetch_balancer_manager_page(srv, vhost=None):
  vh = vhost
  if vh == None:
    vh = VHost() ## Create a default vhost
    
  try:
    req = Request('http://%s:%s/%s' % (srv.ip, srv.port, vh.balancerUrlPath))
    if vh.name != '': req.add_header('Host', vh.name)
    r = urlopen(req)
    return r.read()
  except URLError, e:
    #print ('Error occured [%s:%s] - %s' % (srv.ip, srv.port, e.reason))
    raise

def process_server_vhost(srv, vhost):
  try:
    b=BalancerManagerParser(srv, vhost)
    page=fetch_balancer_manager_page(srv, vhost)
    b.feed(page)
    vhost.lbs = b.lbs
  except Exception, e:
    #print "hohohoho - %s" % e
    srv.error=True

