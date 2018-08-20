#!/usr/bin/python

from util import SysUtil
from heatclient.client import CLient as HeatClient
from heatclient.common import utils
from heatclient.common import template_utils
import heatclient.exc as exc
from heatclient.exc import HTTPUnauthorized


heat_args = SysUtil.get_credentials()
print type(heat_args)
print heat_args
