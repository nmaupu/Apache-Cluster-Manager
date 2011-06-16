#!/usr/bin/python

## Package acm.acm
##
from core import *
from parser import *
from urllib2 import URLError
from optparse import OptionParser, OptionGroup
from functional import curry

parser = OptionParser()
parser.add_option('-c', '--conf', dest='conf', \
  help='Specify configuration file')

group_set = OptionGroup(parser, "Setter options")
group_set.add_option('--lf', dest='lf', action='store', type='int', \
  help='Set load factor')
group_set.add_option('--ls', dest='ls', action='store', type='int', \
  help='Set lbset')
group_set.add_option('--wr', dest='wr', action='store', type='string', \
  help='Set route')
group_set.add_option('--rr', dest='rr', action='store', type='string', \
  help='Set route redirect')
group_set.add_option('--dw', dest='dw', action='store', type='choice', choices=('Enable', 'Disable'), \
  help='Set worker status (Enable|Disable)')

group_cmd = OptionGroup(parser, "Command options")
group_cmd.add_option('-i', '--info', dest='cmd', action='store_const', const="info", \
  help='Specify configuration file')
group_cmd.add_option('-s', '--set', dest='cmd', action='store_const', const="set", \
  help='Set a server var, specify -o')

parser.add_option_group(group_cmd)
parser.add_option_group(group_set)

(opts, args) = parser.parse_args()

##

if not opts.conf:
  print 'Give me a configuration file !'
  sys.exit(1)

if opts.cmd == 'info':
  configParser = ConfigParser(opts.conf)
  clusters = configParser.readConf()
  for c in iter(clusters):
    for s in iter(c.servers):
      map(curry(process_server_vhost, s), s.vhosts)
  print_debug(clusters)
elif opts.cmd == 'set':
  if opts.lf:
    print 'Setting lf'
  if opts.ls:
    print 'Setting ls'
  if opts.wr:
    print 'Setting wr'
  if opts.rr:
    print 'Setting rr'
  if opts.dw:
    print 'Setting dw'
else:
  print "No command specified, use -h or --help"

