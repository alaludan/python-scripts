#!/usr/bin/python
from os import environ as env
from keystoneauth1 import loading
from keystoneauth1 import session
from keystoneclient.v2_0 import client
from heatclient.client import Client as Heat_Client
from credentials import get_nova_creds

creds = get_nova_creds()

keystone = client.Client(auth_url=env['OS_AUTH_URL'],
                         username=env['OS_USERNAME'],
                         password=env['OS_PASSWORD'],
                         tenant_name=env['OS_TENANT_NAME'])


heat_endpoint = keystone.service_catalog.url_for(service_type='orchestration',endpoint_type='publicURL')
heatclient = Heat_Client('1',heat_endpoint,token=keystone.auth_token)

def list_stacks():
    return heatclient.stacks.list()

aa = list_stacks()

stack_id = "e3610e64-3574-42b5-b77f-7efa3421b10f"

heatclient.resources.list(stack_id)
