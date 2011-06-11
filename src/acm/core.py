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

class LoadBalancer(list):
  """apache Load Balancer class - contains a list of Workers"""
  def __init(self):
    self.name = ''
    self.StickySession = ''
    self.Timeout = ''
    self.FailoverAttempts = ''
    self.Method = ''

class VHost(list):
  """Class representing a VHost - contains a list of LoadBalancers"""
  def __init__(self):
    self.name = ''

class Server(list):
  """Class representing an apache httpd server - contains a list of VHosts"""
  def __init__(self):
    self.ip   = ''
    self.port = '80'
    
class Cluster(list):
  """Class representing a group of apache Servers - contains a list of Servers"""
  def __init__(self):
    self.name = ''
