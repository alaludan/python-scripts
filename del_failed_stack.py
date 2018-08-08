#!/usr/bin/python
import os
import sys
import time

failed_resource_id_list = []
sub_failed_resource_id_list = []
volume_id_list = []

def get_failed_resource_id():
    
    stack_id = str(sys.argv[1])
    failed_resource_info = os.popen("openstack stack resource list %s -f value -c physical_resource_id -c resource_type -c resource_status|grep -v COMP|awk -F' ' '{print $1}'" % (stack_id))
    failed_resource_ids = failed_resource_info.readlines()
	
    for failed_resource_id in failed_resource_ids:
	failed_resource_id = str(failed_resource_id).strip()
	failed_resource_id_list.append(failed_resource_id)
        print "failed_resource_id:%s" % (failed_resource_id)
    return failed_resource_id_list

def get_sub_resource_id():

    for sub_resource_id in failed_resource_id_list:
        sub_failed_resource_info = os.popen("openstack stack resource list %s -f value -c physical_resource_id" % (sub_resource_id))
        sub_failed_resource_ids = sub_failed_resource_info.readlines()
        
        for sub_failed_resource_id in sub_failed_resource_ids:
            sub_failed_resource_id = str(sub_failed_resource_id).strip()
            sub_failed_resource_id_list.append(sub_failed_resource_id)
            print "sub_failed_resource_id:%s" % (sub_failed_resource_id)
    return sub_failed_resource_id_list
            
	 
def get_volume_id():

    for sub_failed_id in sub_failed_resource_id_list:
	volume_id_info = os.popen("openstack stack resource list %s -f value -c physical_resource_id -c resource_type -c resource_status|grep -v COMP|awk -F' ' '{print $1}'" % (sub_failed_id))
        volume_ids = volume_id_info.readlines()
		
        for volume_id in volume_ids:
	    volume_id = str(volume_id).strip()
            volume_id_list.append(volume_id)
            print "volume_id:%s" % (volume_id)
    return volume_id_list

def del_volume():
    for volume_id in volume_id_list:
        os.system("cinder reset-state --state available --attach-status detached %s" % (volume_id))
        time.sleep(0.5)
        os.system("cinder delete %s" % (volume_id))

def main():
    get_failed_resource_id()
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

