# encoding: utf-8

from __future__ import print_function
from __future__ import absolute_import

import sys
import yaml

from optparse import OptionParser

from .utils import *
from .ouroboros  import Ouroboros

__all__ = ('run_script')

__version__ = "0.1.0"
__author__ = "Eduard Snesarev"

default_config = {
  'timeout': 2,

  'redis': {
    'host': '127.0.0.1',
    'port': '6379',
    'db': None,
    'queue_name': None
  },
  'http': {
    'bind': '127.0.0.1',
    'port': 8080
  }
}

def run_script():
    p = OptionParser()
    p.add_option('-c', '--config', dest="config_path", help="path to config.yml")
    (opt, args) = p.parse_args()

    if opt.config_path:
        try:
            config = yaml.load(file(opt.config_path))
        except (OSError, IOError):
            print("error: could not open config `{0}`".format(opt.config_path))
            sys.exit(1)
        except yaml.YAMLError:
            print("error: could not parse config `{0}`".format(opt.config_path))
            sys.exit(1)
    else:
        print("error: missing required argument '-c|--config', see {0} -h".format(sys.argv[0]))
        sys.exit(1)

    config = merge(default_config, config)

    for x in ['queue_name', 'db']:
        if config['redis'][x] is None:
            print("error: missing required parameter in config 'redis.{0}'".format(x))
            sys.exit(1)

    try:
        o = Ouroboros(config)
        o.run()
    except KeyboardInterrupt:
        sys.exit(1)
