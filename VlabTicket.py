#coding:utf-8
import urllib
import urllib2
import cookielib
import ssl
import re
import HTMLParser
import xlwt
import os
import sys
import win32com.client
from win32com.client import Dispatch, Constants

class Spider:
    
    def __init__(self, url, loginUrl, **headers):
        self.url =  url
        self.loginUrl = loginUrl
        self.headers = headers
    
    def getData(self, loginUrl, loginData):
        global data
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        
        urllib2.urlopen(loginUrl)
        
        for cookie in enumerate(cj):
            csr = str(cookie)
            str1 =  csr.split(",")[2].split("=")[1].strip("'")
            str2 = csr.split(",")[3].split("=")[1].strip("'")
            str3 =  str1 + "=" + str2
            csrList.append(str3)
            
        csr =  csrList[1] + "; " + csrList[0]        
        
        for key in self.headers:
            opener.addheaders.append((key, self.headers[key]))
        
        ticketNumReg = r'data-issuekey="(.*?)"'
        ticketNumLinkReg = r'<td class="issuetype">.*?ref="(.*?)">'
        ticketAssigneeReg =  r'id="assignee_.*?>(.*?)</a>'
        ticketCreatetimeReg = r'<time datetime=".*?>(.*?)</time>'
        ticketStatusReg = r'&lt;/span&gt;">(.*?)</span>'
        ticketSummaryReg =  r'<td class="summary"><p>\n*.*?>(.*?)</a>'
        ticketReporterReg = r'id="reporter.*?>(.*?)</a>'
        ticketResolutionReg = r'<em>(.*?)</em>'
        ticketAffectsReg = r'<td class="versions">(.*?)\s</td>'
        ticketTypeReg =  r'avatarType=issuetype" height="16" width="16" border="0" align="absmiddle" alt="(.*?)"'
        loginData = urllib.urlencode(loginData)
        
        opener.open(loginUrl,loginData)
        #content = opener.open('https://greenhopper.app.alcatel-lucent.com/issues/?filter=54652').read()
        content = opener.open('https://greenhopper.app.alcatel-lucent.com/issues/?filter=60219').read()
        #print content
        
        ticketNum = re.findall(ticketNumReg, content)
        ticketNumLink = re.findall(ticketNumLinkReg, content)
        ticketAssigneeName =  re.findall(ticketAssigneeReg, content)
        ticketCreatetime =  re.findall(ticketCreatetimeReg, content)
        ticketStatus =  re.findall(ticketStatusReg, content)
        ticketSummary =  re.findall(ticketSummaryReg, content)
        ticketReporter = re.findall(ticketReporterReg, content)
        ticketResolution =  re.findall(ticketResolutionReg, content)
        ticketAffects =  re.findall(ticketAffectsReg, content)
        ticketType =  re.findall(ticketTypeReg, content)
        
        html_parser =  HTMLParser.HTMLParser()
        
        for summary in ticketSummary:
            summary = html_parser.unescape(summary)
            ticketSummaryUnescape.append(summary)
        
        #data =  zip(ticketAssigneeName, ticketCreatetime, ticketNum, ticketNumLink, ticketStatus, ticketSummaryUnescape, ticketReporter, ticketResolution, ticketAffects, ticketType)
        data =  zip(ticketAssigneeName, ticketCreatetime,ticketType, ticketNum, ticketNumLink, ticketAffects, ticketStatus, ticketSummaryUnescape, ticketReporter, ticketResolution)
              
    
    def saveToExcel(self, filename):
        global data
        style =  xlwt.XFStyle()
        font =  xlwt.Font()
        font.colour_index = 0x0c
        style.font =  font       
        
        i = 1
        book =  xlwt.Workbook()
        sheet1 =  book.add_sheet("VlabTicket")
        #head =  ['Assignee', 'Created', 'TicketNum', 'Status', 'Summary', 'Reporter', 'Resolution', 'Affects Version']
        head =  ['Assignee', 'Created', 'TicketType','TicketNum', 'Affects Version', 'Status', 'Summary', 'Reporter', 'Resolution']
        
        Assignee_col = sheet1.col(0)
        Assignee_col.width = 256 * 30
        Creted_col = sheet1.col(1)
        Creted_col.width = 256 * 10
        TiecktType_col = sheet1.col(2)
        TiecktType_col.width = 256 * 20       
        TicketNum_col = sheet1.col(3)
        TicketNum_col.width = 256 * 20
        Affects_col = sheet1.col(4)
        Affects_col.width = 256 * 14          
        Status_col = sheet1.col(5)
        Status_col.width = 256 * 10
        Summary_col =  sheet1.col(6)
        Summary_col.width = 256 * 80
        Reporter_col = sheet1.col(7)
        Reporter_col.width = 256 * 35
        Resolution_col = sheet1.col(8)
        Resolution_col.width = 256 * 12
        
        for h in range(len(head)):
            sheet1.write(0, h, head[h])
        i = 1
            
        for name in data:
            sheet1.write(i, 0, name[0])
            i += 1
        i = 1
        
        for time in data:
            sheet1.write(i, 1, time[1])
            i += 1
        i = 1
        
        for tickettype in data:
            sheet1.write(i, 2, tickettype[2])
            i += 1
        i = 1
        
        for ticketnum in data:
            link =  url + ticketnum[4]
            sheet1.write(i, 3, xlwt.Formula("HYPERLINK"+'("'+link+'";"'+ticketnum[3]+'")'), style)
            i +=  1
        i = 1
        
        for affects in data:
            affects_info =  affects[5].strip()
            if affects_info == "&nbsp;":
                affects_info = " "
            sheet1.write(i, 4, affects_info)
            i +=  1
        i = 1
        
        for status in data:
            sheet1.write(i, 5, status[6])
            i +=  1
        i = 1
        
        for summary in data:
            sheet1.write(i, 6, summary[7])
            i +=  1
        i = 1
        
        for reporter in data:
            sheet1.write(i, 7, reporter[8])
            i +=  1
        i = 1
        
        for resolution in data:
            sheet1.write(i, 8, resolution[9])
            i +=  1
        i = 1
        
        book.save(filename)
        print "%s save ok..." %  (filename)
            
