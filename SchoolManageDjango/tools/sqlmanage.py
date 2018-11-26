#!/usr/bin/env python
import pymysql


def sql_get_all(sql, args=None):
    # fetchall()查询
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="1234", db="db1", charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 查询结果设置为字典形式
    cursor.execute(sql,args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def sql_get_one(sql, args=None):
    # fetchone()查询
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="1234", db="db1", charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def sql_run(sql, args=None):
    # 执行SQL语句
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="1234", db="db1", charset="utf8")
    cursor = conn.cursor()
    cursor.execute(sql,args)
    conn.commit()
    cursor.close()
    conn.close()
