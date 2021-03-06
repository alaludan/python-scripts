#!/usr/bin/python
#-*-coding:utf-8-*-

# This tool will automatically clear the specified project all the volume, vm,
# image,network, net, stack, and then delete the user, the final need to 
# manually delete the project!                                                                      
#                                                                                   
#                                              -----Developer by Yupeng Luo       
#                                              -----Mail:yupeng.luo@nokia-sbell.com 
#


import os
import sys
import time

project_dic = {}
vol_id_list = []
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

check_vm = check_vol = check_subnet = check_net = check_port = check_image = check_stack = check_secgroup = check_router = True 

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
        # retrun a dictionary that containing project information
        info = os.popen("openstack project list -f value")
        project_info = info.readlines()
        for project in project_info:
            project = str(project).strip()
            project_name = project.split(" ")[1]
            project_id = project.split(" ")[0]
            project_dic[project_id] = project_name
        return project_dic

    def disable(self,project_id):
        # disable project
        if project_dic.has_key(project_id):
            project_id = project_dic[project_id]
            os.system("openstack project set --disable %s" % (project_id))
            title = "Disable Project"
            content = project_id + " " + "disable succeessful"
            print "\n"
            print title.center(100,'*')
            print "*" + " "*98 + "*"
            print "*" + " "*98 + "*"
            print content.center(100,"*")
            print "*" + " "*98 + "*"
            print "*" + " "*98 + "*"
            print "*"*100
            print "\n"
        else:
            print "%s does not exist" % (project_id)
            sys.exit(10)

    def show_user(self,project_id):
        # return an user_id list of project 
        print "\n"
        print "=>Show All Users of %s..." % (project_id)
        os.system("openstack user list --project %s|grep -v -w admin" % (project_id))
        user_info = os.popen("openstack user list -f value -c ID -c Name --project %s |grep -v -w admin" % (project_id))
        user_ids = user_info.readlines()
        for user_id in user_ids:
            user_id = str(user_id).strip().split(" ")[0]
            user_id_list.append(user_id)
        return user_id_list

    def show_vol(self,project_id):
        # return a volume_id list of project
        print "\n"
        print "=>Show All Volumes Of %s..." % (project_id)
        os.system("cinder list --tenant %s" % (project_id))
        print "\n"
        vol_info =  os.popen("cinder list --tenant %s|awk -F'|' '{print $2}'|awk 'NR>2'|awk NF" % (project_id))
        vol_ids = vol_info.readlines()
        for vol_id in vol_ids:
            vol_id = str(vol_id).strip()
            vol_id_list.append(vol_id)
        return vol_id_list
        
    def show_vm(self,project_id):
        # return a instance_id list of project
        print "\n"
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
        # return a image_id list of project
        print "\n"
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
        # return a subnet_id list of project
        print "\n"
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

    def show_all_port(self,project_id):
        # return a port_id list of project
        all_port_info = os.popen("neutron port-list -f value -c id -c security_groups -c tenant_id |grep %s|awk -F' ' '{print $1}'" % (project_id))
        all_port_ids = all_port_info.readlines()
        for all_port_id in all_port_ids:
            all_port_id = str(all_port_id).strip()
            all_port_id_list.append(all_port_id)
           
        for subnet_id in subnet_id_list:
            subnet_port_info = os.popen("neutron port-list|grep %s|awk -F'|' '{print $2}'" % (subnet_id))
            subnet_port_ids = subnet_port_info.readlines()
            for subnet_port_id in subnet_port_ids:
                subnet_port_id = str(subnet_port_id).strip()
                all_port_id_list.append(subnet_port_id) 
        return all_port_id_list

    def show_net(self,project_id):
        # return a network_id list of project
        print "\n"
        print "=>Show All Networks Of %s..." % (project_id)
        os.system("neutron net-list --tenant-id %s" % (project_id))
        print "\n"
        net_info = os.popen("neutron net-list --tenant-id %s -f value -c id" % (project_id))
        net_ids = net_info.readlines()
        for net_id in net_ids:
            net_id = str(net_id).strip()
            net_id_list.append(net_id)
        return net_id_list

    def show_dhcp_agent(self,project_id):
        # return a dhcp_agent_id list of project
        print "\n"
        print "=>Show All DHCP_AGENT of %s..." % (project_id)
        os.system("neutron agent-list|grep DHCP")
        print "\n"
        dhcp_agent_info = os.popen("neutron agent-list|grep dhcp|awk -F '|' '{print $2}'")
        dhcp_agent_ids = dhcp_agent_info.readlines()
        for dhcp_agent_id in dhcp_agent_ids:
            dhcp_agent_id = str(dhcp_agent_id).strip()
            dhcp_agent_id_list.append(dhcp_agent_id)
        return dhcp_agent_id_list

    def show_router(self,project_id):
        # return a route_id list of project
        print "\n"
        print "=>Show All Routers Of %s..." % (project_id)
        os.system("openstack router list|grep %s" % (project_id))
        print "\n"
        router_info = os.popen("openstack router list|grep %s|awk -F'|' '{print $2}'" % (project_id))
        router_ids = router_info.readlines()
        for router_id in router_ids:
            router_id = str(router_id).strip()
            router_id_list.append(router_id)
        return router_id_list
            
    def show_secgroup(self,project_id):
        # return a security group id list of project
        print "\n"
        print "=>Show All Secgroups Of %s..." % (project_id)
        os.system("nova secgroup-list --all-tenants|grep %s" % (project_id))
        print "\n"
        secgroup_info = os.popen("nova secgroup-list --all-tenants|grep %s|awk -F'|' '{print $2}'" % (project_id))
        secgroup_ids = secgroup_info.readlines()
        for secgroup_id in secgroup_ids:
            secgroup_id = str(secgroup_id).strip()
            secgroup_id_list.append(secgroup_id)
        return secgroup_id_list 

    def show_stack(self,project_id):
        # return a stack_id list of project
        print "\n"
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
        # reset volume status to "available" and attach-status to "detached"
        print "\n"
        print "=>Reset Volume..."
        print "\n"
        for vol_id in vol_id_list:
            os.system("cinder reset-state --state available --attach-status detached %s" % (vol_id))
            print "Reset status for VM:%s" % (vol_id)
            time.sleep(2)
        print "\n"
        print "\n"

    def shutdown_vm(self,project_id):
        # shutdown all instances
        print "\n"
        print "=>Shutdown All VMs of %s..." % (project_id)
        print "\n"
        for vm in vm_id_list:
            os.system("openstack server stop %s" % (vm))
            print "Stop VM:%s" % (vm)
            time.sleep(10)
        print "\n"
        print "\n"
        
    def del_vol(self,project_id):
        # delete all volumes
        print "\n"
        print "=>Delete All Volumes of %s..." % (project_id)
        print "\n"
        for vol_id in vol_id_list:
            os.system("openstack volume delete %s" % (vol_id))
            print "Delete Volume:%s" % (vol_id)
            time.sleep(10)
        print "\n"
        print "\n"

    def del_vm(self,project_id):
        # delete all instances
        print "\n"
        print "=>Delete All VMs of %s..." % (project_id)
        print "\n"
        for vm in vm_id_list:
            os.system("openstack server delete %s" % (vm))
            print "Delete VM:%s" % (vm)
            time.sleep(10)
        print "\n"
        print "\n"

    def del_image(self,project_id):
        # delete all images 
        print "\n"
        print "=>Delete All Images Of %s..." % (project_id)
        print "\n"
        for image in image_id_list:
            os.system("glance image-update --is-protected False %s" % (image))
            os.system("glance image-delete %s" % (image))
            print "Delete image:%s" % (image)
            time.sleep(2)
        print "\n"
        print "\n"

    def del_router(self,project_id):
        # delete all routers
        print "\n"
        print "=>Delete All routers of %s" % (project_id)
        for router_id in router_id_list:
            router_port_info = os.popen("neutron router-port-list %s -f value -c id" % (router_id)) 
            router_port_ids = router_port_info.readlines()
            for router_port_id in router_port_ids:
                os.system("neutron router-interface-delete %s port=%s" % (router_id,router_port_id))
                time.sleep(2)
            os.system("neutron router-delete %s" % (router_id))
            print "Delete router:%s" % (router_id)

    def remove_dhcp_agent(self):
        # remove all dhcp_agent from network
        print "\n"
        for dhcp_agent_id in dhcp_agent_id_list:
            for net_id in net_id_list:
                os.system("neutron dhcp-agent-network-remove %s %s" % (dhcp_agent_id,net_id))
                time.sleep(2)

    def del_port(self,project_id):
        # delete all ports
        print "\n"
        print "=>Delete All ports of %s" % (project_id)
        for port_id in all_port_id_list:
            os.system("neutron port-delete %s" % (port_id))
            time.sleep(2)

    def del_subnet(self,project_id):
        # delete all subnets
        print "\n"
        print "=>Delete All subnets of %s" % (project_id)

        for subnet_id in subnet_id_list:
            os.system("openstack subnet delete %s" % (subnet_id))
            time.sleep(2)
            print "Delete subnet:%s" % (subnet_id)

    def del_net(self,project_id):
        # delete all networks
        print "\n"
        print "=>Delete All Networks Of %s..." % (project_id)
        print "\n"
        for net_id in net_id_list:
            os.system("openstack network delete %s" %(net_id))
            print "Delete network:%s" % (net_id)
            time.sleep(2)
        print "\n"
        print "\n"

    def del_secgroup(self,project_id):
        # delete all security groups
        print "\n"
        print "=>Delete All Secgroups Of %s..." % (project_id)
        print "\n"
        for secgroup_id in secgroup_id_list:
            os.system("nova secgroup-delete %s" %(secgroup_id))
            print "Delete secgroup:%s" % (secgroup_id)
            time.sleep(2)
        print "\n"
        print "\n"

    def del_user(self,project_id):
        # delete all users
        print "\n"
        print "=>Delete All Users of %s..." % (project_id)
        print "\n"
        for user_id in user_id_list:
            os.system("openstack user delete %s" % (user_id))
            print "Delete user:%s" % (user_id)
            time.sleep(2)
        print "\n"
        print "\n"

    def del_stack(self,project_id):
        # delete all stacks
        print "\n"
        print "=>Delete All Stacks of %s..." % (project_id)
        print "\n"
        for stack_id in stack_id_list:
            os.system("openstack stack delete %s --yes" % (stack_id))
            print "Delete Stack:%s" % (stack_id)
            time.sleep(40)
        print "\n"
        print "\n"

