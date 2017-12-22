#!/usr/bin/env python
# 
# Script that create output/openstack-client.yml to put into ansible-openstack/#_environment_#/group_vars directory

import os,csv
from jinja2 import Environment, FileSystemLoader

### CONSTANTS

DEST_OS_YML="/opt/idpcloud-data/ansible-openstack/inventories/production/group_vars/openstack-client.yml"
IDP_CSV="data/vm-idp-os.csv"

### END CONSTANTS

def prepare(vals):
   # Create the jinja2 environment.
   # Notice the use of trim_blocks, which greatly helps control whitespace.
   j2_env = Environment(loader=FileSystemLoader(os.getcwd()),keep_trailing_newline=True,trim_blocks=True,lstrip_blocks=True)
   result = j2_env.get_template('templates/openstack-client.yml.j2').render(j2_vals=vals)
   return result

if __name__ == '__main__':

   # Load Institutions CSV data
   idp_csv = open(IDP_CSV,"rU")
   idp_csv_reader = csv.reader(idp_csv,delimiter=';')

   vals = {}

   # Saltare sempre la linea degli HEADER
   firsLine1 = True

   idp_num = 1

   # ITERAZIONE SU OGNI IDP
   for row in idp_csv_reader:

      if (firsLine1 == True):
         firsLine1 = False
   	 os_client_yml = open(DEST_OS_YML, "w")
         os_client_yml.write("---\nos_vms:\n")
         os_client_yml.close()
         continue

      vals[idp_num] = {}

      vals[idp_num]['fqdn'] = row[0]
      vals[idp_num]['ip_priv'] = row[1]
      vals[idp_num]['ip_pub'] = row[2]
      vals[idp_num]['state'] = row[3]

      idp_num = idp_num + 1

   os_client_yml = open(DEST_OS_YML, "a+")
   values = prepare(vals)
   os_client_yml.write(values)
   os_client_yml.close()
