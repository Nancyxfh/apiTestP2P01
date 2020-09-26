from api import logger
from config import BASE_URL

class Loan():

    # 1.初始化
    def __init__(self, session):

        logger.info("初始化session对象: {}".format(session))

        self.session = session
        # 获取投资产品详情url
        self.loan_URL = BASE_URL + "/common/loan/loaninfo"
        # 投资url
        self.tender_URL = BASE_URL + "/trust/trust/tender"
        # 获取投资列表URL
        self.tenderlist_URL = BASE_URL + "/loan/tender/mytenderlist"

    def api_loan_info(self,id):
        data = {
            "id": id
        }
        logger.info("正在调用投资产品详情请求url:{}".format(self.loan_URL))
        return self.session.post(self.loan_URL,data =data)

    def api_tender(self, id, amount):
        data = {
            "id": id,
            "depositCertificate": "-1",
            "amount" : amount
        }
        logger.info("正在调用投资接口 请求url:{}".format(self.tender_URL))
        return self.session.post(self.tender_URL, data=data)

    def api_tenderlist(self,status):
        data = {
            "page": 1,
            "status": status
        }
        logger.info("正在调用投资列表接口 请求url:{}".format(self.tenderlist_URL))
        return self.session.post(self.tenderlist_URL, data=data)