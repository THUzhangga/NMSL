# -*- coding:utf-8 -*-

from flask import Flask
from flask import request, make_response

import hashlib
import time
from nmsl_local import *
import pickle
import sqlite3
from lxml import etree
import xml.etree.ElementTree as ET



app = Flask(__name__)
app.debug = True

class  Message(object):
    """docstring for  Message"""
    def __init__(self, req):
        self.request = req    
        self.token = 'thulecture'
        self.AppID = 'wx0f12d0d1a1f763bf'
        self.AppSecret = 'I343yWDXtxEOHLot6JVK9vnzgka52FKFEuUtAt6q4np'

class Post(Message):
    def __init__(self, req):
        super(Post, self).__init__(req)
        self.xml = etree.fromstring(req.stream.read())
        self.MsgType = self.xml.find("MsgType").text
        self.ToUserName = self.xml.find("ToUserName").text
        self.FromUserName = self.xml.find("FromUserName").text
        self.CreateTime = self.xml.find("CreateTime").text
        self.MsgId = self.xml.find("MsgId").text

        hash_table = {
            'text': ['Content'],
            'image': ['PicUrl', 'MediaId'],
            'voice': ['MediaId', 'Format'],
            'video': ['MediaId', 'ThumbMediaId'],
            'shortvideo': ['MediaId', 'ThumbMediaId'],
            'location': ['Location_X', 'Location_Y', 'Scale', 'Label'],
            'link': ['Title', 'Description', 'Url'],
        }
        attributes = hash_table[self.MsgType]
        self.Content = self.xml.find("Content").text if 'Content' in attributes else '抱歉，暂未支持此消息。'
        self.PicUrl = self.xml.find("PicUrl").text if 'PicUrl' in attributes else '抱歉，暂未支持此消息。'
        self.MediaId = self.xml.find("MediaId").text if 'MediaId' in attributes else '抱歉，暂未支持此消息。'
        self.Format = self.xml.find("Format").text if 'Format' in attributes else '抱歉，暂未支持此消息。'
        self.ThumbMediaId = self.xml.find("ThumbMediaId").text if 'ThumbMediaId' in attributes else '抱歉，暂未支持此消息。'
        self.Location_X = self.xml.find("Location_X").text if 'Location_X' in attributes else '抱歉，暂未支持此消息。'
        self.Location_Y = self.xml.find("Location_Y").text if 'Location_Y' in attributes else '抱歉，暂未支持此消息。'
        self.Scale = self.xml.find("Scale").text if 'Scale' in attributes else '抱歉，暂未支持此消息。'
        self.Label = self.xml.find("Label").text if 'Label' in attributes else '抱歉，暂未支持此消息。'
        self.Title = self.xml.find("Title").text if 'Title' in attributes else '抱歉，暂未支持此消息。'
        self.Description = self.xml.find("Description").text if 'Description' in attributes else '抱歉，暂未支持此消息。'
        self.Url = self.xml.find("Url").text if 'Url' in attributes else '抱歉，暂未支持此消息。'
        self.Recognition = self.xml.find("Recognition").text if 'Recognition' in attributes else '抱歉，暂未支持此消息。'

class Reply(Post):
    def __init__(self, req):
        super(Reply, self).__init__(req)
        self.xml = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime>" % (self.FromUserName, self.ToUserName, str(int(time.time())))
    def text(self, Content):
        self.xml += "<MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content></xml>" % (Content)
        # self.xml = ET.fromstring(xml_string)
        # return self.xml
    def reply(self):
        response = make_response(self.xml)
        response.content_type = 'application/xml'
        return response

@app.route('/wx_flask',methods=['GET','POST'])
def wechat():
    with sqlite3.connect("USERS.db") as con:
        def check_USER_not_exist(user):
            cursor.execute("SELECT * FROM USERS WHERE USER=?", (user,))
            rows = cursor.fetchall()
            return len(rows) == 0

        def check_USER_method(user):
            cursor.execute("SELECT method FROM USERS WHERE USER=?", (user,))
            rows = cursor.fetchone()
            return rows[0]

        if request.method == 'GET':
            #这里改写你在微信公众平台里输入的token
            token = 'thulecture'
            #获取输入参数
            data = request.args
            signature = data.get('signature','')
            timestamp = data.get('timestamp','')
            nonce = data.get('nonce','')
            echostr = data.get('echostr','')
            #字典排序
            mylist = [token, timestamp, nonce]
            mylist.sort()

            s = mylist[0] + mylist[1] + mylist[2]
            #sha1加密算法        
            hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
            #如果是来自微信的请求，则回复echostr
            if hascode == signature:
                return echostr
            else:
                return "nmsl"
            return echostr
        if request.method == 'POST':
            message = Reply(request)
            cursor = con.cursor()

            if message.MsgType == 'event':
                print('subscribe')
                message.text('山不在高，有林则徐。水不在深，有***。回复文字即可转换为抽象话，回复0或1可切换抽象模式到轻度或深度。')

            # message.text(message.Content)
            # pickle.dump(message.Content, open('message.txt', 'wb'))
            if message.Content == '深度' or message.Content == '1':
                user = message.FromUserName
                if check_USER_not_exist(user):
                    cursor.execute("INSERT INTO USERS (USER, METHOD) VALUES (?,?);", (user, 1))
                    con.commit()
                else: # 用户存在，则更新
                    cursor.execute("UPDATE USERS set METHOD=? where USER=?;", (1, user))
                    con.commit()
                message.text('深度抽象模式')

            if message.Content == '轻度' or message.Content == '0':
                user = message.FromUserName
                if check_USER_not_exist(user):
                    cursor.execute("INSERT INTO USERS (USER, METHOD) VALUES (?,?);", (user, 0))
                    con.commit()
                else:
                    cursor.execute("UPDATE USERS set METHOD=? where USER=?;", (0, user))
                    con.commit()
                message.text('轻度抽象模式')
            else:
                user = message.FromUserName
                print(user)
                if check_USER_not_exist(user): # 用户不存在，默认轻度抽象        
                    message.text(text_to_emoji(message.Content))
                else: # 用户存在，需要检查抽象模式
                    method = check_USER_method(user)
                    print(method)
                    message.text(text_to_emoji(message.Content, method=method))

            return message.reply()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
