#!/usr/bin/python
#-*- coding:utf-8 -*-

from credentials import get_nova_creds
from novaclient.client import Client
from novaclient.v2.client import servers

creds = get_nova_creds()

nova_client = Client(creds['version'],creds['username'],creds['password'],creds['project_id'],creds['auth_url'])

instances = nova_client.servers.list(detailed=True)

print type(instances)

print "\n"

for ser in instances:
    print "."*60
    print ser.id
    print ser.name
    print ser.user_id
    print ser.tenant_id
    print nova_client.images.get(ser.image['id']).name
    print nova_client.flavors.get(ser.flavor['id']).name
    print ser.key_name
    print ser.status
    print ser.created
    print getattr(ser,'accessIPv4')
    name = getattr(ser,'OS-EXT-SRV-ATTR:host')
    print name
    addresses = ser.addresses
    addresses_key = addresses.keys()[0]
    print addresses[addresses_key][0]['addr']
    print "."*60
    print "\n"
