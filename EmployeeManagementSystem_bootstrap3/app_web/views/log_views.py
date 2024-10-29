"""
    记录日志的view函数
"""

from django.shortcuts import render, HttpResponse
import logging

# 获取logger对象
logger = logging.getLogger("logger_study.file")


def log_view(request):

    # 日志级别从低到高
    logger.debug('日志测试 debug 级别')
    logger.info('日志测试 info 级别')
    logger.warning('日志测试 warning 级别')
    logger.error('日志测试 error 级别')
    logger.critical('日志测试 critical 级别')
    return HttpResponse('学习Django框架中的日志')