def sendmail(filename):
    sub = 'outlook python mail test'
    body = 'Hi All\n\rHere are the information about tickets ongoing.The scan will be run every working day and mail will be sent on morning. Thanks'
    outlook = win32com.client.Dispatch('outlook.application')
    receivers =  ['cn-lab@list.nokia.com']
    mail = outlook.CreateItem(0)
    mail.To = receivers[0]
    mail.Subject = sub.decode('utf-8')
    mail.Body = body.decode('utf-8')
    filepath = sys.path[0] + "\\" + filename
    mail.Attachments.Add(filepath)
    mail.Send()
    print "mail send ok..."
            
def main():
    WebSpider =  Spider(url, loginUrl, **headers)
    WebSpider.getData(loginUrl, loginData)
    filename = "VlabTicket.xls"
    WebSpider.saveToExcel(filename)
    sendmail(filename)

if __name__ == '__main__':
    csrList = []
    ticketSummaryUnescape =  []
    data =  []
    ssl._create_default_https_context = ssl._create_unverified_context
    
    url =  'https://greenhopper.app.alcatel-lucent.com'
    loginUrl =  'https://greenhopper.app.alcatel-lucent.com/login.jsp'
    headers = {"Origin": "https://greenhopper.app.alcatel-lucent.com",
           "Referer":"https://greenhopper.app.alcatel-lucent.com/login.jsp",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
    loginData = {"os_username":"yupenglu",
                      "os_password":"lyp#12Xz6",
                      "os_destination":"",
                      "user_role":"",
                      "atl_token":"",
                      "login":"Log In"}
    
    main()

        
        

