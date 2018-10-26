#!/usr/bin/python


#####################################################################################
#This tool will automatically clear the specified project all the volume, vm, image #
#, network, net, stack, and then delete the user, the final need to manually delete #
# the project!                                                                      #
#                                                                                   #
#                                              -----Developer by Yupeng Luo         #
#                                              -----Mail:yupeng.luo@nokia-sbell.com #
#####################################################################################


import os
import sys
import time
import logging

project_dic = {}
vol_id_list = []
vol_snap_id_list = []
vm_id_list = []
image_id_list = []
net_id_list = []
subnet_id_list = []
port_id_list = []
all_port_id_list = [] 
user_id_list = []
stack_id_list = []
secgroup_id_list = []
dhcp_agent_id_list = []
router_id_list = []
project_name = ""
project_id = ""

check_vm = check_vol = check_vol_snap = check_subnet = check_net = check_port = check_image = check_stack = check_secgroup = check_router = True 

LOG_FILENAME = sys.argv[0]+".log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT)

def usage():
    print """
          *****************************************
          * Please run "source node_name" command *
          * before using this tool.               *
          * eg:source n13                         *
          *                                       *
          * Usage:                                *
          * %s                                    *
          *                                       *
          *****************************************
          """ % (sys.argv[0])

class project:

    def get(self):
        print "\n def get \n"
        info = os.popen("openstack project list -f value")
        project_info = info.readlines()
        for project in project_info:
            project = str(project).strip()
            project_name = project.split(" ")[1]
            project_id = project.split(" ")[0]
            project_dic[project_id] = project_name
        return project_dic

    def disable(self,project_id):
        print "\n def disable \n"
        if project_dic.has_key(project_id):
            project_id = project_dic[project_id]
            os.system("openstack project set --disable %s" % (project_id))
            title = "Disable Project"
            content = project_id + " " + "disable successful"
            print "\n"
            print title.center(100,'*')
            print "*" + " "*98 + "*"
            print "*" + " "*98 + "*"
            print content.center(100,"*")
            print "*" + " "*98 + "*"
            print "*" + " "*98 + "*"
            print "*"*100
            print "\n"
            logging.info(content)
        else:
            loginfo = "%s does not exist" % (project_id)
            logging.error(loginfo)
            sys.exit(10)

    def show_user(self,project_id):
        print "\n def show_user \n"
        print "=>Show All Users of %s..." % (project_id)
        os.system("openstack user list --project %s|grep -v -w admin" % (project_id))
        user_info = os.popen("openstack user list -f value -c ID -c Name --project %s |grep -v -w admin" % (project_id))
        user_ids = user_info.readlines()
        for user_id in user_ids:
            user_id = str(user_id).strip().split(" ")[0]
            user_id_list.append(user_id)
        return user_id_list

    def show_vol(self,project_id):
        print "\n def show_vol \n"
        print "=>Show All Volumes Of %s..." % (project_id)
        os.system("openstack volume list --project %s" % (project_id))
        print "\n"
        vol_info = os.popen("openstack volume list --project %s -f value -c ID" % (project_id))
        vol_ids = vol_info.readlines()
        for vol_id in vol_ids:
            vol_id = str(vol_id).strip()
            vol_id_list.append(vol_id)
        return vol_id_list

    def show_vol_snap(self,project_id):
        print "\n def show_vol_snap \n"
        print "=>Show All Snapshot Of %s..." % (project_id)
        os.system("openstack volume snapshot list --project %s" % (project_id))
        print "\n"
        vol_snap_info = os.popen("openstack volume snapshot list --project %s -f value -c ID" % (project_id))
        vol_snap_ids = vol_snap_info.readlines()
        for vol_snap_id in vol_snap_ids:
            vol_snap_id = str(vol_snap_id).strip()
            vol_snap_id_list.append(vol_snap_id)
        return vol_snap_id_list
        
    def show_vm(self,project_id):
        print "\n def show_vm \n"
        print "=>Show All VM Of %s..." % (project_id)
        os.system("openstack server list --project %s" % (project_id))
        print "\n"
        vm_info = os.popen("openstack server list --project %s -f value -c ID" % (project_id))
        vm_ids = vm_info.readlines()
        for vm_id in vm_ids:
            vm_id = str(vm_id).strip()
            vm_id_list.append(vm_id)
        return vm_id_list

    def show_image(self,project_id):
        print "\n def show_image \n"
        print "=>Show All Images Of %s..." % (project_id)
        os.system("glance image-list --owner %s" % (project_id))
        print "\n"
        image_info = os.popen("glance image-list --owner %s|awk -F'|' '{print $2}'|awk 'NR>2'|awk NF" % (project_id))
        image_ids = image_info.readlines()
        for image_id in image_ids:
            image_id = str(image_id).strip()
            image_id_list.append(image_id)
        return image_id_list

    def show_subnet(self,project_id):
        print "\n def show_subnet \n"
        print "=>Show All Subnets Of %s..." % (project_id)
        print "\n"
        os.system("openstack subnet list --long -f value -c ID -c Project -c Name|grep %s" % (project_id))
        print "\n"
        subnet_info = os.popen("openstack subnet list --long -f value -c ID -c Project|grep %s" % (project_id))
        subnet_ids = subnet_info.readlines()
        for subnet_id in subnet_ids:
            subnet_id = str(subnet_id).strip().split(" ")[0]
            subnet_id_list.append(subnet_id)
        return subnet_id_list

    def show_net(self,project_id):
        print "\n def show_net \n"
        print "=>Show All Networks Of %s..." % (project_id)
        os.system("openstack network list --project %s" % (project_id))
        print "\n"
        net_info = os.popen("openstack network list --project %s -f value -c ID" % (project_id))
        net_ids = net_info.readlines()
        for net_id in net_ids:
            net_id = str(net_id).strip()
            net_id_list.append(net_id)
        return net_id_list

    def show_all_port(self,project_id):
        print "\n def show_all_port \n" 
        os.system("openstack port list --project %s" %(project_id))
        all_port_info = os.popen("openstack port list --project %s -f value -c ID" % (project_id))
        all_port_ids = all_port_info.readlines()
        for all_port_id in all_port_ids:
            all_port_id = str(all_port_id).strip()
            all_port_id_list.append(all_port_id)

        for net_id in net_id_list:
            all_net_port_info =os.popen("openstack port list --network %s -f value -c ID" % (net_id))
            all_net_port_ids = all_net_port_info.readlines()
            for all_net_port_id in all_net_port_ids:
                all_net_port_id = str(all_net_port_id).strip()
                all_port_id_list.append(all_net_port_id)

        return all_port_id_list

    def show_dhcp_agent(self,project_id):
        print "\n def show_dhcp_agent \n"
        print "=>Show All DHCP_AGENT of %s..." % (project_id)
        os.system("openstack network agent list|grep DHCP")
        print "\n"
        dhcp_agent_info = os.popen("openstack network agent list|grep dhcp|awk -F '|' '{print $2}'")
        dhcp_agent_ids = dhcp_agent_info.readlines()
        for dhcp_agent_id in dhcp_agent_ids:
            dhcp_agent_id = str(dhcp_agent_id).strip()
            dhcp_agent_id_list.append(dhcp_agent_id)
        return dhcp_agent_id_list

    def show_router(self,project_id):
        print "\n def show_router \n"
        print "=>Show All Routers Of %s..." % (project_id)
        os.system("openstack router list|grep %s" % (project_id))
        print "\n"
        router_info = os.popen("openstack router list|grep %s|awk -F'|' '{print $2}'" % (project_id))
        router_ids = router_info.readlines()
        for router_id in router_ids:
            router_id = str(router_id).strip()
            router_id_list.append(router_id)
        return router_id_list

    def show_router_port(self):
        print "\n def show_router_port \n"
        for router_id in router_id_list:
            print "=>Show All Ports Of Routers %s" % (router_id)
            os.system("openstack port list --router %s" % (router_id))
            router_port_info = os.popen("openstack port list --router %s -f value -c ID" % (router_id))
            router_port_ids = router_port_info.readlines()
            for router_port_id in router_port_ids:
                router_port_id = str(router_port_id).strip()
                router_port_id_list.append(router_port_id)
            return router_port_id_list
 
    def show_secgroup(self,project_id):
        print "\n def show_secgroup \n"
        print "=>Show All Secgroups Of %s..." % (project_id)
        os.system("openstack security group list --all|grep %s" % (project_id))
        os.system("openstack security group list --all|grep %s" % (project_id))
        print "\n"
        secgroup_info = os.popen("openstack security group list --all|grep %s|awk -F'|' '{print $2}'" % (project_id))
        secgroup_ids = secgroup_info.readlines()
        for secgroup_id in secgroup_ids:
            secgroup_id = str(secgroup_id).strip()
            secgroup_id_list.append(secgroup_id)
        return secgroup_id_list 

    def show_stack(self,project_id):
        print "\n def show_stack \n"
        print "=>Show All Stacks Of %s..." % (project_id)
        print "\n"
        os.system('openstack stack list --all-project -f value -c ID -c "Stack Name" -c Project|grep %s' % (project_id))
        print "\n"
        stack_info = os.popen('openstack stack list --all-project -f value -c ID -c "Stack Name" -c Project|grep %s' % (project_id))
        stack_ids = stack_info.readlines()
        for stack_id in stack_ids:
            stack_id = str(stack_id).strip().split(" ")[0]
            stack_id_list.append(stack_id)
        return stack_id_list

    def reset_vol_status(self,project_id):
        print "\n def reset_vol_status \n"
        print "=>Reset Volume..."
        print "\n"
        for vol_id in vol_id_list:
            os.system("cinder reset-state --state available --attach-status detached %s" % (vol_id))
            print "Reset status for VM:%s" % (vol_id)
            loginfo = "Volume:%s reset successful..." % (vol_id)
            logging.info(loginfo)
            time.sleep(2)
        print "\n"
        print "\n"

    def shutdown_vm(self,project_id):
        print "\n def shutdown_vm \n"
        print "=>Shutdown All VMs of %s..." % (project_id)
        print "\n"
        for vm in vm_id_list:
            os.system("openstack server stop %s" % (vm))
            print "Stop VM:%s" % (vm)
            loginfo = "Stop vm %s successful..." % (vm)
            logging.info(loginfo)
            time.sleep(10)
        print "\n"
        print "\n"

    def del_vol_snap(self,project_id):
        print "\n def del_vol_snap"
        print "=>Delete All Snapshots of %s..." % (project_id)
        print "\n"
        for vol_snap_id in vol_snap_id_list:
            print vol_snap_id
            os.system("openstack volume snapshot delete %s" % (vol_snap_id))
            print "Delete Volume Snapshot:%s" % (vol_snap_id)
            loginfo = "Delete Volume Snapshot %s successful..." % (vol_snap_id)
            logging.info(loginfo)
            time.sleep(10)
        print "\n"
        print "\n"
        
    def del_vol(self,project_id):
        print "\n def del_vol \n"
        print "=>Delete All Volumes of %s..." % (project_id)
        print "\n"
        for vol_id in vol_id_list:
            os.system("openstack volume delete %s" % (vol_id))
            print "Delete Volume:%s" % (vol_id)
            loginfo = "Delete volume %s successful..." % (vol_id)
            logging.info(loginfo)
            time.sleep(10)
        print "\n"
        print "\n"

    def del_vm(self,project_id):
        print "\n def del_vm \n"
        print "=>Delete All VMs of %s..." % (project_id)
        print "\n"
        for vm in vm_id_list:
            os.system("openstack server delete %s" % (vm))
            print "Delete VM:%s" % (vm)
            loginfo = "Delete VM %s successful..." % (vm)
            logging.info(loginfo)
            time.sleep(10)
        print "\n"
        print "\n"

    def del_image(self,project_id):
        print "\n def del_image \n"
        print "=>Delete All Images Of %s..." % (project_id)
        print "\n"
        for image in image_id_list:
            os.system("openstack image set %s --unprotected" % (image))
            os.system("openstack image delete %s" % (image))
            print "Delete image:%s" % (image)
            loginfo = "Delete image %s successful..." % (image)
            logging.info(loginfo)
            time.sleep(2)
        print "\n"
        print "\n"


    def del_router(self,project_id):
        print "\n def del_router \n"
        print "=>Delete All Routers Of %s" % (project_id)
        for router_id in router_id_list:
            router_port_info = os.popen("openstack port list --router %s -f value -c ID" % (router_id)) 
            router_port_ids = router_port_info.readlines()
            for router_port_id in router_port_ids:
                os.system("openstack router remove port %s %s" % (router_id,router_port_id))
                time.sleep(2)
            os.system("openstack router delete %s" % (router_id))
            print "Delete router:%s" % (router_id)
            loginfo = "Delete router %s successful..." % (router_id)
            logging.info(loginfo)

    def remove_dhcp_agent(self):
        print "\n def remove_dhcp_agent \n"
        for dhcp_agent_id in dhcp_agent_id_list:
            for net_id in net_id_list:
                os.system("openstack network agent remove network %s %s" % (dhcp_agent_id,net_id))
                time.sleep(2)

    def del_port(self,project_id):
        print "\n def del_port \n"
        print "=>Delete All ports of %s" % (project_id)
        for port_id in all_port_id_list:
            os.system("openstack port delete %s" % (port_id))
            loginfo = "Delete port %s successful..." % (port_id)
            logging.info(loginfo)
            time.sleep(2)

    def del_subnet(self,project_id):
        print "\n def del_subnet \n"
        print "=>Delete All subnets of %s" % (project_id)

        for subnet_id in subnet_id_list:
            os.system("openstack subnet delete %s" % (subnet_id))
            time.sleep(2)
            print "Delete subnet:%s" % (subnet_id)
            loginfo = "Delete subnet %s successful..." % (subnet_id)
            logging.info(loginfo)

    def del_net(self,project_id):
        print "\n def del_net \n"
        print "=>Delete All Networks Of %s..." % (project_id)
        print "\n"
        for net_id in net_id_list:
            os.system("openstack network delete %s" %(net_id))
            print "Delete network:%s" % (net_id)
            loginfo = "Delete network %s successful..." % (net_id)
            logging.info(loginfo)
            time.sleep(2)
        print "\n"
        print "\n"

    def del_secgroup(self,project_id):
        print "\n def del_secgroup \n"
        print "=>Delete All Secgroups Of %s..." % (project_id)
        print "\n"
        for secgroup_id in secgroup_id_list:
            os.system("openstack security group delete %s" %(secgroup_id))
            print "Delete secgroup:%s" % (secgroup_id)
            loginfo = "Delete security group %s successful..." % (secgroup_id)
            logging.info(loginfo)
            time.sleep(2)
        print "\n"
        print "\n"

    def del_user(self,project_id):
        print "\n def del_user \n"
        print "=>Delete All Users of %s..." % (project_id)
        print "\n"
        for user_id in user_id_list:
            os.system("openstack user delete %s" % (user_id))
            print "Delete user:%s" % (user_id)
            loginfo = "Delete user %s successful..." % (user_id)
            logging.info(loginfo)
            time.sleep(2)
        print "\n"
        print "\n"

    def del_stack(self,project_id):
        print "\n def del_stack \n"
        print "=>Delete All Stacks of %s..." % (project_id)
        print "\n"
        for stack_id in stack_id_list:
            os.system("openstack stack delete %s --yes" % (stack_id))
            print "Delete Stack:%s" % (stack_id)
            loginfo = "Delete stack %s successful..." % (stack_id)
            logging.info(loginfo)
            time.sleep(40)
        print "\n"
        print "\n"

