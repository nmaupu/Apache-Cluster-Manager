## Package acm.core
## Core objects for Apache Cluster Manager project

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
  
  def toString(self):
    return '  Worker: actionURL=%s, Worker_URL=%s, Route=%s, RouteRedir=%s, Factor=%s, Set=%s, Status=%s, Elected=%s, To=%s, From=%s' % \
      (self.actionURL, self.Worker_URL, self.Route, self.RouteRedir, self.Factor, self.Set, self.Status, self.Elected, self.To, self.From)


class LoadBalancer:
  """apache Load Balancer class - contains a list of Workers"""
  def __init__(self):
    self.name = ''
    self.StickySession = ''
    self.Timeout = ''
    self.FailoverAttempts = ''
    self.Method = ''
    self.workers = []

  def toString(self):
    return 'Load balancer (%d workers): name=%s, StickySession=%s, Timeout=%s, FailoverAttempts=%s, Method=%s' % \
      (len(self.workers), self.name, self.StickySession, self.Timeout, self.FailoverAttempts, self.Method)
    

class VHost:
  """Class representing a VHost - contains a list of LoadBalancers"""
  def __init__(self):
    self.name = ''
    self.lbs = []
    self.balancerUrlPath = 'balancer-manager'


class Server:
  """Class representing an apache httpd server - contains a list of VHosts"""
  def __init__(self):
    self.ip   = ''
    self.port = '80'
    self.vhosts = []
    
class Cluster:
  """Class representing a group of apache Servers - contains a list of Servers"""
  def __init__(self):
    self.name = ''
    self.servers = []
