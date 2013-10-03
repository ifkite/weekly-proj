import urllib2
import urllib
import gzip
import StringIO
import sys
import re
#import httplib
#httplib.HTTPConnection.debuglevel=1
def login(postUrl, postData):
    request = urllib2.Request(postUrl, urllib.urlencode(postData))
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('Connection','keep-alive')
    opener = urllib2.build_opener()
    gzipFd = opener.open(request)
    gzipData = gzipFd.read()
    gzipStream = StringIO.StringIO(gzipData)
    unZipFd = gzip.GzipFile(fileobj=gzipStream)
    html = unZipFd.read() 
    open('tmp.html','w').write(html)
    
def submit(subUrl, subData):
    request = urllib2.Request()

def main():
    postUrl = 'http://poj.org/login'
    psWord = raw_input('Enter your password in POJ: ')
    postData = {'user_id1':'McDolphin', 'password1':psWord, 'url':'/', 'B1':login}
    #login(postUrl, postData)
     
    '''
       1.get name from args
       2.parsing, get the problem_id
       3.read specific file
       4.submit file to matched url
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
                submitUrl = 'poj.org/problem?id='+problem_id
                srcCode = srcFile.read()
                submitData = {'language':'1', 'problem_id':problem_id, 'source':srcCode, 'submit':Submit}
                submit(submitUrl, submitData)
if __name__ == '__main__':
    main()
