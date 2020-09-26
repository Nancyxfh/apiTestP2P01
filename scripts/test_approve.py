import unittest

import requests

from api import logger
from api.api_approve import Approve
from api.p2p import ApiRegLogin
from tools import common_assert

#       认证
class TestApprove(unittest.TestCase):

    def setUp(self) -> None:

        self.session = requests.session()
        self.login = ApiRegLogin(self.session)
        self.approve = Approve(self.session)

    def tearDown(self) -> None:
        logger.info("正在关闭session对象")
        # 关闭session对象
        self.session.close()

    def test01_approve(self):
        self.login.login("13600001111","q123456")
        r = self.approve.api_approve("张三","362322199512036344")

        try:
            common_assert(self,r,status_code=200)
        except Exception as e:
            logger.error(e)
            raise

    def test02_approve_info(self):
        self.login.login("13600001111", "q123456")
        r = self.approve.api_approve_info()

        try:
            common_assert(self, r,status=None)
        except Exception as e:
            logger.error(e)
            raise