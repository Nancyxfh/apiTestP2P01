from api import logger
from config import BASE_URL

class ApiRegLogin():

    # 1.初始化
    def __init__(self, session):

        logger.info("初始化session对象: {}".format(session))

        self.session = session
        # 获取图片验证码url
        self.img_URL = BASE_URL + "/common/public/verifycode1/{}"
        # 获取手机验证码url
        self.mess_URL = BASE_URL + "/member/public/sendSms"
        # 注册url
        self.reg_URL = BASE_URL + "/member/public/reg"
        # 登录url
        self.login_URL = BASE_URL + "/member/public/login"
        # 是否登录url
        self.islogin_URL = BASE_URL + "/member/public/islogin"

    # 2. 注册-获取图片验证码
    def reg_img_code(self, random):
        """
        :param random: 随机数
        :return: 响应对象
        """
        logger.info("正在调用注册获取图片验证码接口 请求url:{}".format(self.img_URL.format(random)))
        img_resp = self.session.get(self.img_URL.format(random))
        return img_resp

    # 3. 注册-获取手机验证码
    def reg_sms_code(self, phone, code,type="reg"):
        # 1. 定义请求数据
        sms_data = {'phone': phone,
                    'imgVerifyCode': code,
                    'type': type}
        logger.info("正在调用注册获取手机验证码接口 请求url: {} ".format(self.mess_URL,sms_data))
        # 2. 调用post方法
        sms_resp = self.session.post(self.mess_URL, data=sms_data)
        return sms_resp

    # 4. 注册
    def reg(self, phone, pwd, vercode, phonecode, invite_phone, dy_server="on"):
        # 1. 定义请求数据
        reg_data = {'phone': phone,
                    'password': pwd,
                    'verifycode': vercode,
                    'phone_code': phonecode,
                    'invite_phone': invite_phone,
                    'dy_server':  dy_server
                    }
        logger.info("正在调用注册接口 请求url: {} 请求数据:{}".format(self.reg_URL,reg_data))
        # 2.调用post方法
        reg_resp =self.session.post(self.reg_URL,data=reg_data)
        return reg_resp

    # 5. 登录
    def login(self, phone, password):
        # 1. 定义请求数据
        login_data = {'keywords': phone,
                      'password': password
                    }
        logger.info("正在调用登录接口 请求url:{} 请求数据:{}" .format(self.login_URL,login_data))
        # 2.调用post方法
        log_resp =self.session.post(self.login_URL,data=login_data)
        return log_resp

    # 6. 是否登录
    def islogin(self):
        logger.info("正在调用登录接口 请求url:{} ".format(self.islogin_URL))
        islogin_resp =self.session.post(self.islogin_URL)
        return islogin_resp


# if __name__ == '__main__':
#     session = requests.session()
#     apitest = Api(session)
#     rep = apitest.reg_img_code(0.1112222255)
#     print(rep.status_code)
#
#
#     session.close()




