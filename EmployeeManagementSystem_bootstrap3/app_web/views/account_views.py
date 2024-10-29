"""
    登录界面的视图函数
"""
from django import forms
from django.shortcuts import render, HttpResponse, redirect

from io import BytesIO

from app_web import models
from app_web.utils.bootstrap_mf import BootStrapForm
from app_web.utils.encrypt import admin_pwd_md5
from app_web.utils.captcha import captcha


class LoginForm(BootStrapForm):
    admin_name = forms.CharField(  # 可能是admin_name
        label="用户名",
        widget=forms.TextInput,  # (attrs={"class": "form-control"})
        required=True  # 默认不能为空
    )
    admin_password = forms.CharField(  # admin_password
        label="密码",
        widget=forms.PasswordInput(render_value=True),  # 没有下方的init函数,加这个参数可实现效果(attrs={"class": "form-control"})
        required=True  # 默认不能为空
    )

    captcha = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True  # 默认不能为空
    )

    def clean_admin_password(self):
        admin_pwd = self.cleaned_data.get("admin_password")
        return admin_pwd_md5(admin_pwd)


# class LoginModelForm(forms.ModelForm):
#     class Meta:
#         model = models.Admin
#         fields = ['admin_name', 'admin_password']


def login(request):
    """ 登录 """

    if request.method == "GET":
        form_m = LoginForm()
        return render(request, 'login.html', {'form_m': form_m})

    form_m = LoginForm(data=request.POST)
    if form_m.is_valid():
        # 验证成功后,获取到的用户名和密码
        # print(form_m.cleaned_data)  # {'admin_name': 'jason_7', 'admin_password': '1ddee8b81f96f875279ef2766ef5319b', 'captcha': 'xxxx}

        # 验证码的校验
        user_input_captcha = form_m.cleaned_data.pop('captcha')
        get_captcha_string = request.session.get('image_captcha_string', "")  # 到session中拿到验证码的字符串,内容可能为空,
        if get_captcha_string.upper() != user_input_captcha.upper():
            form_m.add_error("captcha", "验证码错误")
            return render(request, 'login.html', {'form_m': form_m})

        # 去数据库校验用户名和密码是否一致, 获取用户对象, 如果用户名和密码为错误的,得到的对象是空.
        # admin_object_a = models.Admin.objects.filter(admin_name=form_n.cleaned_data['admin_name'], admin_password=form_n.cleaned_data['admin_password']).first()
        admin_object_a = models.Admin.objects.filter(**form_m.cleaned_data).first()
        if not admin_object_a:
            form_m.add_error("admin_password", "用户名或密码错误")
            return render(request, 'login.html', {'form_m': form_m})

        # 用户名密码输入正确,
        # 网站生成随机字符串; 写到用户浏览器的cookie中;再写入到session中,
        request.session["login_info"] = {  # 在服务端的session中,存储是字典类型的login_info信息,里面有登录用户的id和用户名.
            'id': admin_object_a.id,
            'admin_name': admin_object_a.admin_name
        }
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)  # 对session超时进行重新设置, 设置7天免登录

        return redirect("/admin/list/")

    return render(request, 'login.html', {'form_m': form_m})


def image_captcha(request):
    """ 生成图片验证码 """

    # 调用pillow函数,生成图片
    image_c, captcha_string = captcha()
    print(captcha_string)

    # 写入到自己的session中,(以便于后续获取验证码再进行校验)
    request.session['image_captcha_string'] = captcha_string

    # 给session设置60s超时
    request.session.set_expiry(60)

    stream_a = BytesIO()  # 创建数据流文件stream_a在内存中
    image_c.save(stream_a, 'png')  # 将image_c写到stream_a文件中以png的格式

    return HttpResponse(stream_a.getvalue())


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')





