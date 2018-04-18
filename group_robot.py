import itchat
from itchat.content import *
import requests
import json

DEFAULT_CONF_FILE = "conf/conf.json"
globalconf = {}

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : globalconf["robot"]["key"],
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        defaultReply = 'I received: ' + msg['Text']
        #remove nickname of the msg Text
        puremsg = msg['Text']
        puremsg = puremsg.replace("@叫我马丁","")
        reply = get_response(puremsg)
        return reply or defaultReply

#get conf
def get_global_conf(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data 

#global conf , json struct
globalconf = get_global_conf(DEFAULT_CONF_FILE)
itchat.auto_login(enableCmdQR=2, hotReload=True)
itchat.run()
