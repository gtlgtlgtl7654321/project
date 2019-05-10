#把爬下来的csv格式 数据存入到mysql数据库中：

import pymysql
import csv
import logging
logging.basicConfig(level = logging.INFO)

import pandas as pd
# pandas读取文件
# usecols 就是说我只用这些列其他列不需要
# parse_dates 由于csv只储存str、int、float格式无法储存日期格式，所以读取是设定吧日期列读作时间格式
df = pd.read_csv('lvyou_data.csv', encoding='utf-8', usecols=[0,1,2,3,4,5,6,7,8,9,10] )
values = {"级别" : "普通",
    "地址" : " ",
    "特色" : "暂无介绍",
    "价格" : "未知"}


# logging.info(df)
# logging.info("")
df = df.fillna(value = values)
# logging.info(df)
# logging.info("")

# 参数设置 DictCursor使输出为字典模式 连接到本地用户root 密码为123456
config = dict(host='localhost', user='root', password='123456',
             cursorclass=pymysql.cursors.DictCursor
             )
# 建立连接
conn = pymysql.Connect(**config)
# 自动确认commit True
conn.autocommit(1)
# 设置光标
cursor = conn.cursor()


#格式转换，在创建table时需要设置列的类型，这里写一个function 将pandas的类型转换为sql类型：

def make_table_sql(df):
    '''
    一个根据pandas自动识别type来设定table的type
    '''
    columns = df.columns.tolist()
    types = df.ftypes

    # logging.info("columns:")
    # logging.info(columns)
    # logging.info("")
    # logging.info("types:")
    # logging.info(types)
    # logging.info("")

    # 添加id 制动递增主键模式
    make_table = []
    for item in columns:
        if 'int' in types[item]:
            #char = item + ' INT(64)'
            char = item + ' VARCHAR(64)'
        elif 'float' in types[item]:
            char = item + ' FLOAT'
        elif 'object' in types[item]:
            char = item + ' VARCHAR(255)'
        elif 'datetime' in types[item]:
            char = item + ' DATETIME'
        make_table.append(char)
    return ','.join(make_table)


#创建table 并批量写入mysql：
def csv2mysql(db_name, table_name, df):
    '''csv 格式输入 mysql 中'''
    # 如果没有数据库，创建database
    sql_create = 'CREATE DATABASE IF NOT EXISTS {}'.format(db_name)
    cursor.execute(sql_create)

    # 选择连接database
    conn.select_db(db_name)
    # 创建table
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))

    # logging.info(print('DROP TABLE IF EXISTS {}'.format(table_name)))
    # logging.info(print(""))

    cursor.execute('CREATE TABLE {}({})'.format(table_name,make_table_sql(df)))

    # logging.info(print('CREATE TABLE {}({})'.format(table_name,make_table_sql(df))))
    # logging.info(print(""))

    # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
    # df['日期'] = df['日期'].astype('str')
    values = df.values.tolist()

    # logging.info(print("df.values:"))
    # logging.info(df.values)
    # logging.info("values 的长度：")
    # logging.info(len(values))

    # 根据columns个数
    s = ','.join(['%s' for _ in range(len(df.columns))])#11个 %s
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    #cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name,s), values)
    sql='INSERT INTO {} VALUES ({})'.format(table_name,s)
    cursor.executemany( sql , values )

db_name = "lvyou"
table_name = "attractions"
csv2mysql(db_name, table_name , df)

# cursor.execute('SELECT * FROM test1 LIMIT 5')
# # scroll(self, value, mode='relative') 移动指针到某一行; 如果mode='relative',则表示从当前所在行移动value条,如果 mode='absolute',则表示从结果集的第一行移动value条.
# cursor.scroll(4)
# what = cursor.fetchall()
# print (what)


# 光标关闭
cursor.close()
# 连接关闭
conn.close()