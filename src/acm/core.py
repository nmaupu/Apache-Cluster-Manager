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
## Package acm.core
## Core objects for Apache Cluster Manager project
from termcolor import colored
from functional import curry
import re
import copy

class Worker():
  """apache Load Balancer Worker class"""
  def __init__(self):
    self.mark = False
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
  
  def setMark(self, m):
    self.mark = m

  def __str__(self):
    return '  Worker: Worker_URL=%s, Route=%s, RouteRedir=%s, Factor=%s, Set=%s, Status=%s, Elected=%s, To=%s, From=%s' % \
      (self.Worker_URL, self.Route, self.RouteRedir, self.Factor, self.Set, self.Status, self.Elected, self.To, self.From)


class LoadBalancer():
  """apache Load Balancer class - contains a list of Workers"""
  def __init__(self):
    self.mark = False
    self.name = ''
    self.StickySession = ''
    self.Timeout = ''
    self.FailoverAttempts = ''
    self.Method = ''
    self.workers = []

  def setMark(self, m):
    self.mark = m
    for w in iter(self.workers):
      w.setMark(m)

  def __str__(self):
    return 'Load balancer (%d workers): name=%s, StickySession=%s, Timeout=%s, FailoverAttempts=%s, Method=%s' % \
      (len(self.workers), self.name, self.StickySession, self.Timeout, self.FailoverAttempts, self.Method)
    

class VHost():
  """Class representing a VHost - contains a list of LoadBalancers"""
  def __init__(self):
    self.mark = False
    self.name = ''
    self.lbs = []
    self.balancerUrlPath = 'balancer-manager'

  def setMark(self, m):
    self.mark = m
    for lb in iter(self.lbs):
      lb.setMark(m)

  def __str__(self):
    return 'vhost: (%d lbs): name=%s, balancerUrlPath=%s' % (len(self.lbs), self.name, self.balancerUrlPath)


class Server():
  """Class representing an apache httpd server - contains a list of VHosts"""
  def __init__(self):
    self.mark = False
    self.ip   = ''
    self.port = '80'
    self.vhosts = []
    self.error = False

  def add_vhost(self, name, balancerUrlPath='balancer-manager'):
    vh = VHost()
    vh.name = name
    vh.balancerUrlPath = balancerUrlPath
    self.vhosts.append(vh)

  def setMark(self, m):
    self.mark = m
    for vh in iter(self.vhosts):
      vh.setMark(m)

  def __str__(self):
    boldblink=['bold', 'blink']
    bold=['bold']
    return 'Server (%d vhosts) [%s]: ip=%s, port=%s' % (len(self.vhosts), (colored('KO', 'red', attrs=boldblink) if self.error else colored('OK', 'green', attrs=bold)), self.ip, self.port)
    
class Cluster():
  """Class representing a group of apache Servers - contains a list of Servers"""
  def __init__(self):
    self.mark = False
    self.name = ''
    self.servers = []

  def setMark(self, m):
    self.mark = m
    for s in iter(self.servers):
      s.setMark(m)

  def __str__(self):
    return 'Cluster (%d servers): name=%s' % (len(self.servers), self.name)


##
def acm_filter(obj, filter_cluster='.*', filter_vhost='.*', filter_lbname='.*', filter_route='.*', filter_worker='.*'):
  '''Apply given filters to given acm object'''
  f=curry(acm_filter, \
          filter_cluster=filter_cluster, \
          filter_vhost=filter_vhost, \
	  filter_lbname=filter_lbname, \
	  filter_route=filter_route, \
	  filter_worker=filter_worker)
  if isinstance(obj, list):
    map(f, obj)

  if isinstance(obj, Cluster):
    match = re.search(filter_cluster, obj.name)
    if match is None:
      obj.setMark(True)
    f(obj.servers)
  elif isinstance(obj, Server):
    f(obj.vhosts)
  elif isinstance(obj, VHost):
    match = re.search(filter_vhost, obj.name)
    if match is None:
      obj.setMark(True)
    f(obj.lbs)
  elif isinstance(obj, LoadBalancer):
    match = re.search(filter_lbname, obj.name)
    if match is None:
      obj.setMark(True)
    f(obj.workers)
  elif isinstance(obj, Worker):
    match_url   = re.search(filter_worker, obj.Worker_URL)
    match_route = re.search(filter_route, obj.Route)
    if match_url is None or match_route is None:
      obj.setMark(True)


def acm_print(obj):
  '''Print given acm object'''
  if isinstance(obj, list):
    map(acm_print, obj)
  elif not obj.mark:
    print obj

  if isinstance(obj, Cluster):
    acm_print(obj.servers)
  elif isinstance(obj, Server):
    acm_print(obj.vhosts)
  elif isinstance(obj, VHost):
    acm_print(obj.lbs)
  elif isinstance(obj, LoadBalancer):
    acm_print(obj.workers) 

