from api import logger
from config import BASE_URL

class ApiTrust():

    # 1.初始化
    def __init__(self, session):

        logger.info("初始化session对象: {}".format(session))

        self.session = session
        # 获取开户url
        self.trust_URL = BASE_URL + "/trust/trust/register"
        # 获取获取充值验证码url
        self.recharge_code_URL = BASE_URL + "/common/public/verifycode/{}"
        # 充值url
        self.recharge_URL = BASE_URL + "/trust/trust/recharge"

    def api_trust(self):

        logger.info("正在调用开户接口 请求url:{}".format(self.trust_URL))

        return self.session.post(self.trust_URL)

    def api_recharge_code(self):

        logger.info("正在调用充值验证码接口 请求url:{}".format(self.recharge_code_URL))

        return self.session.post(self.recharge_code_URL.format(0.1426580900762553))

    def api_recharge(self,amount,code):
        data = {
            "paymentType": "chinapnrTrust",
            "amount": amount,
            "formStr": "reForm",
            "valicode": code
        }
        logger.info("正在调用充值接口 请求url:{}".format(self.recharge_URL))
        return self.session.post(self.recharge_URL,data=data)