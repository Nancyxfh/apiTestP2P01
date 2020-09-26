import random
import unittest
import requests

from api import logger
from api.api_approve import Approve
from api.api_loan import Loan
from api.api_recharge import ApiTrust

from api.p2p import ApiRegLogin
from tools import common_assert, parser_html
from tools import DBUtil
phone = "13600001121"
imgVerifycode = "8888"
password = "q123456"
phone_code = "666666"
dy_server = "on"
invite_phone = "13888800002"
id = 874
amount = 100
class TestLoanFlow(unittest.TestCase):
    def setUp(self) -> None:
        # 清除数据
        DBUtil.mysql_conn()
        # 获取session对象
        self.session = requests.session()
        # 获取ApiRegLogin对象
        self.api_reglog = ApiRegLogin(self.session)
        self.approve = Approve(self.session)
        self.trust = ApiTrust(self.session)
        self.loan = Loan(self.session)

    def tearDown(self) -> None:
        logger.info("正在关闭session对象")
        # 关闭session对象
        self.session.close()
        # DBUtil.mysql_conn()

    def test01(self):
        # 1. 获取图片验证码
        r = self.api_reglog.reg_img_code(random.random())
        try:
            self.assertEqual(200, r.status_code)
        except Exception as e:
            logger.error(e)
            raise
        # 2. 获取短信验证码
        self.api_reglog.reg_sms_code(phone,imgVerifycode,type=type)
        # 3. 调用注册接口
        self.api_reglog.reg(phone,
                     password,
                     imgVerifycode,
                     phone_code,
                     dy_server,
                     invite_phone)
        # 4. 登录
        self.api_reglog.login(phone, password)
        # 5.判断是否登录
        self.api_reglog.islogin()
        # 6.认证
        self.approve.api_approve("张三", "362322199512036344")
        # 7.查询认证信息
        self.approve.api_approve_info()
        # 8.开户
        r =self.trust.api_trust()
        # 9.调用第三方开户
        result = parser_html(r)
        logger.info("解析开户数据结果为:{}".format(result))
        r = self.session.post(url=result[0], data=result[1])
        print("三方开户结果为:", r.text)
        logger.info("三方开户结果为:{}".format(r.text))
        self.assertIn("OK", r.text)

        # 10.充值,第三方充值
        r = self.trust.api_recharge_code()
        logger.info("获取充值验证码结果:{}".format(r.status_code))

        r = self.trust.api_recharge(100, 8888)
        print("充值结果", r.json())
        # 调用第三方充值
        result = parser_html(r)
        logger.info("解析充值数据结果为:{}".format(result))
        r = self.session.post(url=result[0], data=result[1])
        print("三方充值结果为:", r.text)
        logger.info("三方充值结果为:{}".format(r.text))
        self.assertIn("OK", r.text)

        # 11.调用投资
        self.loan.api_loan_info(id)
        # 12.第三方投资
        r = self.loan.api_tender(id, amount)
        logger.info("投资结果:{}".format(r.json()))

        print("投资结果", r.json())
        # 调用第三方投资
        result = parser_html(r)
        logger.info("解析投资数据结果为:{}".format(result))
        r = self.session.post(url=result[0], data=result[1])
        print("三方投资结果为:", r.text)
        logger.info("三方投资结果为:{}".format(r.text))

        try:
            self.assertIn("OK", r.text)
        except Exception as e:
            logger.error(e)
            raise



