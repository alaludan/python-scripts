#coding:utf-8
import os
import win32com.client
from win32com.client import Dispatch, Constants

def sendmail():
    sub = 'outlook python mail test'
    body = 'Hi All\n\rHere are the information about tickets ongoing.The scan will be run every working day and mail will be sent on morning. Thanks'
    outlook = win32com.client.Dispatch('outlook.application')
    receivers =  ['yupeng.luo@nokia-sbell.com']
    mail = outlook.CreateItem(0)
    mail.To = receivers[0]
    mail.Subject = sub.decode('utf-8')
    mail.Body = body.decode('utf-8')
    mail.Attachments.Add('C:\Users\yupenglu\Desktop\VlabTicket.xls')
    mail.Send()
    print "ok"
    
if __name__ == '__main__':
    sendmail()


