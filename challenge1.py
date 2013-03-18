#!/usr/bin/env python

import os
import pyrax
import time
from sys import stdout
import re

credentials_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.rackspace_cloud_credentials')
pyrax.set_credential_file(credentials_file)

cloudservers = pyrax.cloudservers

image_id = "8a3a9f96-b997-46fd-b7a8-a9e740796ffd"
flavor_id = 2

server_dict = {}

for i in range(0,3):
  server_name = "web%s" % i
  server = cloudservers.servers.create(server_name, image_id, flavor_id)
  server_dict[server_name] = {}
  server_dict[server_name] = { "serverId" : server.id, "adminPass" : server.adminPass, "accessIPv4" : server.accessIPv4, "serverName" : server.name }

pattern = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")

for key in server_dict.keys():
  server_id = server_dict[key]['serverId']
  server = cloudservers.servers.get(server_id)
  server_name = server.name
  while server.status != "ACTIVE" and not pattern.match(server.accessIPv4):
    time.sleep(5)
    server = cloudservers.servers.get(server_id)
  server_dict[server_name]['accessIPv4'] = server.accessIPv4

for server in server_dict.keys():
  if not pattern.match(server_dict[server]['accessIPv4']):
    server = cloudservers.servers.get(server_dict[server]['serverId'])
    server_dict[server]['accessIPv4'] = server.accessIPv4

  print "%s : %s : %s" % (server_dict[server]['serverName'],
                               server_dict[server]['accessIPv4'],
                               server_dict[server]['adminPass'])

