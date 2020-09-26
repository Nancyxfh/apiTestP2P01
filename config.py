import logging
import os
from logging.handlers import TimedRotatingFileHandler

BASE_URL = "http://user-p2p-test.itheima.net"

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
print("config中调用:", os.path.dirname(__file__))

# 日志工具 GetLogger
class GetLogger:
    # 一个日志器记录日志  类属性保存日志器
    __logger = None

    # 获取到这个日志  类方法获取日志器
    @classmethod
    def get_logger(cls):
        # 当获取日志器时,日志器如果是空None
        if cls.__logger is None:
            # __logger进行初始化
            # 日志器的创建
            cls.__logger = logging.getLogger("P2PLogger")
            # 设置级别 总开关
            cls.__logger.setLevel(logging.INFO)

            # 处理器 -- 终端处理器, 时间分隔处理器
            # 终端处理器
            shl = logging.StreamHandler()
            file_name = BASE_PATH + os.sep + "log" + os.sep + "p2p.log"
            # 获取文件处理器
            trfhl = TimedRotatingFileHandler(file_name, when="midnight", interval=1, backupCount=0, encoding="utf-8")

            # 格式化器
            fomatter = logging.Formatter(
                fmt="%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s")

            # 处理器设置格式化器
            shl.setFormatter(fmt=fomatter)
            trfhl.setFormatter(fmt=fomatter)

            # 日志器添加处理器
            cls.__logger.addHandler(shl)
            cls.__logger.addHandler(trfhl)

        return cls.__logger