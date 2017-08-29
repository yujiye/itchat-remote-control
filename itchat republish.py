"""
this is code by lieber.

2016-10-11
"""
# -*- coding: utf-8 -*-
import itchat
import _thread as thread
from itchat.content import *
import time
import pickle
import os
import time

def write_pkl(var, filepath):
    """
    变量写入pkl
    """
    output = open(filepath, 'wb')
    pickle.dump(var, output)
    print('writing to ' + filepath)
    output.close()


def load_pkl(filepath):
    """
    读取pkl到变量
    """
    output = open(filepath, 'rb')
    var = pickle.load(output)
    output.close()
    return var


def get_name(id):
    """利用 id 返回备注或者昵称"""
    user=itchat.search_friends(userName=id)
    if user['RemarkName']!='':
        return user['RemarkName']
    else:
        return user['NickName']
def get_id(NAME):
    """利用 昵称返回 id"""
    return itchat.search_friends(name=NAME)[0]['UserName']

def get_all_name():
    """获取所有好友名字"""
    alluser=itchat.get_friends()
    allname=[]
    for user in alluser:
        if user['RemarkName'] !='':
            allname.append(user['RemarkName'].strip())
        else:
            allname.append(user['NickName'].strip())
    # allname.sort()
    return '  '.join(allname)

def get_all_id():
    """获取所有好友id"""
    alluser=itchat.get_friends()
    allid=[]
    for user in alluser:
            allid.append(user['UserName'])
    # allname.sort()
    return allid

def search_byfirst(txt):
    """查找首字母为 txt 的名字"""
    temp=[]
    for _ in get_all_name().split('  '):
        if _ !='':
            if txt==_[0]:
                temp.append(_)
    # print(temp)
    return '  '.join(temp)

def write_sub(room_id,from_user_name,content,msgtime):
    ###存储历史chatroom###
    input=open('room_history.txt','a',encoding='utf-8')
    input.write(room_id+'##$##'+from_user_name+'##$##'+content+'##$##'+msgtime+'\n')
    input.close()

def get_all_active_room():
    """获取所有在 roomhistory 中记录了的 roomid,roomname"""
    input=open('room_history.txt','r',encoding='utf-8')
    room_name_list=[]
    for line in input:
        name=line.split('##$##')[0]
        if name not in room_name_list:
            room_name_list.append(name)
    return room_name_list

def get_room_chat_history(index):
    """通过 room_id_list 的某房间 id 获取该房间最近聊天记录文件"""
    goal_room_name=get_all_active_room()[index]
    input=open('room_history.txt','r',encoding='utf-8')

    outputfile=open('tempdata/temp chat history.txt','w',encoding='utf-8')
    outputfile.write('聊天记录------%s\n'%goal_room_name)
    i=0
    for line in input:
        line=line.strip()
        # print(line)
        roomname=line.split('##$##')[0]
        username=line.split('##$##')[1]
        text=line.split('##$##')[2]
        msgtime=line.split('##$##')[3]
        if roomname==goal_room_name:
            i+=1
            if i==500:
                break
            outputfile.write(username+' : '+text+'    '+msgtime+'\n')
    input.close()
    outputfile.close()

