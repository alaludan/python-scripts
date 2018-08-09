#!/usr/bin/python
import os
import sys
import time

volume_id_list = []
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
                resource_id = str(resource_id).strip()
                if "OS::Cinder::Volume" in resource_id:
                    resource_id = resource_id.split(" ")[0]
                    volume_id_list.append(resource_id)
                    flag = False
                else:
                    resource_id = resource_id.split(" ")[0]
                    id_list.append(resource_id)
        return volume_id_list

def del_volume():
    for volume_id in volume_id_list:
        os.system("cinder reset-state --state available --attach-status detached %s" % (volume_id))
        time.sleep(0.5)
        os.system("cinder delete %s" % (volume_id))

def main():
    get_id_list()
    del_volume()

if __name__ == '__main__':

    if len(sys.argv) !=2:
        print "\n"
        print ">>>ERROR:lost stack id..."
        print "\n"
        print ">>>Usage:%s stack_id" % (sys.argv[0])
        print "\n"
    else:
        main()    
