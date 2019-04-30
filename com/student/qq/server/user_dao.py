#!/usr/bin/env python

# -*- coding:utf-8 -*-

"""用户管理DAO"""
from com.student.qq.server.base_dao import BaseDao


class UserDao(BaseDao):
    #编写构造方法
    def __init__(self):
        super().__init__()

    def findbyid(self, userid):
        """根据用户id查询用户信息"""
        try:
            #创建游标对象
            with self.conn.cursor() as cursor:
                #执行SQL操作
                sql = 'select user_id,user_pwd,user_name, user_icon ' \
                      'from users where user_id =%s'
                cursor.execute(sql, userid)
                #提取结果集
                row = cursor.fetchone()

                if row is not None:
                    user = {}       #字典
                    user['user_id'] = row[0]
                    user['user_pwd'] = row[1]
                    user['user_name'] = row[2]
                    user['user_icon'] = row[3]
                    return user

                # with代码块结束,关闭游标

        finally:
            #关闭数据连接
            self.close()


    def findfriends(self, userid):
        """按照用户id查询好友信息"""

        users = []      #列表
        try:
            #创建游标对象
            with self.conn.cursor() as cursor:
                #执行SQL操作
                sql = 'select user_id,user_pwd,user_name,user_icon FROM users WHERE ' \
                      ' user_id IN (select user_id2 as user_id from friends where user_id1 = %s)' \
                      ' OR user_id IN (select user_id1 as user_id from friends where user_id2 = %s)'

                cursor.execute(sql, (userid, userid))
                #提取结果集,多条记录
                result_set = cursor.fetchall()

                for row in result_set:
                    user = {}
                    user['user_id'] = row[0]
                    user['user_pwd'] = row[1]
                    user['user_name'] = row[2]
                    user['user_icon'] = row[3]

                    users.append(user)
                # with代码块结束,关闭游标
        finally:
            #关闭数据连接
            self.close()

        return users