def update_function():
    """
    微信动态注册消息
    """


    @itchat.msg_register([MAP,CARD,SHARING,FRIENDS,NOTE], isGroupChat=False)
    def general_reply(msg):
        if msg['FromUserName'] not in[account1_id]:
            if msg['Type']=='Note' and any(s in msg['Text'] for s in (u'红包', u'转账')) :
                content='收到来自%s 的红包！！！！'%(get_name(msg['FromUserName']))
                itchat.send(msg=content, toUserName=account2_id)
                return
            if msg['Type']=='Sharing':
                if msg['AppMsgType']== 5:
                #非音乐链接
                    content='收到%s 的分享链接 %s '%(get_name(msg['FromUserName']),msg['Text'])
                    url=msg['Url']
                    itchat.send(msg=content+'\n'+url, toUserName=account2_id)
                    return 
                if msg['AppMsgType']== 3:
                #非音乐链接
                    content='收到%s 的分享音乐 %s '%(get_name(msg['FromUserName']),msg['FileName'])
                    url=msg['Url']
                    itchat.send(msg=content+'\n'+url, toUserName=account2_id)
                    return 
            if msg['Type']=='Map':
                content='收到%s 的地图分享 %s '%(get_name(msg['FromUserName']),msg['Text'])
                url=msg['Url']
                itchat.send(msg=content+'\n'+url, toUserName=account2_id)
                return 
            content='收到来自%s 的%s 类型消息，请前往大号查看。'%(get_name(msg['FromUserName']),msg['Type'])
            itchat.send(msg=content, toUserName=account2_id)
                    

    @itchat.msg_register(TEXT, isGroupChat=False)
    def text_reply(msg):

        global recent_name_list
        global chat_namelist_index

        if msg['FromUserName'] in[account1_id,account2_id]:
        #处理来自大号或者小号自身消息
            if False:
                #开启或者关闭系统
                # if  msg['FromUserName'] in[]:
                #     if u'开启' in msg['Text'] 
                #         print('开启成功')
                #         return u'开启成功'
                pass

            else:
                if msg['FromUserName']==account2_id:
                    
                    text=msg['Text']

                    #返回帮助信息
                    if text=='help':
                        content="全部好友 : 获取所有好友\n好友名--内容 : 以指定模式发送消息\n？姓 : 查询当前姓所有好友\n"+\
                        "@@@ : 获取最近聊天好友列表\n@@int : 设定固定模式聊天对象\n@？ : 查询当前固定模式聊天对象\n@内容 : 向固定模式发送消息\n"+\
                        "最近群聊 : 获取最近聊天群组 index::群组名\n群聊查询int : 获取该群聊聊天历史\n群聊int--内容 : 向该群发消息 群聊int--@好友名--内容 : 在该群@好友"
                        itchat.send(msg=content, toUserName=account2_id)
                        return

                    #获取所有好友的列表
                    if '全部好友'==text:
                        content=get_all_name()
                        itchat.send(msg=content, toUserName=account2_id)

                    #获取最近聊天群聊
                    if '最近群聊'==text:
                        room_name_list=get_all_active_room()
                        if room_name_list==[]:
                            print('最近群聊为空')
                            itchat.send(msg='最近群聊为空', toUserName=account2_id)
                            return
                        else:
                            # print(room_id_list)
                            content='最近群聊::::  '
                            for i, room_name in enumerate(room_name_list):
                                # print(itchat.search_chatrooms(userName=room_id)['NickName'])
                                content=content+' '+str(i)+' : '+room_name
                            itchat.send(msg=content, toUserName=account2_id)

                    #查询群聊聊天记录
                    if '群聊查询'==text[:4]:

                        try:
                            room_index=int(text[4:])
                            # print(get_all_active_room())
                            roomname=get_all_active_room()[room_index]
                            # print(roomid)
                            get_room_chat_history(room_index)
                            itchat.send(msg='%s 的最近聊天记录'%roomname, toUserName=account2_id)
                            itchat.send('@fil@'+os.getcwd()+'/tempdata/temp chat history.txt', account2_id)
                        except:
                            print('查询群聊历史 error')
                            itchat.send(msg='查询群聊历史 error', toUserName=account2_id)
                        return

                    #在群聊中发信息
                    if '群聊' ==text[:2] and '群聊查询'!=text[:4]:
                        try:

                            room_index=int(text.split('--')[0][2:])
                            roomname=get_all_active_room()[room_index]
                            roomid=itchat.search_chatrooms(name=roomname)[0]['UserName']
                            content='--'.join(text.split('--')[1:])
                            if '@' not in content:
                            #不@用户时
                                itchat.send(msg=content,toUserName=roomid)
                                print('!@ %s --> %s'%(content,roomname))
                            else:
                            #@用户时
                                atusername=content.split('--')[0][1:]
                                realcontent=content.split('--')[1]
                                nickname=itchat.search_friends(name=atusername)[0]['NickName']
                                sendcontent='@%s %s'%(nickname,realcontent)
                                itchat.send(msg=sendcontent,toUserName=roomid)
                                print('%s --> %s'%(sendcontent,roomname))
                        except:
                            print('发送群聊消息 error')
                            itchat.send(msg='发送群聊消息 error', toUserName=account2_id)


                    #获取最近聊天好友列表
                    if '@@@'==text:
                        write_pkl(recent_name_list,'recent_name_list.pkl')
                        content=' '.join(str(recent_name_list.index(_))+':'+_ for _ in recent_name_list) \
                                                if recent_name_list !=[] else '最近列表为空'
                        itchat.send(msg=content, toUserName=account2_id)
                        return

                    #搜索特殊 姓 下的名字
                    if  "？"==text[0]:
                        try:
                            content=search_byfirst(text[1])
                            itchat.send(msg=content, toUserName=account2_id)
                        except:
                            print('搜索姓名用户 error')
                            itchat.send(msg='搜索姓名用户 error', toUserName=account2_id)



                    #设定常用聊天模式用户index '@@ %int'
                    if '@@'==text[:2]:
                        try:
                            chat_namelist_index=int(text[2:])
                            content='设定常用聊天对象为: '+recent_name_list[chat_namelist_index]
                            itchat.send(msg=content, toUserName=account2_id)
                        except:
                            print('常用聊天模式用户index error')
                            itchat.send(msg='常用聊天模式用户index error', toUserName=account2_id)

                        return

                    #查询当前常用用户聊天模式设定 index
                    if '@？'==text:
                        content='当前聊天对象: '+recent_name_list[chat_namelist_index]
                        itchat.send(msg=content, toUserName=account2_id)

                        return 

                    #使用小号回复消息
                    #常用聊天模式
                    if "@" == text[0]:
                        content=text[1:]
                        to_id=get_id(recent_name_list[chat_namelist_index])
                        print(content+' --> '+recent_name_list[chat_namelist_index])
                        itchat.send(msg=content, toUserName=to_id)

                    #使用小号回复消息
                    #指定用户名模式
                    if '--' in text and '群聊' !=text[:2]:
                        name=text.split('--')[0]
                        content=text.split('--')[1]
                        print(content+' --> '+name)
                        if name not in get_all_name():
                            print('指定用户名模式 error')
                            itchat.send(msg='指定用户名模式 error', toUserName=account2_id)
                        else:
                            itchat.send(msg=content, toUserName=get_id(name))



        else:
        #处理不来自大号或者小号自身消息
            
            text=msg['Text']
            from_id=msg['FromUserName']
            from_name=get_name(from_id)

            #添加到常用 recent_name_list
            if from_name not in recent_name_list:
                recent_name_list.append(from_name)
                write_pkl(recent_name_list,'recent_name_list.pkl')

            #转发收到的消息到 小号
            send_txt=from_name+'--'+text
            print(from_name+' --> '+text)
            itchat.send(msg=(from_name+'--'+text), toUserName=account2_id)

    @itchat.msg_register(['Picture','Recording','Attachment','Video'],isGroupChat=False)
    def record_reply(msg):

        global recent_name_list
        global chat_namelist_index

        #处理不来自大号和小号的附件信息
        if msg['FromUserName'] not in[account1_id,account2_id]:
            msg['Text'](os.getcwd()+'/tempdata/'+msg['FileName'])
            content='来自%s 的附件'%(get_name(msg['FromUserName']))
            itchat.send(msg=content, toUserName=account2_id)
            itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil',\
                         os.getcwd()+'/tempdata/'+msg['FileName']), account2_id)
            print('收到'+content)
        else:
        #转发出其他信息
        #只能使用常用聊天模式
            # print(msg) 
            msg['Text'](os.getcwd()+'/tempdata/'+msg['FileName'])
            itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil',\
                         os.getcwd()+'/tempdata/'+msg['FileName']), get_id(recent_name_list[chat_namelist_index]))

    @itchat.msg_register(TEXT, isGroupChat=True)
    def group_reply(msg):
        global keywords
        #不能使用大号回复内容
        from_userid=msg['ActualUserName']
        room_id=msg['FromUserName']
        content=msg['Content']
        isat=msg['IsAt']
        msgtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        # print(msg)
        if from_userid !=account1_id:
            room_name=itchat.search_chatrooms(userName=room_id)['NickName']
            from_user_name=get_name(from_userid)
            if isat or any(_ in content for _ in keywords):
                itchat.send('群 %s: %s --> %s' % (room_name, from_user_name,content), account2_id)
                print('群 %s: %s --> %s' % (room_name, from_user_name,content))
                write_sub(room_name,from_user_name,content,msgtime)
            else:
                write_sub(room_name,from_user_name,content,msgtime)
        else:
            room_id=msg['ToUserName']
            room_name=itchat.search_chatrooms(userName=room_id)['NickName']
            from_user_name='我自己'
            write_sub(room_name,from_user_name,content,msgtime)

