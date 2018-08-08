#!/usr/bin/python
import re, sys, time, os
import pexpect
from pexpect import pxssh


os.system('rm -rf list pass pass1 pass2 pass3 pass4 ucip uslist')

host = 'burp.vlab.us.alcatel-lucent.com'
user = 'vlab'
password = 'Sp1d3rm@n'

def connect(hostname,username,password):
    try:
        s = pxssh.pxssh()
        s.login(host,user,password)
        return s
        print s
    except Exception, e:
        print "[-] Error Connecting:" + str(e)

def send_command(ssh_session, command):
    ssh_session.sendline(command)
    ssh_session.prompt()
    f=open('pass','a')
    print >>f,ssh_session.before
    f.close()

def delblankline(infile,outfile):
    infopen = open(infile,'r')
    outfopen = open(outfile,'w')
    lines = infopen.readlines()
    for line in lines:
        if line.split():
            outfopen.writelines(line)
        else:
            outfopen.writelines("")
    infopen.close()
    outfopen.close()

session = connect(host,user,password)

def main():
    send_command(session,command)




f=open('nodenumber','r')
for line in f.readlines():
    num=str(line)
    num=num.strip('\n')
    command = 'ssh  -q -p 5522 vlabssh@pw.vlab.us.alcatel-lucent.com RETRIEVE --resource=' + num + '_UC --account=stack'

    main()


lines = []
f = open('pass')
for line in f.readlines():
    if not re.search('RETRIEVE', line):
        lines.append(str(line))
f.close()

f = open('pass1', 'a')
f.writelines(lines)
f.close()

delblankline("pass1","pass2")

b=open('undercloud', 'r')
ip=list(b)
f=open('ucip','w')
print>>f, ':'.join(ip)
f.close()

f=open('pass2','r')
stac=list(f)
f1=open('pass3','w')
print>>f1, ':stack:'.join(stac)
f1.close()
f.close()


f = open('pass3','r')
for line in f.readlines():
    line=line[:-3]
    f1 = open('pass4','a')
    print>>f1, line
    f1.close()
f.close()

os.system('paste -d "" nodenumber ucip pass4 > uslist')

l = len(open('uslist').readlines())
os.system('sed -i ' + str(l) + 'd uslist')
os.system('sed -i "1d" uslist')
os.system('rm -rf ucip pass pass1 pass2 pass3 pass4') 
