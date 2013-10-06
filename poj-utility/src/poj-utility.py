import urllib2
import urllib
import gzip
import StringIO
import sys
import re
import cookielib
import httplib
from bs4 import BeautifulSoup
#httplib.HTTPConnection.debuglevel=1
'''change agent'''
def postData(logUrl, logData, opener, loginFlag):
    request = urllib2.Request(logUrl, urllib.urlencode(logData))
    request.add_header('host','poj.org')
    request.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')
    request.add_header('Accept-Encoding', 'gzip')
    request.add_header('Connection','keep-alive')
    html = ''
    data = {'opener':opener, 'html':html}
    if loginFlag is False:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
    '''another way to add header'''
    data['opener'] = opener
    #opener.addheaders = [(),(),]
    gzipFd = opener.open(request)
    gzipData = gzipFd.read()
    gzipStream = StringIO.StringIO(gzipData)
    unZipFd = gzip.GzipFile(fileobj=gzipStream)
    data['html'] = unZipFd.read() 
    return data
    '''low efficient code, in fact, data['opener'] do not chaenged, but i have to''' 
    '''return the value'''
    #open('tmp.html','w').write(html) 
    #return html 
def logout(logoutUrl, opener):
    request = urllib2.Request(logoutUrl)
    request.add_header('host','poj.org')
    request.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')
    request.add_header('Accept-Encoding', 'gzip')
    request.add_header('Connection','keep-alive')
    opener.open(request)
def main():
    '''login'''
    psWord = raw_input('Enter your password on POJ: ')
    user_id = 'testdot'
    logUrl = 'http://poj.org/login'
    logData = {'user_id1': user_id, 'password1':psWord, 'url':'submit', 'B1':'login'}
    opener = urllib2.OpenerDirector() 
    data = postData(logUrl, logData, opener, loginFlag = False)
    '''
       int for loop do the following things:
       1.get name from args
       2.parsing, get the problem_id
       3.read specific file
       4.submit file to matched url
    ''' 

    pattern = '(\d+)\.(c|cpp|java|pas)'

    '''hardcode: and if not find statParse, do not raise exception'''
    '''when poj changed, the code can not work'''
    statParse = 'a[href^=userstatus?user_id=' + user_id + ']'
    '''NEED TO SOLVE: exception of lacking argv '''
    '''little chances that users on windows use this srcipt'''
    lang = {'cpp':'0', 'c':'1','java':'2','pas':'3'}
    for v in sys.argv[1:]:
        matchobj = re.match(pattern, v)
        if matchobj:
            try:
                srcFile = open(v, 'r')
            except IOerror:
                print 'failed to open %s, file may not exist' %(v),
            else:
                problem_id = matchobj.group(1)
                langId = lang[matchobj.group(2)]
                submitUrl = 'http://poj.org/submit'
                srcCode = srcFile.read()
                submitData = {'language':langId, 'problem_id':problem_id, 'source':srcCode, 'submit':'Submit'}
                data = postData(submitUrl, submitData, data['opener'], loginFlag = True)  

                '''parse status html, working in a particular way'''
                soup = BeautifulSoup(data['html'])
                tags = soup.select(statParse) 
                for tag in tags:
                    tagPar = tag.parent.parent
                    print '%s \t %s'%(tagPar.contents[2].string, tagPar.contents[3].string)
                srcFile.close()
        else:
            print 'please name src file by problem id\n'            
            print 'examples: 1000.c'
    logoutUrl = 'http://poj.org/login?action=logout&url=%2F' 
    logout(logoutUrl,opener)
if __name__ == '__main__':
    main()
