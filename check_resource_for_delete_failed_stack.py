#!/usr/bin/python
import os
import sys
import time

volume_id_list = []
instance_id_list = []
port_id_list = []
id_list = []
flag = True

def get_id_list():

    global flag
    id_list = [str(sys.argv[1])]

    while flag:
         
        for id_ in id_list:
            
            resource_id_info = os.popen("openstack stack resource list %s -f value -c physical_resource_id -c resource_type -c resource_status|grep -v COMPL" % (id_))
            resource_ids = resource_id_info.readlines()
            
            for resource_id in resource_ids:
                resource_id = str(resource_id).rstrip()
                if "Stack not found" in resource_id:
                    continue
                elif "OS::Cinder::Volume" in resource_id:
                    resource_id = resource_id.split(" ")[0]
                    volume_id_list.append(resource_id)
                    flag = False
                elif "OS::Nova::Server" in resource_id:
                    resource_id = resource_id.split(" ")[0]
                    if resource_id == "":
                        resource_id = "NULL"
                        instance_id_list.append(resource_id)
                    else:
                        instance_id_list.append(resource_id)
                    flag = False
                elif "OS::Neutron::Port" in resource_id:
                    resource_id = resource_id.split(" ")[0]
                    port_id_list.append(resource_id)
                    flag = False
                else:
                    resource_id = resource_id.rsplit(" ")[0]
                    id_list.append(resource_id)
        return volume_id_list,instance_id_list,port_id_list

def del_volume():
    for volume_id in volume_id_list:
        os.system("cinder reset-state --state available --attach-status detached %s" % (volume_id))
        time.sleep(0.5)
        os.system("cinder delete %s" % (volume_id))

def main():
    get_id_list()
    print "\n"
    print "Not delete resoures..."
    print "\n"
    if len(volume_id_list):
        print "Not delete volumes:%s" % (volume_id_list)
    print "\n"

    if len(instance_id_list):
        print "Not delete instances:%s" % (instance_id_list)
    print "\n"

    if len(port_id_list):
        print "Not delete ports:%s" % (port_id_list)
    print "\n"

if __name__ == '__main__':

    if len(sys.argv) !=2:
        print "\n"
        print ">>>ERROR:lost stack id..."
        print "\n"
        print ">>>Usage:%s stack_id" % (sys.argv[0])
        print "\n"
    else:
        main()    
