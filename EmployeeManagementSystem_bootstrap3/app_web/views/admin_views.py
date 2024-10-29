"""
    项目中管理员管理相关业务功能用到的views视图函数
"""

from django.shortcuts import render, redirect
from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from app_web import models
from app_web.utils.pagination import Pagination
from app_web.utils.bootstrap_mf import BootStrapModelForm
from app_web.utils.encrypt import admin_pwd_md5


def admin_list(request):
    """ 管理员列表 """
    # 检查用户是否已经登录,已登录再继续执行代码,未登录的话跳转到登录页面.
    # 用户发来请求,获取cookie中随机字符串,拿着随机字符串去服务端的session中对比,看看有没有
    # login_info = request.session.get("login_info")   # 获取存储登录信息的字典里面的信息
    # # print(login_info)
    # if not login_info:
    #     return redirect('/login/')

    # login_info_dict = request.session['login_info']
    # print(login_info_dict["id"])
    # print(login_info_dict["admin_name"])

    # 构造搜索
    data_dict3 = {}
    search_data = request.GET.get('user_search', "")
    if search_data:
        data_dict3["admin_name__contains"] = search_data
    # 根据搜索条件去数据库获取
    queryset_f = models.Admin.objects.filter(**data_dict3)

    # 分页
    paginate_object_f = Pagination(request, queryset_f)
    content = {
        'queryset_f': paginate_object_f.paginate_queryset,
        'page_string': paginate_object_f.html_pagination(),
        'search_data': search_data
    }

    return render(request, 'admin_list.html', content)


class AdminModelForm(BootStrapModelForm):
    # 确认密码字段
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)  # render_value=True参数表示密码校验不一致后已经输入的值不清空
    )

    class Meta:
        model = models.Admin
        fields = ["admin_name", "admin_password", "confirm_password"]
        widgets = {
            "admin_password": forms.PasswordInput(render_value=True)
        }

    # 输入的密码进行加密
    def clean_admin_password(self):
        """
        这里的函数命名第一次打成了:def clean_admin_name(self): 打错了, 应该是 def clean_admin_password(self):  还排查了好几天,呜呜呜
        """
        first_password = self.cleaned_data.get("admin_password")
        return admin_pwd_md5(first_password)

    # 两次密码输入一致性确认
    def clean_confirm_password(self):
        print(self.cleaned_data)
        # 加密前打印: {'admin_name': 'jason_5', 'admin_password': '123', 'confirm_password': '456'}
        # 加密后打印: {'admin_name': 'jason_7', 'admin_password': '1ddee8b81f96f875279ef2766ef5319b', 'confirm_password': '7899'}

        first_password = self.cleaned_data.get("admin_password")
        # confirm_pwd = self.cleaned_data.get("confirm_password")  # 没有经过加密函数的确认密码
        confirm_pwd = admin_pwd_md5(self.cleaned_data.get("confirm_password"))
        print(confirm_pwd)  # 这里的确认密码已经是密文:d4bfc55d1ba737791ca25859c87f3f7b

        if confirm_pwd != first_password:
            raise ValidationError("密码不一致!")
        # return什么, 此confirm_password字段以后保存到数据库就是什么
        return confirm_pwd  # return的内容会放到cleaned_data中,然后form_h.save()后  会保存到数据库


def admin_add(request):
    """ 新建/添加管理员 """
    admin_add_title = "新建管理员"

    if request.method == "GET":   # 用户向server端请求数据
        form_g = AdminModelForm()
        return render(request, 'common_add.html', {"form": form_g, "add_title": admin_add_title})

    form_h = AdminModelForm(data=request.POST)   # 接收前端用户输入的值
    if form_h.is_valid():
        print(form_h.cleaned_data)  # 打印验证通过之后里面所有的数据
        # 验证通过之后的数据,明文密码是123 打印结果:{'admin_name': 'jason_7', 'admin_password': '1ddee8b81f96f875279ef2766ef5319b', 'confirm_password': '1ddee8b81f96f875279ef2766ef5319b'}
        form_h.save()
        return redirect('/admin/list/')

    return render(request, 'common_add.html', {"form": form_h, "add_title": admin_add_title})


class AdminEditModelForm(BootStrapModelForm):  # 单独定义一个管理员编辑的ModelForm
    class Meta:
        model = models.Admin
        fields = ['admin_name']   # 这里面只允许修改admin_name字段


