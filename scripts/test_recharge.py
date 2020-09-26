import unittest

import requests

from api import logger
from api.api_approve import Approve
from api.api_recharge import ApiTrust
from api.p2p import ApiRegLogin
from tools import common_assert, parser_html


class TestTrust(unittest.TestCase):

    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.session()
        # 获取ApiRegLogin对象
        self.login = ApiRegLogin(self.session)
        self.trust = ApiTrust(self.session)
        # 登录
        self.login.login("13600001111","q123456")

    def tearDown(self) -> None:
        logger.info("正在关闭session对象")
        # 关闭session对象
        self.session.close()

    def test01_trust(self):

        r = self.trust.api_trust()
        logger.info("开户结果:{}".format(r.text))
        try:
            common_assert(self,r)
        except Exception as e:
            logger.error(e)
            raise

        # 调用第三方开户
        result = parser_html(r)
        logger.info("解析开户数据结果为:{}".format(result))
        r = self.session.post(url=result[0],data=result[1])
        print("三方开户结果为:",r.text)
        logger.info("三方开户结果为:{}".format(r.text))
        self.assertIn("OK", r.text)


    def test02_recharge(self):

        r = self.trust.api_recharge_code()
        logger.info("获取充值验证码结果:{}".format(r.status_code))

        r = self.trust.api_recharge(100,8888)
        print("充值结果",r.text)
        # 调用第三方充值
        result = parser_html(r)
        logger.info("解析充值数据结果为:{}".format(result))
        r = self.session.post(url=result[0],data=result[1])
        print("三方充值结果为:",r.text)
        logger.info("三方充值结果为:{}".format(r.text))
        self.assertIn("OK", r.text)