#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import datetime
import feedparser


def WriteNewTimeStr():
    with open(TimeFile, "w") as f:
        f.write(NewTimeStr)

Url = "http://forums.debiancn.org/feed.php"
TimeFile = "timefile"
# 切换到脚本所在目录
Directory, Filename = os.path.split(os.path.abspath(sys.argv[0]))
os.chdir(Directory)

Feed = feedparser.parse(Url)
NewTimeStr = Feed.updated

if not os.path.exists(TimeFile):
    WriteNewTimeStr()
    print("未发现 timefile 文件，自动创建该文件并记录读取到的Feed更新时间...")
    sys.exit(0)

with open(TimeFile, "r") as f:
    OldTimeStr = f.readline()

NewTime = Feed.updated_parsed
NewDate = datetime.datetime(NewTime[0],
                            NewTime[1],
                            NewTime[2],
                            NewTime[3],
                            NewTime[4],
                            NewTime[5])

OldTime = time.strptime(OldTimeStr, "%a, %d %b %Y %H:%M:%S GMT")
OldDate = datetime.datetime(OldTime[0],
                            OldTime[1],
                            OldTime[2],
                            OldTime[3],
                            OldTime[4],
                            OldTime[5])

if NewDate == OldDate:
    print("论坛暂时没有新帖")
    sys.exit(0)

if NewDate > OldDate:
    Feed.entries.reverse()
    for Entry in Feed.entries:
        EntryTime = Entry.updated_parsed
        EntryDate = datetime.datetime(EntryTime[0],
                                      EntryTime[1],
                                      EntryTime[2],
                                      EntryTime[3],
                                      EntryTime[4],
                                      EntryTime[5])

        if EntryDate > OldDate:
            PostsDir = "NewPosts"
            if not os.path.isdir(PostsDir):
                print("未发现 NewsPosts 目录，自动创建该目录...")
                os.mkdir(PostsDir)

            PostName = "./NewPosts/post" + str(random.randint(100000, 999999))
            with open(PostName, "w") as f:
                NewPost = "论坛新帖: " + Entry.title + ' - ' + \
                    Entry.author + ' - ' + Entry.links[0].href
                print(NewPost)
                f.write(NewPost)

WriteNewTimeStr()
