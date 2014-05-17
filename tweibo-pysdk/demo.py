# -*- coding:utf-8 -*- #
#! /usr/bin/env python

import time
from multiprocessing.pool import ThreadPool
#sys.path.insert(0, 'tweibo.zip')
from tweibo import * 
from threading import Thread
from threading import current_thread
from Queue import Queue
# 换成你的 APPKEY
APP_KEY = "801503782"
APP_SECRET = "cee9c0bd355f8c730304151887aabff86"
CALLBACK_URL = "https://www.github.com"
# 请先按照 https://github.com/upbit/tweibo-pysdk/wiki/OAuth2Handler 的鉴权说明填写 ACCESS_TOKEN 和 OPENID
ACCESS_TOKEN = "eebb463c87bfd293e295fbf9cf557076"
OPENID = "9FF31A1D9A1FEFDEC109EB0DA6BA8E61"
IMG_EXAMPLE = "example.png"

# 返回text是unicode，设置默认编码为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def access_token_test():
    """ 访问get_access_token_url()的URL并授权后，会跳转callback页面，其中包含如下参数：
        #access_token=00000000000ACCESSTOKEN0000000000&expires_in=8035200&openid=0000000000000OPENID0000000000000&openkey=0000000000000OPENKEY000000000000&refresh_token=0000000000REFRESHTOKEN00000000&state=
    保存下其中的 access_token, openid 并调用
        oauth.set_access_token(access_token)
        oauth.set_openid(openid)
    即可完成 OAuth2Handler() 的初始化。可以记录 access_token 等信息
    """
    oauth = OAuth2Handler()
    oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
    print oauth.get_access_token_url()

def tweibo_test():
    oauth = OAuth2Handler()
    oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
    oauth.set_access_token(ACCESS_TOKEN)
    oauth.set_openid(OPENID)

    api = API(oauth)
    #api = API(oauth, host="127.0.0.1", port=8888)       # Init API() with proxy

    # GET /t/show
    #tweet1 = api.get.t__show(format="json", id=301041004850688)
    #print ">> %s: %s" % (tweet1.data.nick, tweet1.data.text)

    # POST /t/add
    #content_str = "[from PySDK] %s says: %s" % (tweet1.data.nick, tweet1.data.origtext)
    #tweet2 = api.post.t__add(format="json", content=content_str, clientip="10.0.0.1")
    #print ">> time=%s, http://t.qq.com/p/t/%s" % (tweet2.data.time, tweet2.data.id)

    # GET /statuses/user_timeline
    #user_timeline = api.get.statuses__user_timeline(format="json", name="qqfarm", reqnum=3, pageflag=0, lastid=0, pagetime=0, type=3, contenttype=0)
    #for idx, tweet in enumerate(user_timeline.data.info):
    #    print "[%d] http://t.qq.com/p/t/%s, (type:%d) %s" % (idx+1, tweet.id, tweet.type, tweet.text)

    # UPLOAD /t/upload_pic
    pic1 = api.upload.t__upload_pic(format="json", pic_type=2, pic=open(IMG_EXAMPLE, "rb"))
    print ">> IMG: %s" % (pic1.data.imgurl)

    # POST /t/add_pic_url
    content_str2 = "[from PySDK] add pic demo: %s, time %s" % (IMG_EXAMPLE, time.time())
    pic_urls = "%s" % (pic1.data.imgurl)
    tweet_pic1 = api.post.t__add_pic_url(format="json", content=content_str2, pic_url=pic_urls, clientip="10.0.0.1")
    print ">> time=%s, http://t.qq.com/p/t/%s" % (tweet_pic1.data.time, tweet_pic1.data.id)

    #t1=time.time()
    #heat_trend=api.get.trends__ht(format="json", reqnum=20, pos=0)
    #for dat in heat_trend.data['info']:
    #    print dat['name'].encode('utf-8'),dat['tweetnum']
    #    heat_tweets=api.get.statuses__ht_timeline_ext(format="json",reqnum=4,tweetid=0,time=0,pageflag=0,flag=0,htid=dat['id'],type=1,contenttype=0x80)
    #    for tweets_dat in heat_tweets.data['info']:
    #        print tweets_dat['text'].encode('utf-8')
    #t2=time.time()
    #print t2-t1
    t3=time.time()
    
    heat_trend=api.get.trends__ht(format="json", reqnum=4, pos=0)
    
    def worker(_task_queue,_api):
        lastTweetid,lastTweettime,lastPageflag=0,0,0
        while(True):
            # try: 
            htid=_task_queue.get()
            heat_tweets=_api.get.statuses__ht_timeline_ext(format="json",reqnum=2,tweetid=lastTweetid,time=lastTweettime,pageflag=lastPageflag,flag=0,htid=htid,type=1,contenttype=0x80)
            #     for tweets_dat in heat_tweets.data['info']:
            #         print tweets_dat['text'].encode('utf-8')
                #(heat_tweets.data['info'][-1]['id'],heat_tweets.data['info'][-1]['timestamp'])
            
            # reqApi(_api,htid)
            # print heat_tweets.data['info'][-1]['timestamp']
            for tweets_dat in heat_tweets.data['info']:
                print tweets_dat['text'].encode('utf-8')
            lastTweetid=heat_tweets.data['info'][-1]['id']
            lastTweettime=heat_tweets.data['info'][-1]['timestamp']
            
            lastPageflag=1
            _task_queue.task_done()
            # except TypeError as e:
            #     print 'TypeError'
            # except:
            #     print 'Unexpected error: ',sys.exc_info()[0]

    def getHeatTrend(_task_queue):
        while(True):
            try:
                heat_trend=api.get.trends__ht(format="json", reqnum=4, pos=0)
                if heat_trend:
                    for dat in heat_trend.data['info']:
                        _task_queue.put(dat['id'])
                    _task_queue.join()
            except TypeError as e:
                print 'TypeError'
            except:
                print 'Unexpected error: ',sys.exc_info()[0]
    
    task_queue=Queue()
    
    #spwran threading pool
    for i in range(4):
        t=Thread(target=worker,args=(task_queue,api))
        t.start()

    getHTThread=Thread(target=getHeatTrend,args=(task_queue,))
    getHTThread.start()
    
    t4=time.time()
    print t4-t3
if __name__ == '__main__':
    
    #access_token_test()
    tweibo_test()