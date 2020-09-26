from api import logger
from config import BASE_URL

class Approve():

    # 1.初始化
    def __init__(self, session):

        logger.info("初始化session对象: {}".format(session))

        self.session = session
        # 获取图片验证码url
        self.approve_URL = BASE_URL + "/member/realname/approverealname"
        # 获取手机验证码url
        self.approve_info_URL = BASE_URL + "/member/member/getapprove"

    def api_approve(self, realname, card_id):
        data = {
            "realname":realname,
            "card_id": card_id
        }
        logger.info("正在调用认证接口 请求url:{}".format(self.approve_URL))

        return self.session.post(self.approve_URL,data =data,files={"x":"y"})

    def api_approve_info(self):

        logger.info("正在调用认证信息接口 请求url:{}".format(self.approve_info_URL))

        return self.session.post(self.approve_info_URL)