## Package acm.core
## Core objects for Apache Cluster Manager project
from termcolor import colored

class Worker:
  """apache Load Balancer Worker class"""
  def __init__(self):
    self.actionURL = ''
    self.Worker_URL = ''
    self.Route = ''
    self.RouteRedir = ''
    self.Factor = ''
    self.Set = ''
    self.Status = ''
    self.Elected = ''
    self.To = ''
    self.From = ''
  
  def __str__(self):
    return '  Worker: Worker_URL=%s, Route=%s, RouteRedir=%s, Factor=%s, Set=%s, Status=%s, Elected=%s, To=%s, From=%s' % \
      (self.Worker_URL, self.Route, self.RouteRedir, self.Factor, self.Set, self.Status, self.Elected, self.To, self.From)


class LoadBalancer:
  """apache Load Balancer class - contains a list of Workers"""
  def __init__(self):
    self.name = ''
    self.StickySession = ''
    self.Timeout = ''
    self.FailoverAttempts = ''
    self.Method = ''
    self.workers = []

  def __str__(self):
    return 'Load balancer (%d workers): name=%s, StickySession=%s, Timeout=%s, FailoverAttempts=%s, Method=%s' % \
      (len(self.workers), self.name, self.StickySession, self.Timeout, self.FailoverAttempts, self.Method)
    

class VHost:
  """Class representing a VHost - contains a list of LoadBalancers"""
  def __init__(self):
    self.name = ''
    self.lbs = []
    self.balancerUrlPath = 'balancer-manager'

  def __str__(self):
    return 'vhost: (%d lbs): name=%s, balancerUrlPath=%s' % (len(self.lbs), self.name, self.balancerUrlPath)


class Server:
  """Class representing an apache httpd server - contains a list of VHosts"""
  def __init__(self):
    self.ip   = ''
    self.port = '80'
    self.vhosts = []
    self.error = False

  def add_vhost(self, name, balancerUrlPath='balancer-manager'):
    vh = VHost()
    vh.name = name
    vh.balancerUrlPath = balancerUrlPath
    self.vhosts.append(vh)

  def __str__(self):
    boldblink=['bold', 'blink']
    bold=['bold']
    return 'Server (%d vhosts) [%s]: ip=%s, port=%s' % (len(self.vhosts), (colored('KO', 'red', attrs=boldblink) if self.error else colored('OK', 'green', attrs=bold)), self.ip, self.port)
    
class Cluster:
  """Class representing a group of apache Servers - contains a list of Servers"""
  def __init__(self):
    self.name = ''
    self.servers = []

  def __str__(self):
    return 'Cluster (%d servers): name=%s' % (len(self.servers), self.name)

def print_debug(obj):
  if isinstance(obj, list):
    map(print_debug, obj)
  else:
    print obj

  if isinstance(obj, Cluster):
    print_debug(obj.servers)
  elif isinstance(obj, Server):
    print_debug(obj.vhosts)
  elif isinstance(obj, VHost):
    print_debug(obj.lbs)
  elif isinstance(obj, LoadBalancer):
    print_debug(obj.workers) 