class check:

    def vol(self,project_id):
        # check if all volumes of project were deleted
        after_del_vol_id_list = []
        after_del_vol_info =  os.popen("cinder list --tenant %s|awk -F'|' '{print $2}'|awk 'NR>2'|awk NF" % (project_id))
        after_del_vol_ids = after_del_vol_info.readlines()
        for after_del_vol_id in after_del_vol_ids:
            after_del_vol_id = str(after_del_vol_id).strip()
            after_del_vol_id_list.append(after_del_vol_id)

        if len(after_del_vol_id_list) == 0:
            print "Volume Clean up"
            print "\n"
            return True
        else:
            for after_del_vol_id in after_del_vol_id_list:
                print "Volume:%s does not delete,Please check!" % (after_del_vol_id)
                print "\n"
                return False

    def vm(self,project_id):
        # check if all instances of project were deleted        
        after_del_vm_id_list = []
        after_del_info =  os.popen("cinder list --tenant %s|awk -F'|' '{print $2}'|awk 'NR>2'|awk NF" % (project_id))
        after_del_vm_ids = after_del_info.readlines()
        for after_del_vm_id in after_del_vm_ids:
            after_del_vm_id = str(after_del_vm_id).strip()
            after_del_vm_id_list.append(after_del_vm_id)

        if len(after_del_vm_id_list) == 0:
            print "VM Clean up"
            print "\n"
            return True
        else:
            for after_del_vm_id in after_del_vm_id_list:
                print "VM:%s does not delete,Please check!" % (after_del_vm_id)
                print "\n"
                return False

    def subnet(self,project_id):
        # check if all subnets of project were deleted
        after_del_subnet_id_list = []
        after_del_subnet_info = os.popen("openstack subnet list --long -f value -c ID -c Project|grep %s" % (project_id))
        after_del_subnet_ids = after_del_subnet_info.readlines()
        for after_del_subnet_id in after_del_subnet_ids:
            after_del_subnet_id = str(after_del_subnet_id).strip().split(" ")[0]
            after_del_subnet_id_list.append(after_del_subnet_id)

        if len(after_del_subnet_id_list) == 0:
            print "Subnet Clean up"
            print "\n"
            return True
        else:
            for after_del_subnet_id in after_del_subnet_id_list:
                print "Subnet:%s does not delete,Please check!" % (after_del_subnet_id)
                print "\n"
                return False

    def secgroup(self,project_id):
        # check if all security groups of project were deleted
        after_del_secgroup_id_list = []
        after_del_secgroup_info = os.popen("nova secgroup-list --all-tenants|grep %s|awk -F'|' '{print $2}'" % (project_id))
        after_del_secgroup_ids = after_del_secgroup_info.readlines()
        for after_del_secgroup_id in after_del_secgroup_ids:
            after_del_secgroup_id = str(after_del_secgroup_id).strip()
            after_del_secgroup_id_list.append(after_del_secgroup_id)

        if len(after_del_secgroup_id_list) == 0:
            print "Secgroup Clean up"
            print "\n"
            return True
        else:
            for after_del_secgroup_id in after_del_secgroup_id_list:
                print "Secgroup:%s does not delete,Please check!" % (after_del_secgroup_id)
                print "\n"
                return False
    
    def router(self,project_id):
        # check if all routers of project were deleted
        after_del_router_id_list = []     
        after_del_router_info = os.popen("openstack router list|grep %s|awk -F'|' '{print $2}'" % (project_id))
        after_del_router_ids = after_del_router_info.readlines()
        for after_del_router_id in after_del_router_ids:
            after_del_router_id = str(after_del_router_id).strip()
            after_del_router_id_list.append(after_del_router_id)

        if len(after_del_router_id_list) == 0:
            print "Routers Clean up"
            print "\n"
            return True
        else:
            for after_del_router_id in after_del_router_id_list:
                print "Routers:%s does not delete,Please check!" % (after_del_router_id)
                print "\n"
                return False

    def net(self,project_id):
        # check if all networks of project were deleted
        after_del_net_id_list = []
        after_del_net_info = os.popen("neutron net-list --tenant-id %s -f value -c id" % (project_id))
        after_del_net_ids = after_del_net_info.readlines()
        for after_del_net_id in after_del_net_ids:
            after_del_net_id = str(after_del_net_id).strip()
            after_del_net_id_list.append(after_del_net_id)
        if len(after_del_net_id_list) == 0:
            print "Network Clean up"
            print "\n"
            return True
        else:
            for after_del_net_id in after_del_net_id_list:
                print "Network:%s does not delete,Please check!" % (after_del_net_id)
                print "\n"
                return False

    def port(self,project_id):
        # check if all ports of project were deleted
        after_del_port_id_list = []
        for subnet_id in subnet_id_list:
            after_del_port_info = os.popen("neutron port-list -f value -c id -c security_groups -c tenant_id |grep %s|awk -F' ' '{print $1}'" % (subnet_id))
            after_del_port_ids = after_del_port_info.readlines()
            for after_del_port_id in after_del_port_ids:
                after_del_port_id = str(after_del_port_id).split(" ")[0]
                after_del_port_id_list.append(after_def_port_id)

        if len(after_del_port_id_list) == 0:
            print "Port Clean up"
            print "\n"
            return True
        else:
            for after_del_port_id in after_del_port_id_list:
                print "Port:%s does not delete,Please check!" % (after_del_port_id)
                print "\n"
                return False

    def image(self,project_id):
        # check if all images of project were deleted
        after_del_image_id_list = []
        after_del_image_info = os.popen("glance image-list --owner %s|awk -F'|' '{print $2}'|awk 'NR>2'|awk NF" % (project_id))
        after_del_image_ids = after_del_image_info.readlines()
        for after_del_image_id in after_del_image_ids:
            after_del_image_id = str(after_del_image_id).strip()
            after_del_image_id_list.append(after_del_image_id)

        if len(after_del_image_id_list) == 0:
            print "Image Clean up"
            print "\n"
            return True
        else:
            for after_del_image_id in after_del_image_id_list:
                print "Image:%s does not delete,Please check!" % (after_del_image_id)
                print "\n"
                return False

    def stack(self,project_id):
        # check if all stacks of project were deleted
        after_del_stack_id_list = []
        after_del_stack_info = os.popen('openstack stack list --all-project -f value -c ID -c "Stack Name" -c Project|grep %s' % (project_id))
        after_del_stack_ids = after_del_stack_info.readlines()
        for after_del_stack_id in after_del_stack_ids:
            after_del_stack_id = str(after_del_stack_id).strip().split(" ")[0]
            after_del_stack_id_list.append(after_del_stack_id)

        if len(after_del_stack_id_list) == 0:
            print "Stack Clean up"
            print "\n"
            return True
        else:
            for after_del_stack_id in after_del_stack_id_list:
                print "Stack:%s does not delete,Please check!" % (after_del_stack_id)
                print "\n"
                return False 


