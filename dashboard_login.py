import urllib2
import cookielib
import urllib

login_url = 'http://135.252.195.10/dashboard/auth/login/'

headers = {"Origin": "http://135.252.195.10",
           "Referer":"http://135.252.195.10/dashboard/auth/login/?next=/dashboard/",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

resp = urllib2.urlopen(login_url)

for cookie in enumerate(cj):
    csr = str(cookie[1]).split("=")[1].split(" ")[0]
    
print csr

login_data = urllib.urlencode({"csrfmiddlewaretoken":csr,
                               "fake_email":"",
                               "fake_password":"",
                               "next":"/dashboard/",
                               "region":"http://192.168.1.200:5000/v2.0",
                               "domain":"default",
                               "username":"admin",
                               "password":"123456"})


for key in headers:
    opener.addheaders.append((key,headers[key]))
opener.open(login_url,login_data)
print opener.open('http://135.252.195.10/dashboard/project/instances/').read()
