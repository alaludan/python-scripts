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

project_dic = {}
vol_id_list = []
vm_id_list = []
image_id_list = []
net_id_list = []
subnet_id_list = []
port_id_list = []
user_id_list = []
stack_id_list = []
project_name = ""
project_id = ""

check_vm = check_vol = check_subnet = check_net = check_port = check_image = check_stack = True 

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
        info = os.popen("openstack project list -f value")
        project_info = info.readlines()
        for project in project_info:
            project = str(project).strip()
            project_name = project.split(" ")[1]
            project_id = project.split(" ")[0]
            project_dic[project_name] = project_id
        return project_dic

    def disable(self,project_name):
        if project_dic.has_key(project_name):
            project_id = project_dic[project_name]
            os.system("openstack project set --name %s --disable %s" % (project_name,project_id))
            print "\n"
            print "****************************************Disable Project****************************************"
            print "*                                                                                             *"
            print "*                             %s disable succeessful                                  *" % (project_name)
            print "*                                                                                             *"
            print "***********************************************************************************************"
        else:
            print "%s does not exist" % (project_name)
            sys.exit(10)

    def show_user(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Show All Users of %s..." % (project_name)
        os.system("openstack user list --project %s|grep -v -w admin" % (project_id))
        user_info = os.popen("openstack user list -f value -c ID -c Name --project %s |grep -v -w admin" % (project_id))
        user_ids = user_info.readlines()
        for user_id in user_ids:
            user_id = str(user_id).strip().split(" ")[0]
            user_id_list.append(user_id)
        return user_id_list

    def show_vol(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Show All Volumes Of %s..." % (project_name)
        os.system("cinder list --tenant %s" % (project_id))
        print "\n"
        vol_info =  os.popen("cinder list --tenant %s|awk -F'|' '{print $2}'|awk 'NR>2'|awk NF" % (project_id))
        vol_ids = vol_info.readlines()
        for vol_id in vol_ids:
            vol_id = str(vol_id).strip()
            vol_id_list.append(vol_id)
        return vol_id_list
        
    def show_vm(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Show All VM Of %s..." % (project_name)
        os.system("openstack server list --project %s" % (project_id))
        print "\n"
        vm_info = os.popen("openstack server list --project %s -f value -c ID" % (project_id))
        vm_ids = vm_info.readlines()
        for vm_id in vm_ids:
            vm_id = str(vm_id).strip()
            vm_id_list.append(vm_id)
        return vm_id_list

    def show_image(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Show All Images Of %s..." % (project_name)
        os.system("glance image-list --owner %s" % (project_id))
        print "\n"
        image_info = os.popen("glance image-list --owner %s|awk -F'|' '{print $2}'|awk 'NR>2'|awk NF" % (project_id))
        image_ids = image_info.readlines()
        for image_id in image_ids:
            image_id = str(image_id).strip()
            image_id_list.append(image_id)
        return image_id_list

    def show_subnet(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Show All Subnets Of %s..." % (project_name)
        print "\n"
        os.system("openstack subnet list --long -f value -c ID -c Project -c Name|grep %s" % (project_id))
        print "\n"
        subnet_info = os.popen("openstack subnet list --long -f value -c ID -c Project|grep %s" % (project_id))
        subnet_ids = subnet_info.readlines()
        for subnet_id in subnet_ids:
            subnet_id = str(subnet_id).strip().split(" ")[0]
            subnet_id_list.append(subnet_id)
        return subnet_id_list

    def show_port(self):
        for subnet_id in subnet_id_list:
            port_info = os.popen("neutron port-list -f value -c id -c fixed_ips|grep %s" % (subnet_id))
            port_ids = port_info.readlines()
            for port_id in port_ids:
                port_id = str(port_id).split(" ")[0]
                port_id_list.append(port_id)
        return port_id_list

    def show_net(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Show All Networks Of %s..." % (project_name)
        os.system("neutron net-list --tenant-id %s" % (project_id))
        print "\n"
        net_info = os.popen("neutron net-list --tenant-id %s -f value -c id" % (project_id))
        net_ids = net_info.readlines()
        for net_id in net_ids:
            net_id = str(net_id).strip()
            net_id_list.append(net_id)
        return net_id_list
            
    def show_stack(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Show All Stacks Of %s..." % (project_name)
        print "\n"
        os.system('openstack stack list --all-project -f value -c ID -c "Stack Name" -c Project|grep %s' % (project_id))
        print "\n"
        stack_info = os.popen('openstack stack list --all-project -f value -c ID -c "Stack Name" -c Project|grep %s' % (project_id))
        stack_ids = stack_info.readlines()
        for stack_id in stack_ids:
            stack_id = str(stack_id).strip().split(" ")[0]
            stack_id_list.append(stack_id)
        return stack_id_list

    def reset_vol_status(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Reset Volume..."
        print "\n"
        for vol_id in vol_id_list:
            os.system("cinder reset-state --state available --attach-status detached %s" % (vol_id))
            print "Reset status for VM:%s" % (vol_id)
            time.sleep(5)
        print "\n"
        print "\n"
        #os.system("cinder list --tenant %s" % (project_id))

    def shutdown_vm(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Shutdown All VMs of %s..." % (project_name)
        print "\n"
        for vm in vm_id_list:
            os.system("openstack server stop %s" % (vm))
            print "Stop VM:%s" % (vm)
            time.sleep(10)
        print "\n"
        print "\n"
   
        
    def del_vol(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Delete All Volumes of %s..." % (project_name)
        print "\n"
        for vol_id in vol_id_list:
            os.system("openstack volume delete %s" % (vol_id))
            print "Delete Volume:%s" % (vol_id)
            time.sleep(10)
        print "\n"
        print "\n"
        #os.system("cinder list --tenant %s" % (project_id))

    def del_vm(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Delete All VMs of %s..." % (project_name)
        print "\n"
        for vm in vm_id_list:
            os.system("openstack server delete %s" % (vm))
            print "Delete VM:%s" % (vm)
            time.sleep(10)
        print "\n"
        print "\n"
        #os.system("openstack server list --project %s" % (project_id))

    def del_image(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Delete All Images Of %s..." % (project_name)
        print "\n"
        for image in image_id_list:
            os.system("glance image-update --is-protected False %s" % (image))
            os.system("glance image-delete %s" % (image))
            print "Delete image:%s" % (image)
            time.sleep(5)
        print "\n"
        print "\n"
        #os.system("glance image-list --owner %s" % (project_id))


    def del_subnet(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Delete All subnets and ports of %s" % (project_name)

        for subnet_id in subnet_id_list:
            port_info = os.popen("neutron port-list -f value -c id -c fixed_ips|grep %s" % (subnet_id))
            port_ids = port_info.readlines()
            for port_id in port_ids:
                port_id = str(port_id).split(" ")[0]
                os.system("openstack port delete %s" % (port_id))
                print "Delete port:%s" % (port_id)
                time.sleep(5)
            os.system("openstack subnet delete %s" % (subnet_id))
            print "Delete subnet:%s" % (subnet_id)


    def del_net(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Delete All Networks Of %s..." % (project_name)
        print "\n"
        for net_id in net_id_list:
            os.system("openstack network delete %s" %(net_id))
            print "Delete network:%s" % (net_id)
            time.sleep(5)
        print "\n"
        print "\n"
        #os.system("neutron net-list --tenant-id %s" % (project_id))

    def del_user(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Delete All Users of %s..." % (project_name)
        print "\n"
        for user_id in user_id_list:
            os.system("openstack user delete %s" % (user_id))
            print "Delete user:%s" % (user_id)
            time.sleep(5)
        print "\n"
        print "\n"
        #os.system("openstack user list --project %s" % (project_id))

    def del_stack(self,project_name):
        project_id = project_dic[project_name]
        print "\n"
        print "=>Delete All Stacks of %s..." % (project_name)
        print "\n"
        for stack_id in stack_id_list:
            os.system("openstack stack delete %s --yes" % (stack_id))
            print "Delete Stack:%s" % (stack_id)
            time.sleep(40)
        print "\n"
        print "\n"
        #os.system('openstack stack list --all-project -f value -c ID -c "Stack Name" -c Project|grep %s' % (project_id))
                    

class check:

    def vol(self,project_name):
        project_id = project_dic[project_name]

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

    def vm(self,project_name):
        project_id = project_dic[project_name]
                
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

    def subnet(self,project_name):
        project_id = project_dic[project_name]

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
            for after_del_subnet_id in after_delete_subnet_id_list:
                print "Subnet:%s does not delete,Please check!" % (after_del_subnet_id)
                print "\n"
                return False

    def net(self,project_name):
        project_id = project_dic[project_name]

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

    def port(self,project_name):
        project_id = project_dic[project_name]

        after_del_port_id_list = []
        for subnet_id in subnet_id_list:
            after_del_port_info = os.popen("neutron port-list -f value -c id -c fixed_ips|grep %s" % (subnet_id))
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

    def image(self,project_name):
        project_id = project_dic[project_name]

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

    def stack(self,project_name):
        project_id = project_dic[project_name]

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
    project_name = raw_input("Please enter project name that will be delete:")

    if project_dic.has_key(project_name):
        answer = raw_input("Please confirm delete project:%s  (yes/no)" % (project_name))
        if answer == "yes" or answer == "Yes" or answer == "YES" or answer == "y":
            P.disable(project_name)   
    
            P.show_vol(project_name)
            P.show_vm(project_name)
            P.show_image(project_name)
            P.show_subnet(project_name)
            P.show_port()
            P.show_net(project_name)
            P.show_stack(project_name)
            P.shutdown_vm(project_name)
            P.reset_vol_status(project_name)
            P.del_vol(project_name)
            P.del_vm(project_name)
            P.del_image(project_name)
            P.del_subnet(project_name)
            P.del_net(project_name)
            P.del_stack(project_name)


            C = check()
            print "\n"
            print "\n"
            print "=>Starting Resource Check..."
            print "\n"

            P.show_vol(project_name)
            P.show_vm(project_name)
            P.show_image(project_name)
            P.show_subnet(project_name)
            P.show_port()
            P.show_net(project_name)
            P.show_stack(project_name)

            check_vol = C.vol(project_name)
            check_vm = C.vm(project_name)
            check_subnet = C.subnet(project_name)
            check_net = C.net(project_name)
            check_port = C.port(project_name)
            check_image = C.image(project_name)
            check_stack = C.stack(project_name)
    
            print ""
     
    
            if (check_vm and check_vol and check_subnet and check_net and check_port and check_image and check_stack):
                P.show_user(project_name)
                P.del_user(project_name)
                print "\n"
                print "All resources have been cleaned up,Please use the following command to delete project by manually..."
                print "\n"
                print "openstack project delete %s" % (project_name)
                print "\n"
            else:
                print "\n"
                print "Some resources are not cleared. Please manaully clear according to the information shown above..."
                print "\n"
        else:
            sys.exit(1)
    else:
        print "%s does not exist!" % (project_name) 
        sys.exit(10)


if __name__ == '__main__':

    main()   
