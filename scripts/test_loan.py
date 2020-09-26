import unittest

import requests

from api import logger
from api.api_loan import Loan

from api.p2p import ApiRegLogin
from tools import common_assert, parser_html


class TestLoan(unittest.TestCase):

    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.session()
        # 获取ApiRegLogin对象
        ApiRegLogin(self.session).login("13600001111","q123456")
        # 获取Loan对象
        self.loan = Loan(self.session)

    def tearDown(self) -> None:
        logger.info("正在关闭session对象")
        # 关闭session对象
        self.session.close()

    def test01_loan_info(self):
        id = 874
        r = self.loan.api_loan_info(id)
        logger.info("申请投资详情结果:{}".format(r.json()))
        try:
            common_assert(self,r,status=200)
        except Exception as e:
            logger.error(e)
            raise


    def test02_loan(self):
        id , amount = 874,100
        r = self.loan.api_tender(id, amount)
        logger.info("投资结果:{}".format(r.text))

        print("投资结果", r.text)
        # 调用第三方投资
        result = parser_html(r)
        logger.info("解析投资数据结果为:{}".format(result))
        r = self.session.post(url=result[0],data=result[1])
        print("三方投资结果为:",r.text)
        logger.info("三方投资结果为:{}".format(r.text))

        try:
            self.assertEqual(200, r.status_code)
        except Exception as e:
            logger.error(e)
            raise

    def test03_tender_list(self):
        status = "tender"
        r = self.loan.api_tenderlist(status)
        logger.info("申请投资详情结果:{}".format(r.text))
        print("投资列表", r.text)
        id =r.json().get("items")[0].get("loan_id")

        try:
            self.assertEqual("642",id)
        except Exception as e:
            logger.error(e)
            raise