def main():
    
    P = project()
    P.get()
    
    os.system("openstack project list")
    print "\n"
    project_id = raw_input("Please enter project id that will be delete:")
    project_id = str(project_id)

    if project_dic.has_key(project_id):
        answer = raw_input("Please confirm delete project:%s  (yes/no)" % (project_id))
        if answer == "yes" or answer == "Yes" or answer == "YES" or answer == "y":
            P.disable(project_id)   
    
            P.show_vol(project_id)
            P.show_vm(project_id)
            P.show_image(project_id)
            P.show_subnet(project_id)
            P.show_all_port(project_id)
            P.show_net(project_id)
            P.show_dhcp_agent(project_id)
            P.show_router(project_id)
            P.show_secgroup(project_id)
            P.show_stack(project_id)
            P.shutdown_vm(project_id)
            P.reset_vol_status(project_id)
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
            P.show_vm(project_id)
            P.show_image(project_id)
            P.show_router(project_id)
            P.show_subnet(project_id)
            P.show_all_port(project_id)
            P.show_net(project_id)
            P.show_secgroup(project_id)
            P.show_stack(project_id)

            check_vol = C.vol(project_id)
            check_vm = C.vm(project_id)
            check_subnet = C.subnet(project_id)
            check_net = C.net(project_id)
            check_port = C.port(project_id)
            check_image = C.image(project_id)
            check_stack = C.stack(project_id)
            check_secgroup = C.secgroup(project_id)
            check_router = C.router(project_id) 
  
            if (check_vm and check_vol and check_subnet and check_net and check_port and check_image and check_stack and check_secgroup and check_router):
                P.show_user(project_id)
                P.del_user(project_id)
                print "\n"
                print "All resources have been cleaned up,Please use the following command to delete project by manually..."
                print "\n"
                print "openstack project delete %s" % (project_id)
                print "\n"
            else:
                print "\n"
                print "Some resources are not cleared. Please manaully clear according to the information shown above..."
                print "\n"

        else:
            sys.exit(1)
    else:
        print "%s does not exist!" % (project_id) 
        sys.exit(10)

if __name__ == '__main__':
    main()
