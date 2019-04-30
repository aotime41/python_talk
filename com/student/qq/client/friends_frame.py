#!/usr/bin/env python

# -*- coding:utf-8 -*-

"""好友列表窗口"""


import json
import threading

import wx.lib.scrolledpanel as scrolled

from com.student.qq.client.chat_frame import ChatFrame
from com.student.qq.client.my_frame import *


class FriendsFrame(MyFrame):
    def __init__(self, user):
        super().__init__(title='我的好友', size=(260, 600))

        self.chatFrame = None

        # 用户信息
        self.user = user
        # 好友列表
        self.friends = user['friends']
        # 好友图标控件列表
        self.friendctrols = []

        usericonfile = 'resources/images/{0}.jpg'.format(user['user_icon'])
        usericon = wx.Bitmap(usericonfile, wx.BITMAP_TYPE_JPEG)
        # 顶部面板
        toppanel = wx.Panel(self.contentpanel)
        usericon_sbitmap = wx.StaticBitmap(toppanel, bitmap=usericon)
        username_st = wx.StaticText(toppanel, style=wx.ALIGN_CENTRE_HORIZONTAL, label=user['user_name'])

        # 创建顶部Box布局管理对象
        topbox = wx.BoxSizer(wx.VERTICAL)
        topbox.AddSpacer(15)
        topbox.Add(usericon_sbitmap, 1, wx.CENTER)
        topbox.AddSpacer(5)
        topbox.Add(username_st, 1, wx.CENTER)
        toppanel.SetSizer(topbox)

        # 群聊面板
        roompanel = wx.Panel(self.contentpanel,style=wx.DOUBLE_BORDER)
        roomicon = wx.StaticBitmap(roompanel, bitmap=usericon,style=wx.ALIGN_CENTRE_HORIZONTAL)
        roomname = wx.StaticText(roompanel, style=wx.ALIGN_CENTRE_HORIZONTAL, label='双击进入聊天室')

        # 创建群聊Box布局管理对象
        roombox = wx.BoxSizer(wx.HORIZONTAL)
        #roombox.AddSpacer(15)
        roombox.Add(roomicon, 1, wx.CENTER)
        roombox.AddSpacer(5)
        roombox.Add(roomname,3, wx.CENTER)
        roompanel.SetSizer(roombox)

        """
        #双击对象
        roomicon.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)
        """

        # 好友列表面板
        panel = scrolled.ScrolledPanel(self.contentpanel,-1, size=(260, 1000), style=wx.DOUBLE_BORDER)

        gridsizer = wx.GridSizer(cols=1, rows=20, gap=(1, 1))
        if len(self.friends) > 20:
            gridsizer = wx.GridSizer(cols=1, rows=len(self.friends), gap=(1, 1))

        # 添加好友到好友列表面板
        for index, friend in enumerate(self.friends):

            friendpanel = wx.Panel(panel, id=index)

            fdname_st = wx.StaticText(friendpanel, id=index, style=wx.ALIGN_CENTRE_HORIZONTAL,
                                      label=friend['user_name'])

            fdqq_st = wx.StaticText(friendpanel, id=index, style=wx.ALIGN_CENTRE_HORIZONTAL,
                                    label=friend['user_id'])

            path = 'resources/images/{0}.jpg'.format(friend['user_icon'])
            icon = wx.Bitmap(path, wx.BITMAP_TYPE_JPEG)

            # 如果好友在线fdqqname_st可用，否则不可用
            if friend['online'] == '0':
                # 转换为灰色图标
                icon2 = icon.ConvertToDisabled()
                fdicon_sb = wx.StaticBitmap(friendpanel, id=index, bitmap=icon2, style=wx.BORDER_RAISED)
                fdicon_sb.Enable(False)
                fdname_st.Enable(False)
                fdqq_st.Enable(False)
                self.friendctrols.append((fdname_st, fdqq_st, fdicon_sb, icon))
            else:
                fdicon_sb = wx.StaticBitmap(friendpanel, id=index, bitmap=icon, style=wx.BORDER_RAISED)
                fdicon_sb.Enable(True)
                fdname_st.Enable(True)
                fdqq_st.Enable(True)
                self.friendctrols.append((fdname_st, fdqq_st, fdicon_sb, icon))

            # 为好友图标和名字文本添加双击事件处理
            fdicon_sb.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)
            fdname_st.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)
            fdqq_st.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)

            friendbox = wx.BoxSizer(wx.HORIZONTAL)
            friendbox.Add(fdicon_sb, 1, wx.CENTER)
            friendbox.Add(fdname_st, 1, wx.CENTER)
            friendbox.Add(fdqq_st, 1, wx.CENTER)

            friendpanel.SetSizer(friendbox)

            gridsizer.Add(friendpanel, 1, wx.ALL, border=5)

        panel.SetSizer(gridsizer)
        # panel.SetupScrolling()




        # 创建整体布局管理器
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(toppanel, -1, wx.CENTER | wx.EXPAND)
        box.Add(roompanel, -1, wx.CENTER | wx.EXPAND)
        box.Add(panel, -1, wx.CENTER | wx.EXPAND)
        self.contentpanel.SetSizer(box)


        # 初始化线程
        # 子线程运行状态
        self.isrunning = True
        # 创建一个子线程
        self.t1 = threading.Thread(target=self.thread_body)
        # 启动线程t1
        self.t1.start()

    def on_dclick(self, event):
        # 获得好友id
        fid = event.GetId()

        if self.chatFrame is not None and self.chatFrame.IsShown():
            dlg = wx.MessageDialog(self, '关闭聊天窗口已经打开。',
                                   '操作失败',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # 停止当前线程
        self.isrunning = False
        self.t1.join()

        self.chatFrame = ChatFrame(self, self.user, self.friends[fid])
        self.chatFrame.Show()

        event.Skip()

    # 刷新好友列表
    def refreshfriendlist(self, onlineuserlist):

        # 初始化好友列表
        for index, friend in enumerate(self.friends):
            frienduserid = friend['user_id']
            fdname_st, fdqq_st, fdicon_sb, fdicon = self.friendctrols[index]

            if frienduserid in onlineuserlist:
                fdname_st.Enable(True)
                fdqq_st.Enable(True)
                fdicon_sb.Enable(True)
                fdicon_sb.SetBitmap(fdicon)
            else:
                fdname_st.Enable(False)
                fdqq_st.Enable(False)
                fdicon_sb.Enable(False)
                fdicon_sb.SetBitmap(fdicon.ConvertToDisabled())

        # 重绘窗口，显示更换之后的图片
        self.contentpanel.Layout()

    # 线程体函数
    def thread_body(self):
        # 当前线程对象
        while self.isrunning:
            try:
                # 从服务器端接收数据
                json_data, _ = client_socket.recvfrom(1024)
                # JSON解码
                json_obj = json.loads(json_data.decode())
                logger.info('从服务器端接收数据：{0}'.format(json_obj))
                cmd = json_obj['command']

                if cmd is not None and cmd == COMMAND_REFRESH:
                    useridlist = json_obj['OnlineUserList']
                    if useridlist is not None and len(useridlist) > 0:
                        # 刷新好友列表
                        self.refreshfriendlist(useridlist)

            except Exception:
                continue

    # 重启子线程
    def resettread(self):
        # 子线程运行状态
        self.isrunning = True
        # 创建一个子线程
        self.t1 = threading.Thread(target=self.thread_body)
        # 启动线程t1
        self.t1.start()

    def OnClose(self, event):

        if self.chatFrame is not None and self.chatFrame.IsShown():
            dlg = wx.MessageDialog(self, '请先关闭聊天窗口，再关闭好友列表窗口。',
                                   '操作失败',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # 当前用户下线，给服务器发送下线消息
        json_obj = {}
        json_obj['command'] = COMMAND_LOGOUT
        json_obj['user_id'] = self.user['user_id']

        # JSON编码
        json_str = json.dumps(json_obj)
        # 给服务器端发送数据
        client_socket.sendto(json_str.encode(), server_address)

        # 停止当前子线程
        self.isrunning = False
        self.t1.join()
        self.t1 = None

        # 关闭窗口，并退出系统
        super().OnClose(event)