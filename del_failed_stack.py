#!/usr/bin/python
import os
import time
import sys

del_failed_stack_list = []
del_failed_resource_list = []
del_failed_sub_resource_list = []
del_failed_volume_list = []

def get_stack_id():
    stack_info = os.popen("heat stack-list -g|grep DELETE_FAILED|awk -F'|' '{print $2}'")
    stack_ids = stack_info.readlines()
    for stack_id in stack_ids:
        stack_id = stack_id.strip()
        del_failed_stack_list.append(stack_id)
    return del_failed_stack_list

def get_resource_id():
    for stack_id in del_failed_stack_list:
        resource_info = os.popen("heat resource-list %s|grep DELETE_FAILED|awk -F'|' '{print $3}'" % (stack_id))
        resource_ids = resource_info.readlines()
        for resource_id in resource_ids:
            resource_id = resource_id.strip()
            del_failed_resource_list.append(resource_id)
    print "del_failed_resource_list:%s" % (del_failed_resource_list)
    return del_failed_resource_list

def get_resource_id_from_stack():
    stack_id = str(sys.argv[1])
    resource_info = os.popen("heat resource-list %s|grep DELETE_FAILED|awk -F'|' '{print $3}'" % (stack_id))
    resource_ids = resource_info.readlines()
    for resource_id in resource_ids:
        resource_id = resource_id.strip()
        del_failed_resource_list.append(resource_id)
    print "del_failed_resource_list:%s" % (del_failed_resource_list)
    return del_failed_resource_list
     
    
def get_sub_resource_id():
    for sub_resource_id in del_failed_resource_list:
        sub_resource_info = os.popen("heat resource-list %s|grep DELETE_FAILED|awk -F'|' '{print $3}'" % (sub_resource_id))
        sub_resource_ids = sub_resource_info.readlines()
        for sub_resource_id in sub_resource_ids:
            sub_resource_id = sub_resource_id.strip()
            del_failed_sub_resource_list.append(sub_resource_id)
    print "del_failed_sub_resource_list:%s" % (del_failed_sub_resource_list)
    return del_failed_sub_resource_list

def get_volume_id():
    for sub_resource_id in del_failed_sub_resource_list:
        volume_id_info = os.popen("heat resource-list %s|grep OS::Cinder::Volume|grep DELETE|awk -F'|' '{print $3}'" % (sub_resource_id))
        volume_ids = volume_id_info.readlines()
        for volume_id in volume_ids:
            volume_id = volume_id.strip()
            del_failed_volume_list.append(volume_id)
    print "del_failed_volume_list:%s" % (del_failed_volume_list)
    return del_failed_volume_list

def del_volume():
    for volume_id in del_failed_volume_list:
        os.system("cinder reset-state --state available --attach-status detached %s" % (volume_id))
        time.sleep(0.5)
        os.system("cinder delete %s" % (volume_id))

def del_stack():
    for stack_id in del_failed_stack_list:
        os.system("heat stack-delete %s -y" % (stack_id))        

def main():
    get_resource_id_from_stack()        
    get_sub_resource_id()       
    get_volume_id() 
    del_volume()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\n"
        print ">>>ERROR:lost stack id..."
        print "\n"
        print "Usage:%s stack_id" % (sys.argv[0])
        print "\n"
    else:
        main()
