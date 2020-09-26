import json
import os

import pymysql
from bs4 import BeautifulSoup
from api import logger

from config import BASE_PATH

# status description status_code断言
def common_assert(self, response, status=None, status_code=200, description=None):
    self.assertEqual(status_code, response.status_code)

    if status:  # status不为None执行

        self.assertEqual(status, response.json().get("status"))
        print("响应文本", response.json())

    if description:  # 不为None条件成立
        self.assertIn(description, response.json().get("description"))


# 读取json工具
def read_json(filename, case_name):
    file_path = BASE_PATH + os.sep + "data" + os.sep + filename
    arrs = []
    with open(file_path, "r", encoding="utf-8") as f:
        for data in json.load(f).get(case_name):
            arrs.append(tuple(data.values())[1:])
        return arrs


# 提取三方请求工具
def parser_html(response):
    # 提取html
    h = response.json().get("description").get("form")
    print("html提取内容为:{}".format(h))
    # 使用sp4进行解析
    bs = BeautifulSoup(h,"html.parser")
    # 提取url
    URL = bs.form.get("action")
    print("URL提取内容为:{}",URL)
    data = {}
    for input in bs.find_all("input"):
        data[input.get("name")]=input.get("value")
    # 返回url 和 字典数据
    return URL, data

class DBUtil:
  @classmethod
  def mysql_conn(cls):
    conn = pymysql.connect(host="52.83.144.39",
                           user="root",
                           password="Itcast_p2p_20191228",
                           database="czbk_member",
                           port=3306,
                           charset="utf8")
    cursor = conn.cursor()
    sql = """delete l.* from mb_member_login_log l INNER JOIN mb_member m on l.member_id = m.id WHERE m.phone in ("13600001111","13900001111", "13600001112","13600001113","13600001114","13600001115","13600001116","13600001111","13530673646","13700041147");"""
    r =cursor.execute(sql)
    conn.commit()
    print("sql执行结果：{}".format(r))
    print("sql语句为:{}".format(sql))
    logger.info("sql执行结果：{}".format(r))

    sql = """DELETE i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ("13600001111","13900001111", "13600001112","13600001113","13600001114","13600001115","13600001116","13600001111","13530673646","13700041147");"""

    cursor.execute(sql)
    conn.commit()
    print("sql执行结果：{}".format(r))
    print("sql语句为:{}".format(sql))
    logger.info("sql执行结果：{}".format(r))

    sql = """delete from mb_member where phone in ("13600001111","13900001111", "13600001112","13600001113","13600001114","13600001115","13600001116","13600001111","13530673646","13700041147");"""
    cursor.execute(sql)
    conn.commit()
    print("sql执行结果：{}".format(r))
    print("sql语句为:{}".format(sql))
    logger.info("sql执行结果：{}".format(r))

    sql = """DELETE from mb_member_register_log where phone in ("13600001111","13900001111", "13600001112","13600001113","13600001114","13600001115","13600001116","13600001111","13530673646","13700041147");"""
    cursor.execute(sql)
    conn.commit()
    print("sql执行结果：{}".format(r))
    print("sql语句为:{}".format(sql))
    logger.info("sql执行结果：{}".format(r))

    cursor.close()
    conn.close()