class AdminResetPasswordModelForm(BootStrapModelForm):
    # 确认密码字段
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)  # render_value=True参数表示密码校验不一致后已经输入的值不清空
    )

    class Meta:
        model = models.Admin
        fields = ['admin_password', 'confirm_password']   # 这里面只允许修改admin_password字段
        widgets = {
            "admin_password": forms.PasswordInput(render_value=True)
        }

    # 输入的密码进行加密
    def clean_admin_password(self):

        first_password = self.cleaned_data.get("admin_password")

        admin_pwd_md5ed = admin_pwd_md5(first_password)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists_a = models.Admin.objects.filter(id=self.instance.pk, admin_password=admin_pwd_md5ed).exists()
        if exists_a:
            raise ValidationError("新密码不能与之前的密码相同")
        return admin_pwd_md5ed

    # 两次密码输入一致性确认
    def clean_confirm_password(self):
        # print(self.cleaned_data)

        first_password = self.cleaned_data.get("admin_password")
        # confirm_pwd = self.cleaned_data.get("confirm_password")  # 没有经过加密函数的确认密码
        confirm_pwd = admin_pwd_md5(self.cleaned_data.get("confirm_password"))
        # print(confirm_pwd)  # 这里的确认密码已经是密文:d4bfc55d1ba737791ca25859c87f3f7b

        if confirm_pwd != first_password:
            raise ValidationError("密码不一致!")
        # return什么, 此confirm_password字段以后保存到数据库就是什么
        return confirm_pwd  # return的内容会放到cleaned_data中,然后form_h.save()后  会保存到数据库


def admin_edit(request, nid):
    """ 编辑管理员 """
    # 能搜到对应的id,是获取到的一个对象,如果获取的id是不存在的id,获取到的就是一个None
    row_object_a = models.Admin.objects.filter(id=nid).first()  # 获取当前的对象
    if not row_object_a:
        # return render(request, 'error.html', {"error_message": "数据不存在"})  # 当nid不存在时候,跳转到错误提示页面
        return redirect('/admin/list/')  # 当nid不存在时候,直接回到管理员列表页面

    admin_add_title = "编辑管理员"

    if request.method == "GET":
        form_i = AdminEditModelForm(instance=row_object_a)  # 默认值是instance=row_object_a
        return render(request, 'common_add.html', {"form": form_i, "add_title": admin_add_title})

    form_j = AdminEditModelForm(data=request.POST, instance=row_object_a)
    if form_j.is_valid():
        form_j.save()
        return redirect('/admin/list/')
    return render(request, 'common_add.html', {"form": form_j, "add_title": admin_add_title})


def admin_delete(request):  #, nid
    """ 删除管理员 """
    # 新加功能:在点击删除按钮后,要弹出确认是否要删除的提示框.

    # 获取到要删除管理员的ID
    admin_id = request.GET.get('admin_id')

    # 校验要删除的管理员是否存在?
    admin_exists = models.Admin.objects.filter(id=admin_id).exists()
    # 如果在库中查询到不存在,就返回错误信息
    if not admin_exists:
        return JsonResponse({"status": False, 'error': "管理员数据不存在, 删除失败"})
    # 管理员数据存在就到数据库中进行删除
    models.Admin.objects.filter(id=admin_id).delete()
    return JsonResponse({"status": True})

    # models.Admin.objects.filter(id=nid).delete()  // 以前用nid传参删除的代码
    # return redirect('/admin/list/')


def admin_reset_password(request, nid):
    """ 管理员密码的重置 """
    row_object_b = models.Admin.objects.filter(id=nid).first()  # 获取当前的对象
    if not row_object_b:
        # return render(request, 'error.html', {"error_message": "数据不存在"})
        return redirect('/admin/list/')

    admin_add_title = "管理员密码重置 - {}".format(row_object_b.admin_name)  # 带着管理员用户名

    if request.method == "GET":
        form_k = AdminResetPasswordModelForm()  # 这里不传instance=row_object_b, 不然页面会显示原来密码的md5密文
        return render(request, 'common_add.html', {"form": form_k, "add_title": admin_add_title})  # "form": form_j,

    form_l = AdminResetPasswordModelForm(data=request.POST, instance=row_object_b)
    if form_l.is_valid():
        form_l.save()
        return redirect('/admin/list/')
    return render(request, 'common_add.html', {"form": form_l, "add_title": admin_add_title})
