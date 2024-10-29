""" 体验中间件的 鉴权鉴权类 的工作过程 """

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    """ 登录鉴权中间件 """
    def process_request(self, request) :
        # 0. 排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL
        if request.path_info in ["/login/", "/image/captcha/"]:
            return

        # 1. 读取当前访问的用户的session信息,如果能读到,说明已经登录,就可以继续向后执行代码.
        login_info_dict = request.session.get('login_info')
        # print(login_info_dict)  # {'id': 7, 'admin_name': 'jason_5'}
        if login_info_dict:
            return

        # 2. 没有读取到当前用户的session信息,返回到 登录页面.
        return redirect('/login/')






#
# 中间件功能使用示例:
# class MiddlewareA(MiddlewareMixin):
#     """ 中间件A """
#     def process_request(self, request):
#         # 如果方法中没有返回值 (返回None),命令可以继续执行,
#         # 如果有返回值,HttpResponse, render, redirect, 则不再继续向后执行.
#
#         print("MiddlewareA.rocess_request")
#         return HttpResponse("无权访问")
#         # MiddlewareA.rocess_request
#         # MiddlewareA.process_response
#
#     def process_response(self, request, response):
#         print("MiddlewareA.process_response")
#         return response
#
#
# class MiddlewareB(MiddlewareMixin):
#     """ 中间件A """
#     def process_request(self, request):
#         print("MiddlewareB.process_request")
#
#     def process_response(self, request, response):
#         print("MiddlewareB.process_response")
#         return response
