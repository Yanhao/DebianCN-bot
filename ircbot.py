#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import socket
import threading

Server = 'chat.freenode.net'
Port = 8001
Nick = 'mmmbot'
RealName = 'Debian Chinese Forums IRC Bot'
Channel = '#debiancn'
Msg = 'TEST'
NewPostsDir = './NewPosts'


Socket = socket.socket()
print("Create new socket ...")
Socket.connect((Server, Port))
print("Connect to server ...")
Socket.send('NICK {nick}\r\n'.format(nick=Nick).encode())
Socket.send('USER {nick} 0 * :{realname}\r\n'.format(nick=Nick, realname=RealName).encode())
Socket.send('JOIN {channel}\r\n'.format(channel=Channel).encode())
print("Join in the {channel} Channel ...".format(channel=Channel))

while True:
    line = Socket.recv(2048).decode('utf8')
    print(line)
    line = line.split()
    if line[1] == 'JOIN':
        break

def poster():
    print("第二个线程开始运行...")
    while True:
        NewPostsList = os.listdir(NewPostsDir)
        for NewPost in NewPostsList:
            NewPost = NewPostsDir + '/' + NewPost
            Msg = open(NewPost, "r").readline()
            print(Msg)
            Socket.send('PRIVMSG {channel} :{msg}\r\n'.format(channel=Channel, msg=Msg).encode())
            os.remove(NewPost)
            time.sleep(5)
        time.sleep(30)

t = threading.Thread(target=poster, name="Thread2")
t.start()

while True:
    line = Socket.recv(2048).decode('utf8')
    print(line)
    line = line.split()
    if line[0] == 'PING':
        print("Receive PING command form server ...")
        Socket.send('PONG {arg}\r\n'.format(arg=line[1]).encode())
        print("Send PONG commang to server ...")
        Socket.send('PRIVMSG {channel} :{msg}\r\n'.format(channel=Channel, msg="Send PONG commang to server ...").encode())