class check:

    def vol(self,project_id):
        print "\n def vol \n"

        after_del_vol_id_list = []
        after_del_vol_info =  os.popen("openstack volume list --project %s -f value -c ID" % (project_id))
        after_del_vol_ids = after_del_vol_info.readlines()
        for after_del_vol_id in after_del_vol_ids:
            after_del_vol_id = str(after_del_vol_id).strip()
            after_del_vol_id_list.append(after_del_vol_id)

        if len(after_del_vol_id_list) == 0:
            print "All Volumes Clean up..."
            print "\n"
            loginfo = "All Volumes Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_vol_id in after_del_vol_id_list:
                print "Volume:%s does not delete,Please check!" % (after_del_vol_id)
                print "\n"
                loginfo = "Volume:%s does not delete..." % (after_del_vol_id)
                logging.error(loginfo)
                return False

    def vol_snap(self,project_id):
        print "\n def vol_snap \n"

        after_del_vol_snap_id_list = []
        after_del_vol_snap_info =  os.popen("openstack volume snapshot list --project %s -f value -c ID" % (project_id))
        after_del_vol_snap_ids = after_del_vol_snap_info.readlines()
        for after_del_vol_snap_id in after_del_vol_snap_ids:
            after_del_vol_snap_id = str(after_del_vol_snap_id).strip()
            after_del_vol_snap_id_list.append(after_del_vol_snap_id)

        if len(after_del_vol_snap_id_list) == 0:
            print "All Volume Snapshots Clean up..."
            print "\n"
            loginfo = "All Volume Snapshots Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_vol_snap_id in after_del_vol_snap_id_list:
                print "Volume Snapshot:%s does not delete,Please check!" % (after_del_vol_snap_id)
                print "\n"
                loginfo = "Volume Snapshot:%s does not delete..." % (after_del_vol_snap_id)
                logging.error(loginfo)

    def vm(self,project_id):
        print "\n def vm \n"
                
        after_del_vm_id_list = []
        after_del_info =  os.popen("openstack server list --project %s -f value -c ID" % (project_id))
        after_del_vm_ids = after_del_info.readlines()
        for after_del_vm_id in after_del_vm_ids:
            after_del_vm_id = str(after_del_vm_id).strip()
            after_del_vm_id_list.append(after_del_vm_id)

        if len(after_del_vm_id_list) == 0:
            print "All VMs Clean up..."
            print "\n"
            loginfo = "All VMs Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_vm_id in after_del_vm_id_list:
                print "VM:%s does not delete,Please check!" % (after_del_vm_id)
                print "\n"
                loginfo = "VM:%s does not delete..." % (after_del_vm_id)
                logging.error(loginfo)
                return False

    def subnet(self,project_id):
        print "\n def subnet \n"

        after_del_subnet_id_list = []
        after_del_subnet_info = os.popen("openstack subnet list --long -f value -c ID -c Project|grep %s" % (project_id))
        after_del_subnet_ids = after_del_subnet_info.readlines()
        for after_del_subnet_id in after_del_subnet_ids:
            after_del_subnet_id = str(after_del_subnet_id).strip().split(" ")[0]
            after_del_subnet_id_list.append(after_del_subnet_id)

        if len(after_del_subnet_id_list) == 0:
            print "All Subnets Clean up..."
            print "\n"
            loginfo = "All Subnets Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_subnet_id in after_del_subnet_id_list:
                print "Subnet:%s does not delete,Please check!" % (after_del_subnet_id)
                print "\n"
                loginfo = "Subnet:%s does not delete..." % (after_del_subnet_id)
                logging.error(loginfo)
                return False

    def secgroup(self,project_id):
        print "\n def secgroup \n"

        after_del_secgroup_id_list = []
        after_del_secgroup_info = os.popen("openstack security group list --all|grep %s|awk -F'|' '{print $2}'" % (project_id))
        after_del_secgroup_ids = after_del_secgroup_info.readlines()
        for after_del_secgroup_id in after_del_secgroup_ids:
            after_del_secgroup_id = str(after_del_secgroup_id).strip()
            after_del_secgroup_id_list.append(after_del_secgroup_id)

        if len(after_del_secgroup_id_list) == 0:
            print "All Secgroups Clean up..."
            print "\n"
            loginfo = "All Secgroups Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_secgroup_id in after_del_secgroup_id_list:
                print "Secgroup:%s does not delete,Please check!" % (after_del_secgroup_id)
                print "\n"
                loginfo = "Security group:%s does not delete..." % (after_del_secgroup_id)
                logging.error(loginfo)
                return False
    
    def router(self,project_id):
        print "\n def router \n"

        after_del_router_id_list = []     
        after_del_router_info = os.popen("openstack router list|grep %s|awk -F'|' '{print $2}'" % (project_id))
        after_del_router_ids = after_del_router_info.readlines()
        for after_del_router_id in after_del_router_ids:
            after_del_router_id = str(after_del_router_id).strip()
            after_del_router_id_list.append(after_del_router_id)

        if len(after_del_router_id_list) == 0:
            print "All Routers Clean up..."
            print "\n"
            loginfo = "All Routers Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_router_id in after_del_router_id_list:
                print "Routers:%s does not delete,Please check!" % (after_del_router_id)
                print "\n"
                loginfo = "Routers:%s does not delete..." % (after_del_router_id)
                logging.error(loginfo)
                return False

    def net(self,project_id):
        print "\n def net \n"

        after_del_net_id_list = []
        after_del_net_info = os.popen("openstack network list --project %s -f value -c ID" % (project_id))
        after_del_net_ids = after_del_net_info.readlines()
        for after_del_net_id in after_del_net_ids:
            after_del_net_id = str(after_del_net_id).strip()
            after_del_net_id_list.append(after_del_net_id)
        if len(after_del_net_id_list) == 0:
            print "All Networks Clean up..."
            print "\n"
            loginfo = "All Networks Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_net_id in after_del_net_id_list:
                print "Network:%s does not delete,Please check!" % (after_del_net_id)
                print "\n"
                loginfo = "Network:%s does not delete..." % (after_del_net_id)
                logging.error(loginfo)
                return False

    def port(self,project_id):
        print "\n def port \n"

        after_del_port_id_list = after_del_net_port_id_list = []

        after_del_port_info = os.popen("openstack port list --project %s -f value -c ID" % (project_id))
        after_del_port_ids = after_del_port_info.readlines()
        for after_del_port_id in after_del_port_ids:
            after_del_port_id = str(after_del_port_id).strip()
            after_del_port_id_list.append(after_del_port_id)

        for net_id in net_id_list:
            all_del_net_port_info =os.popen("openstack port list --network %s -f value -c ID" % (net_id))
            all_del_net_port_ids = all_del_net_port_info.readlines()
            for all_del_net_port_id in all_del_net_port_ids:
                all_del_net_port_id = str(all_del_net_port_id).strip()
                all_del_port_id_list.append(all_del_net_port_id)

        if len(after_del_port_id_list) == 0:
            print "All Ports Clean up..."
            print "\n"
            loginfo = "All Ports Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_port_id in after_del_port_id_list:
                print "Port:%s does not delete,Please check!" % (after_del_port_id)
                print "\n"
                loginfo = "Port:%s does not delete..." % (after_del_port_id)
                logging.error(loginfo)
                return False

    def image(self,project_id):
        print "\n def image \n"

        after_del_image_id_list = []
        after_del_image_info = os.popen("glance image-list --owner %s|awk -F'|' '{print $2}'|awk 'NR>2'|awk NF" % (project_id))
        after_del_image_ids = after_del_image_info.readlines()
        for after_del_image_id in after_del_image_ids:
            after_del_image_id = str(after_del_image_id).strip()
            after_del_image_id_list.append(after_del_image_id)

        if len(after_del_image_id_list) == 0:
            print "All Images Clean up..."
            print "\n"
            loginfo = "All Images Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_image_id in after_del_image_id_list:
                print "Image:%s does not delete,Please check!" % (after_del_image_id)
                print "\n"
                loginfo = "Image:%s does not delete..." % (after_del_image_id)
                logging.error(loginfo)
                return False

    def stack(self,project_id):
        print "\n def stack \n"

        after_del_stack_id_list = []
        after_del_stack_info = os.popen('openstack stack list --all-project -f value -c ID -c "Stack Name" -c Project|grep %s' % (project_id))
        after_del_stack_ids = after_del_stack_info.readlines()
        for after_del_stack_id in after_del_stack_ids:
            after_del_stack_id = str(after_del_stack_id).strip().split(" ")[0]
            after_del_stack_id_list.append(after_del_stack_id)

        if len(after_del_stack_id_list) == 0:
            print "All Stacks Clean up..."
            print "\n"
            loginfo = "All Stacks Clean up..."
            logging.info(loginfo)
            return True
        else:
            for after_del_stack_id in after_del_stack_id_list:
                print "Stack:%s does not delete,Please check!" % (after_del_stack_id)
                print "\n"
                loginfo = "Stack:%s does not delete..." % (after_del_stack_id)
                logging.error(loginfo)
                return False 


