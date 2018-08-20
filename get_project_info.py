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
tenant = keystone.tenants.get("7a841c5733c54ff3800609b6ad822a31")
print tenant
print "\n"
print type(tenant)
print str(tenant)
