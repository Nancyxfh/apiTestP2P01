from time import sleep
import unittest, random, requests
from parameterized import parameterized
from api import logger
from api.p2p import ApiRegLogin


from tools import common_assert

phone = "13600001111"
phone1 = "13600001112"
phone8 = "13600001113"
password = "q123456"
verifycode = "8888"
phone_code = "666666"
dy_server = "on"
invite_phone = "13888800002"


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

    def test01_img_code(self):
        # 调用图片验证码接口
        r = self.api.reg_img_code(random.random())
        # 断言 响应200
        print("响应状态码:", r.status_code)
        try:
            self.assertEqual(200, r.status_code)
        except Exception as e:
            logger.error(e)
            raise

    # 2. 注册 短信验证码
    def test02_sms_code(self):
        # 1. 获取图片验证码 目的: 使用session对象自动记录cookie
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.reg_sms_code(phone, verifycode)
        print("获取短信验证码 结果为: ", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, description="发送成功")
        except Exception as e:
            logger.error(e)
            raise

    # 3. 注册 测试方法
    def test03_reg(self):
        # 1. 获取图片验证码
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        self.api.reg_sms_code(phone, verifycode)
        # 3. 调用注册接口
        r = self.api.reg(phone, password, verifycode, phone_code, invite_phone)
        print("响应状态码:", r.json())
        try:
            # 4. 断言注册信息
            common_assert(self, r, description="注册成功")
        except Exception as e:
            logger.error(e)
            raise

    # 4. 登录 测试方法
    def test04_login(self):
        r = self.api.login(phone, password)

        print("登录结果:", r.json())
        try:
            # 4. 断言登录信息
            common_assert(self, r, description="登录成功")
        except Exception as e:
            logger.error(e)
            raise

    # 5. 是否登录 测试方法
    def test05_is_login(self):
        # 1.调用登录
        self.api.login(phone, password)
        # 2.判断是否登录
        r = self.api.islogin()
        print("登录查询结果:", r.json())
        try:
            common_assert(self, r, description="OK")
        except Exception as e:
            logger.error(e)
            raise

    """逆向  注册图片验证码"""

    # 6. 逆向-注册图片验证码--（随机整数）
    def test06_img_code(self):
        # 调用图片验证码接口
        r = self.api.reg_img_code(random.randint(1, 999999999999))
        # 断言 响应200
        print("响应状态码:", r.status_code)
        try:
            common_assert(self, r, status=None)
        except Exception as e:
            logger.error(e)
            raise

    # 7. 逆向-注册图片验证码--（随机数为空）
    def test07_img_code(self):
        # 调用图片验证码接口
        num = ""
        r = self.api.reg_img_code(num)
        # 断言 响应404
        print("响应状态码:", r.status_code)
        try:
            common_assert(self, r, status_code=404, status=None)
        except Exception as e:
            logger.error(e)
            raise

    # 8. 逆向-注册图片验证码--（随机数为字符串）
    def test08_img_code(self):
        # 调用图片验证码接口
        num = random.sample("asfdfsgttegfgdgsf", 6)
        r = self.api.reg_img_code("".join(num))
        # 断言 响应404
        print("响应状态码:", r.status_code)
        try:
            self.assertEqual(400, r.status_code)
        except Exception as e:
            logger.error(e)
            raise

    """逆向  注册短信验证码"""

    # 9. 注册 短信验证码 手机号为空
    def test09_sms_code_phone_null(self):
        phone = ""
        # 1. 获取图片验证码 目的: 使用session对象自动记录cookie
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.reg_sms_code(phone, verifycode)
        print("获取短信验证码 结果为: ", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, status=100)
        except Exception as e:
            logger.error(e)
            raise

    # 9. 注册 短信验证码 验证码为空
    def test10_sms_code_code_null(self):
        verifycode = ""
        # 1. 获取图片验证码 目的: 使用session对象自动记录cookie
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.reg_sms_code(phone, verifycode)
        print("获取短信验证码 结果为: ", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, status=100, description="图片验证码错误")
        except Exception as e:
            logger.error(e)
            raise

    # 10. 注册 短信验证码 验证码错误
    def test11_sms_code_verify_null(self):
        verifycode = "8889"
        # 1. 获取图片验证码 目的: 使用session对象自动记录cookie
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.reg_sms_code(phone, verifycode)
        print("获取短信验证码 结果为: ", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, status=100, description="图片验证码错误")
        except Exception as e:
            logger.error(e)
            raise

    # 11. 注册 短信验证码 不请求获取图片验证码
    def test12_sms_code_(self):
        # 2. 获取短信验证码
        r = self.api.reg_sms_code(phone, verifycode)
        logger.info("不请求获取图片验证码 响应数据为:{}".format(r.json()))
        print("不请求获取图片验证码 结果为: ", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, status=100, description="图片验证码错误")
        except Exception as e:
            logger.error(e)
            raise

    """注册  逆向"""

    # 3. 注册 测试方法  所有参数
    def test13_register_all_params(self):
        # 1. 获取图片验证码
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        self.api.reg_sms_code(phone1, verifycode)
        # 3. 调用注册接口
        r = self.api.reg(phone1,
                         password,
                         verifycode,
                         phone_code,
                         invite_phone,
                         dy_server)
        print(r.json())
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=200, description="注册成功")
        except Exception as e:
            logger.error(e)
            raise

    # 3. 注册 测试方法  图片验证码错误
    def test14_reg_img_code_err(self):
        verifycode = "8899"
        # 1. 获取图片验证码
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        self.api.reg_sms_code(phone, verifycode)
        # 3. 调用注册接口
        r = self.api.reg(phone,
                         password,
                         verifycode,
                         phone_code,
                         invite_phone,
                         dy_server)
        print(r.json())
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="验证码错误")
        except Exception as e:
            logger.error(e)
            raise

    # 3. 注册 测试方法  短信验证码错误
    def test15_reg_img_code_err(self):

        phone_code = "8899"
        # 1. 获取图片验证码
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        self.api.reg_sms_code(phone, verifycode)
        # 3. 调用注册接口
        r = self.api.reg(phone8,
                         password,
                         verifycode,
                         phone_code,
                         invite_phone,
                         dy_server)
        print(r.json())
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="验证码错误")
        except Exception as e:
            logger.error(e)
            raise

    # 3. 注册 测试方法  手机号存在
    def test16_reg_img_code_err(self):
        phone = "13700041117"
        # 1. 获取图片验证码
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        self.api.reg_sms_code(phone, verifycode)
        # 3. 调用注册接口
        r = self.api.reg(phone,
                         password,
                         verifycode,
                         phone_code,
                         invite_phone,
                         dy_server)
        print(r.json())
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="手机已存在")
        except Exception as e:
            logger.error(e)
            raise

    # 3. 注册 测试方法  密码为空 ---bug
    def test17_reg_img_code_err(self):
        password = ""
        # 1. 获取图片验证码
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        self.api.reg_sms_code(phone, verifycode)
        # 3. 调用注册接口
        r = self.api.reg(phone,
                         password,
                         verifycode,
                         phone_code,
                         invite_phone,
                         dy_server)
        print(r.json())
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="密码不能为空")
        except Exception as e:
            logger.error(e)
            raise

    # 3. 注册 测试方法  未同意协议 --bug
    def test18_reg_img_code_err(self):
        dy_server = "off"
        # 1. 获取图片验证码
        self.api.reg_img_code(random.random())
        # 2. 获取短信验证码
        self.api.reg_sms_code(phone, verifycode)
        # 3. 调用注册接口
        r = self.api.reg(phone, password,
                         verifycode,
                         phone_code,
                         invite_phone,
                         dy_server)

        print(r.json())
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="同意")
        except Exception as e:
            logger.error(e)
            raise

    """登录   逆向"""

    # 4. 登录 测试方法  用户不存在
    def test19_login(self):
        phone = "134220000"
        r = self.api.login(phone, password)

        print("登录结果:", r.json())
        try:
            # 4. 断言登录信息
            common_assert(self, r, status=100, description="用户不存在")
        except Exception as e:
            logger.error(e)
            raise

    # 4. 登录 测试方法  密码为空
    def test20_login(self):
        password = ""
        r = self.api.login(phone, password)

        print("登录结果:", r.json())
        try:
            # 4. 断言登录信息
            common_assert(self, r, status=100, description="密码不能为空")
        except Exception as e:
            logger.error(e)
            raise

    # 4. 登录 测试方法  密码错误次数
    def test21_login_pwd_err_verify(self):
        password = "123error"
        r = self.api.login(phone, password)
        r = self.api.login(phone, password)
        r = self.api.login(phone, password)
        common_assert(self, r, status=100, description="锁定")
        print("登录结果:", r.json())
        logger.info("登录.密码错误1-3次结果:{}".format(r.json()))
        print("暂停60秒.....")
        sleep(60)
        self.api.login(phone,password="q123456")
        try:
            # 4. 断言登录信息
            common_assert(self, r, status=200, description="登录成功")
        except Exception as e:
            logger.error(e)
            raise


    # 5. 登录 测试方法  未登录
    def test22_is_not_login(self):
        # 2.判断是否登录
        r = self.api.islogin()

        try:
            # 4. 断言登录信息
            common_assert(self, r, status=250, description="您未登陆")
        except Exception as e:
            logger.error(e)
            raise