if __name__ == '__main__':
    # 初始操作
    
    # itchat
    itchat.auto_login(hotReload=True)
    # itchat.auto_login(hotReload=-1)

    # itchat.auto_login()
    itchat.dump_login_status()
    thread.start_new_thread(itchat.run, ())


    if not os.path.exists(os.getcwd()+'/room_history.txt'):
        os.mknod("room_history.txt")
    recent_name_list=[]
    if os.path.exists(os.getcwd()+'/recent_name_list.pkl'):
        recent_name_list=load_pkl('recent_name_list.pkl')
    chat_namelist_index=0 #选择常用用户模式下index

    # itchatID设置
    account2_name='昵称'
    account1_id = itchat.search_friends()['UserName']
    account2_id=itchat.search_friends(name=account2_name)[0]['UserName']
    keywords='关键词 关键词 关键词'.split(' ')

    while 1:
        #每半小时发送 心跳消息检测是否正常
        localtime = time.localtime(time.time())
        if localtime.tm_min in [0,30] and localtime.tm_hour>= 7 and localtime.tm_sec in [0,1]:
            itchat.send(msg='网页微信运行正常(%d:%d)'%(localtime.tm_hour,localtime.tm_min), toUserName=account2_id)
            time.sleep(1)

        update_function()
        time.sleep(1)
