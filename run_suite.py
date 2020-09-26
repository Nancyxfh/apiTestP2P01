# coding = "utf8"
# 1.导包
import os
import unittest

# 2.定义测试套件
from config import BASE_PATH
from lib.HTMLTestRunner import HTMLTestRunner

suite = unittest.defaultTestLoader.discover("./scripts",pattern="test*.py")

# 3.获取报告存储文件流 并实例化调用runner
report_dir =BASE_PATH + os.sep+ "report" + os.sep+ "report.html"
with open (report_dir,"wb") as f:
    HTMLTestRunner(stream=f).run(suite)





