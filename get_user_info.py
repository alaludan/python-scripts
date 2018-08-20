#!/usr/bin/python
from os import environ as env
from keystoneclient.v2_0 import client
from credentials import get_keystone_creds

creds = get_keystone_creds
keystone = client.Client(auth_url=env['OS_AUTH_URL'],
                         username=env['OS_USERNAME'],
                         password=env['OS_PASSWORD'],
                         tenant_name=env['OS_TENANT_NAME'])

print keystone.tenants.list()
print "\n"
user = keystone.users.get("f58500c108b54df4b4d2285ca443b6a8")
print user
print "\n"
print keystone.users.list()

