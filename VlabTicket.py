#coding:utf-8
import urllib
import urllib2
import cookielib
import ssl
import re
import HTMLParser
import xlwt

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
        
        loginData = urllib.urlencode(loginData)
        
        opener.open(loginUrl,loginData)
        content = opener.open('https://greenhopper.app.alcatel-lucent.com/issues/?filter=54652').read()
        
        ticketNum = re.findall(ticketNumReg, content)
        ticketNumLink = re.findall(ticketNumLinkReg, content)
        ticketAssigneeName =  re.findall(ticketAssigneeReg, content)
        ticketCreatetime =  re.findall(ticketCreatetimeReg, content)
        ticketStatus =  re.findall(ticketStatusReg, content)
        ticketSummary =  re.findall(ticketSummaryReg, content)
        ticketReporter = re.findall(ticketReporterReg, content)
        ticketResolution =  re.findall(ticketResolutionReg, content)
        
        html_parser =  HTMLParser.HTMLParser()
        
        for summary in ticketSummary:
            summary = html_parser.unescape(summary)
            ticketSummaryUnescape.append(summary)
        
        data =  zip(ticketAssigneeName, ticketCreatetime, ticketNum, ticketNumLink, ticketStatus, ticketSummaryUnescape, ticketReporter, ticketResolution)
              
    
    def saveToExcel(self, filename):
        global data
        style =  xlwt.XFStyle()
        font =  xlwt.Font()
        font.colour_index = 0x0c
        style.font =  font       
        
        i = 1
        book =  xlwt.Workbook()
        sheet1 =  book.add_sheet("VlabTicket")
        head =  ['Assignee', 'Created', 'TicketNum', 'Status', 'Summary', 'Reporter', 'Resolution']
        
        Assignee_col = sheet1.col(0)
        Assignee_col.width = 256 * 30
        Creted_col = sheet1.col(1)
        Creted_col.width = 256 * 10
        TicketNum_col = sheet1.col(2)
        TicketNum_col.width = 256 * 20
        Status_col = sheet1.col(3)
        Status_col.width = 256 * 10
        Summary_col =  sheet1.col(4)
        Summary_col.width = 256 * 80
        Reporter_col = sheet1.col(5)
        Reporter_col.width = 256 * 35
        Resolution_col = sheet1.col(6)
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
        
        for ticketnum in data:
            link =  url + ticketnum[3]
            sheet1.write(i, 2, xlwt.Formula("HYPERLINK"+'("'+link+'";"'+ticketnum[2]+'")'), style)
            i +=  1
        i = 1
        
        for status in data:
            sheet1.write(i, 3, status[4])
            i +=  1
        i = 1
        
        for summary in data:
            sheet1.write(i, 4, summary[5])
            i +=  1
        i = 1
        
        for reporter in data:
            sheet1.write(i, 5, reporter[6])
            i +=  1
        i = 1
        
        for resolution in data:
            sheet1.write(i, 6, resolution[7])
            i +=  1
        i = 1
        
        book.save(filename)
        print "%s save ok..." %  (filename)
            
            
def main():
    WebSpider =  Spider(url, loginUrl, **headers)
    WebSpider.getData(loginUrl, loginData)
    filename = "VlabTicket.xls"
    WebSpider.saveToExcel(filename)

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

        
        