def main():

    P = project()
    P.get()
    
    project_id = sys.argv[1]
    project_id = str(project_id)

    if project_dic.has_key(project_id):
        P.disable(project_id)   
    
        P.show_vol(project_id)
        P.show_vol_snap(project_id)
        P.show_vm(project_id)
        P.show_image(project_id)
        P.show_subnet(project_id)
        P.show_net(project_id)
        P.show_all_port(project_id)
        P.show_dhcp_agent(project_id)
        P.show_router(project_id)
        P.show_secgroup(project_id)
        P.show_stack(project_id)
        P.shutdown_vm(project_id)
        P.reset_vol_status(project_id)
       
        P.del_vol_snap(project_id)
        P.del_vol(project_id)
        P.del_vm(project_id)
        P.del_image(project_id)
        P.del_router(project_id)
        P.remove_dhcp_agent()
        P.del_port(project_id)
        P.del_subnet(project_id)
        P.del_net(project_id)
        P.del_stack(project_id)
        P.del_secgroup(project_id)
        
        C = check()
        print "\n"
        print "\n"
        print "=>Starting Resource Check..."
        print "\n"

        P.show_vol(project_id)
        P.show_vol_snap(project_id)
        P.show_vm(project_id)
        P.show_image(project_id)
        P.show_router(project_id)
        P.show_all_port(project_id)
        P.show_subnet(project_id)
        P.show_net(project_id)
        P.show_secgroup(project_id)
        P.show_stack(project_id)

	time.sleep(30)

        check_vol = C.vol(project_id)
        check_vol_snap = C.vol_snap(project_id)
        check_vm = C.vm(project_id)
        check_subnet = C.subnet(project_id)
        check_net = C.net(project_id)
        check_port = C.port(project_id)
        check_image = C.image(project_id)
        check_stack = C.stack(project_id)
        check_secgroup = C.secgroup(project_id)
        check_router = C.router(project_id) 
  
        if (check_vm and check_vol and check_vol_snap and check_subnet and check_net and check_port and check_image and check_stack and check_secgroup and check_router):
            P.show_user(project_id)
            P.del_user(project_id)
            print "\n"
            print "All resources have been cleaned up..."
            print "\n"
            os.system("openstack project delete %s" % (project_id))
            print "Project %s deleted successfully!" % (project_id)
            print "\n"
        else:
            print "\n"
            print "Some resources are not cleared. Please manaully clear according to the information shown above..."
            print "\n"

    else:
        print "%s does not exist!" % (project_id) 
        sys.exit(10)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\n"
        print ">>>ERROR:lost project id"
        print "\n"
        print "Usage:%s project_id" % (sys.argv[0])
        print "\n"
        sys.exit(100)
    else:
        main()
