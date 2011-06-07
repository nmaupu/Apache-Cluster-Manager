## Package acm.core
## Core objects for Apache Cluster Manager project

class Worker:
  """apache Load Balancer Worker class"""
  pass

class LoadBalancer(list):
  """apache Load Balancer class - contains a list of Workers"""
  pass

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
