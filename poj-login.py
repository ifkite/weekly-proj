import urllib2
import urllib
import gzip
import StringIO
import sys
import re
import cookielib
#import httplib
#httplib.HTTPConnection.debuglevel=1
'''change agent'''
def postData(logUrl, logData):
    request = urllib2.Request(logUrl, urllib.urlencode(logData))
    #request.add_header('Referer',referer)
    request.add_header('host','poj.org')
    request.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('Connection','keep-alive')
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    '''another way to add header'''
    #opener.addheaders = [(),(),]
    gzipFd = opener.open(request)
    gzipData = gzipFd.read()
    gzipStream = StringIO.StringIO(gzipData)
    unZipFd = gzip.GzipFile(fileobj=gzipStream)
    html = unZipFd.read() 
    #open('tmp.html','w').write(html)
    return html
    
def submit(subUrl, subData):
    request = urllib2.Request()

def main():
    '''login'''
    logUrl = 'http://poj.org/submit'
    psWord = raw_input('Enter your password in POJ: ')
    srcCode = ''
    problem_id = '1000'
    logData = {'user_id1':'testdot', 'password1':psWord, 'url':'/', 'B1':'login','language':'1', 'problem_id':problem_id, 'source':srcCode, 'submit':'Submit'}
    #referer = 'http://poj.org/submit?problem_id=1000'
    logHtml = postData(logUrl, logData)
    open('login.html','w').write(logHtml)
    '''
       1.get name from args
       2.parsing, get the problem_id
       3.read specific file
       4.submit file to matched url
    ''' 

    '''
    pattern = '(\d+)\.(\w+)'
    for v in sys.argv[1:]:
        matchobj = re.match(pattern, v)
        if matchobj:
            try:
                srcFile = open(v, 'r')
            except IOerror:
                print 'failed to open %s, file may not exist' %(v),
            else:
                problem_id = matchobj.group(1)
                submitUrl = 'http://poj.org/submit'
                srcCode = srcFile.read()
                submitData = {'language':'1', 'problem_id':problem_id, 'source':srcCode, 'submit':'Submit'}
                html = postData(submitUrl, submitData)
                open('submit.html','w').write(html) 
     '''
if __name__ == '__main__':
    main()
