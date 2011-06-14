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

group_cmd = OptionGroup(parser, "Command options")
group_cmd.add_option('-i', '--info', dest='info', action='store_true', default=False, \
  help='Specify configuration file')

parser.add_option_group(group_cmd)

(opts, args) = parser.parse_args()

if opts.info:
  ## Print info
  if opts.conf:
    configParser = ConfigParser(opts.conf)
    clusters = configParser.readConf()
    for c in iter(clusters):
      for s in iter(c.servers):
        map(curry(process_server_vhost, s), s.vhosts)
    print_debug(clusters)
else:
  print "No command specified, use -h or --help"

