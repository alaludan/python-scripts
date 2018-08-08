#!/usr/bin/python
import os
import sys
import getopt
import paramiko
import time

pcscmd = ['salt "`alias|grep o=|awk -F" " \'{print $3}\'|sed "s/.$//"`*" cmd.run "pcs status | grep topped -n3 && pcs status | grep -i mana"']
cephcmd = ['salt "`alias|grep o=|awk -F" " \'{print $3}\'|sed "s/.$//"`*" cmd.run "ceph health detail"']
openstackcmd = ['source /home/stack/overcloudrc && nova service-list|grep down && neutron agent-list|grep xxx && cinder service-list']
ceph_health = ""

def usage():
    print """ 
          *********************************************
          * Usage:                                    *
          *                                           *
          * vlabcheck.py -c <u|p>                     *
          *                                           *
          * -c u:Check the VLAB running status of USA.*
          *                                           *
          * -c p:Check the VLAB running status of PL. *
          *                                           *
          *********************************************
          """

def get_hostname(ip,username,passwd,cmd):
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    ssh.connect(ip,22,username,passwd,timeout=5) 
    cmd = ['alias|grep o= |awk -F" " "{print $3}"']
    hostname = cmd.strip()
    return hostname
        

def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
	ssh.connect(ip,22,username,passwd,timeout=5) 
	for m in cmd:
	    stdin,stdout,stderr = ssh.exec_command(m)
	    out = stdout.readlines()

	    for o in out:
		print o
        return 0
	ssh.close()

    except:
        return 1

def ceph_ssh(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
	ssh.connect(ip,22,username,passwd,timeout=5) 
	for m in cmd:
	    stdin,stdout,stderr = ssh.exec_command(m)
	    out = stdout.readlines()

	    for o in out:
                if "HEALTH_WARN" in o:
                    ceph_health = "HEALTH_WARN"
                elif "HEALTH_ERROR" in o:
                    ceph_health = "HEALTH_ERROR"
                elif "HEALTH_OK" in o:
                    ceph_health = "HEALTH_OK"
                print o
            return ceph_health 
	ssh.close()

    except:
        return 1

def op_ssh(ip,username,passwd,cmd,nodename):
    try:
        ssh = paramiko.SSHClient()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
	ssh.connect(ip,22,username,passwd,timeout=5) 
        str_list = []
	for m in cmd:
	    stdin,stdout,stderr = ssh.exec_command(m)
	    out = stdout.readlines()

	    for o in out:
                o = str(o)
                print o
                str_list.append(o)
        return str_list
	ssh.close()

    except:
        str_list = ["ERROR"]
        return str_list

def check(vlabinfo):
    os.system("echo '' > vlabcheck.log")
    with open(vlabinfo,"r") as f:
        lines = f.readlines()
        for line in lines:
            info = line.split(":")
            nodename = info[0]
            ip = info[1].strip()
            username = info[2].strip()
            passwd = info[3].strip()

            print "\n"
            print ("\033[1;44m%s\t%s\tpcs status check\033[0m") % (nodename,ip)
            pcsstatus = ssh2(ip,username,passwd,pcscmd)
            if pcsstatus == 0:
                print ('\033[1;32m%s\t%s pcs status ok\033[0m') % (nodename,ip)
            else:
                print ("\033[1;31m%s\t%s pcs status error\033[0m") % (nodename,ip)
                with open("vlabcheck.log","a") as fc:
                    errorinfo = "%s\t%s pcs status error" % (nodename,ip)
                    fc.writelines(errorinfo+"\n")
            print "\n"

            print ("\033[1;44m%s\t%s\tceph status check\033[0m") % (nodename,ip)
            cephstatus = ceph_ssh(ip,username,passwd,cephcmd)
            if cephstatus == "HEALTH_OK":
                print ("\033[1;32m%s\t%s ceph HEALTH_OK\033[0m") % (nodename,ip)
            elif cephstatus == "HEALTH_WARN":
                print ("\033[1;33m%s\t%s ceph HEALTH_WARN\033[0m") % (nodename,ip)
                with open("vlabcheck.log","a") as fc:
                    errorinfo = "%s\t%s ceph HEALTH_WARN" % (nodename,ip)
                    fc.writelines(errorinfo+"\n")
            elif cephstatus == "HEALTH_ERROR":
                print ("\033[1;31m%s\t%s ceph HEALTH_ERROR\033[0m") % (nodename,ip)
                with open("vlabcheck.log","a") as fc:
                    errorinfo = "%s\t%s ceph HEALTH_ERROR" % (nodename,ip)
                    fc.writelines(errorinfo+"\n")
            else:
                print ("\033[1;31m%s\t%s ceph status error\033[0m") % (nodename,ip)
                with open("vlabcheck.log","a") as fc:
                    errorinfo = "%s\t%s ceph status error" % (nodename,ip)
                    fc.writelines(errorinfo+"\n")
            print "\n"

	    print ("\033[1;44m%s\t%s\topenstack status check\033[0m") % (nodename,ip)
            opstatus = op_ssh(ip,username,passwd,openstackcmd,nodename)
            if len(opstatus) == 0:
                print ("\033[1;32m%s\t%s openstack status ok\033[0m") % (nodename,ip)
            else:
                print ("\033[1;31m%s\t%s openstack status error\033[0m") % (nodename,ip)
                with open("vlabcheck.log","a") as fv:
                    errorinfo = "%s\t%s openstack status error" % (nodename,ip)
                    fv.writelines(errorinfo+"\n")
            print "\n"

def main():
    try: 
        opts,args = getopt.getopt(sys.argv[1:],"hc")
        filePath = os.path.dirname(__file__)
        fileNamePath = os.path.split(os.path.realpath(__file__))[0]
        if len(args) != 1:
            usage()
            sys.exit()

        for opt,arg in opts:
            if opt in ('-h'):
                usage()
                sys.exit()
            elif opt in ('-c') and "u" in args: 
                vlabinfo = os.path.join(fileNamePath,'uslist')
                check(vlabinfo)
            elif opt in ('-c') and "p" in args:
                vlabinfo = os.path.join(fileNamePath,'pllist')
                check(vlabinfo)
            else:
                usage()
                sys.exit()
               
    except getopt.GetoptError:
        usage()
        sys.exit()

if __name__ == '__main__':
    main()
