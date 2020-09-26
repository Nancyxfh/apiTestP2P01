import time
import unittest, random, requests
from parameterized import parameterized
from api import logger
from api.p2p import ApiRegLogin


from tools import common_assert,read_json

# phone = "13530673646"
# phone1 = "13700041147"
# phone8 = "13530673649"
# password = "q12345"
# verifycode = "8888"
# phone_code = "666666"
# dy_server = "on"
# invite_phone = "13800001111"


class TestRegLogin(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.session()
        logger.info("正在获取session对象:{}".format(self.session))
        # 获取ApiRegLogin对象
        self.api = ApiRegLogin(self.session)
        logger.info("正在获取ApiRegLogin对象:{}".format(self.api))

    # 结束
    def tearDown(self) -> None:
        logger.info("正在关闭session对象")
        # 关闭session对象
        self.session.close()

    # 1.注册图片验证码 测试方法
    @parameterized.expand(read_json("register_login.json","img_code_case"))
    def test01_img_code(self,random,expect_code):
        # 调用图片验证码接口
        r = self.api.reg_img_code(random)
        # 断言 响应200
        print("响应状态码:", r.status_code)
        try:
            self.assertEqual(expect_code, r.status_code)
        except Exception as e:
            logger.error(e)
            raise

    # 2. 注册 短信验证码
    @parameterized.expand(read_json("register_login.json", "sms_code_case"))
    def test02_sms_code(self,phone,imgverifycode,type,expect_code,expect_status,description):
        # 1. 获取图片验证码 目的: 使用session对象自动记录cookie
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.reg_sms_code(phone,imgverifycode,type=type)
        print("获取短信验证码 结果为: ", r.json())
        try:
            # 调用断言方法
            common_assert(self, r,status_code=expect_code,status=expect_status, description=description)
        except Exception as e:
            logger.error(e)
            raise

    # 3. 注册 测试方法
    @parameterized.expand(read_json("register_login.json", "reg_case"))
    def test03_reg(self,phone4,password,imgVerifyCode,phone_code,dy_server,invite_phone,expect_code,status,description):
        # 1. 获取图片验证码
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        self.api.reg_sms_code(phone4, imgVerifyCode)
        # 3. 调用注册接口
        r = self.api.reg(phone4,
                         password,
                         imgVerifyCode,
                         phone_code,
                         dy_server,
                         invite_phone)
        print("响应状态码:", r.json())
        logger.info("请求数据：{} 响应结果：{}".format(
            (phone4, password, imgVerifyCode, phone_code, dy_server, invite_phone, expect_code, status,
             description), r.json()))
        try:
            # 4. 断言注册信息
            common_assert(self, r,status_code=expect_code,status=status,description=description)
        except Exception as e:
            logger.error(e)
            raise

    # 4. 登录 测试方法
    @parameterized.expand(read_json("register_login.json", "login_case"))
    def test04_login(self,keywords, password, expect_code):
        r = self.api.login(keywords, password)
        logger.info("请求数据：{} 响应数据：{}".format((keywords, password, expect_code), r.json()))

        print("登录结果:", r.json())
        if "error" in password:
            logger.info("锁定60验证...")
            r = self.api.login(keywords, password)
            logger.info("请求数据：{} 响应数据：{}".format((keywords, password, expect_code), r.json()))
            print("登陆结果：", r.json())

            r = self.api.login(keywords, password)
            logger.info("请求数据：{} 响应数据：{}".format((keywords, password, expect_code), r.json()))
            print("登陆结果：", r.json())

            time.sleep(60)
            r = self.api.login("13600001111", "q123456")
            logger.info("请求数据：{} 响应数据：{}".format((keywords, password, expect_code), r.json()))
            print("登陆结果：", r.json())
        try:
            # 4. 断言登录信息
            common_assert(self, r, status_code=expect_code)
        except Exception as e:
            logger.error(e)
            raise

    # 5. 是否登录 测试方法
    @parameterized.expand(read_json("register_login.json", "islogin_case"))
    def test05_is_login(self,phone4,password,expect_code):
        # 1.调用登录
        self.api.login(phone4, password)
        # 2.判断是否登录
        r = self.api.islogin()
        print("登录查询结果:", r.json())
        logger.info("请求数据：{} 执行结果：{}".format((phone4, password, expect_code), r.json()))
        try:
            common_assert(self, r, status=expect_code)
        except Exception as e:
            logger.error(e)
            raise
