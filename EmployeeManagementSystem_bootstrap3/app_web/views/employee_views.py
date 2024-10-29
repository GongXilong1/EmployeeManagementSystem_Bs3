"""
    项目中员工管理相关业务功能用到的views视图函数
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from app_web import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from app_web.utils.pagination import Pagination
from app_web.utils.bootstrap_mf import BootStrapModelForm
from app_web.utils.model_form import EmployeeModelForm, PrettyNumModelForm, PrettyNumEditModelForm


def employee_list(request):
    """ 用户/员工管理 """
    # # 检查用户是否已经登录,已登录再继续执行代码,未登录的话跳转到登录页面.
    # login_info = request.session.get("login_info")   # 获取存储登录信息的字典里面的信息
    # if not login_info:
    #     return redirect('/login/')

    # 获取所有用户列表   [obj,obj]
    queryset_b = models.EmployeeInfo.objects.all()

    paginate_object_b = Pagination(request, queryset_b, page_size=3)

    page_context = {"queryset_b": paginate_object_b.paginate_queryset,
                    "page_string": paginate_object_b.html_pagination(),
                    }

    """
    用python的语法获取数据:

        for obj in queryset_b:
        print(obj.id, obj.employee_name, obj.employee_account, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(), obj.department_id, obj.department.title)
        # obj.create_time.strftime("%Y-%m-%d") 这部分代码表示将obj.create_time这个原始datatime数据类型转换为字符串,并且只保留显示年月日.

        obj.gender  # 获取的是数据库中存储的1或2
        obj.get_gender_display()  # get_字段名称_display()  这个格式获取的是对应的显示名称
        注意: 数据库中在ORM设计的时候,在Django项目中,有choice和元组里嵌套元组的格式,想去取文本,就用Django中提供的get_字段名称_display()这个方式


        # print(obj.department_id)  # 获取数据库中存储的那个字段所对应的值.
        # print(obj.department.title)  # 根据id自动去关联的表中获取那一行数据department对象,这个是django中已经做好的功能.  因为在员工表的创建中预留了department这个字段,用去垮表去获取数据.
    """

    return render(request, 'employee_list.html', page_context)


def employee_add(request):
    """ 添加员工 (原始方式)"""
    """
    原始方式的几点缺陷:
    1.用户提交的数据没有校验.
    2.页面上填写的内容不合法时应该有错误提示.
    3.页面上,每一个对应的字段都需要我们重新写一遍.
    4.关联的数据,都需要手动去获取并展示,在页面中循环得到展示.
    """

    if request.method == "GET":
        add_context = {
            'gender_choices': models.EmployeeInfo.gender_choices,
            'department_list': models.Department.objects.all()
        }
        # 创建字典,用于传参

        return render(request, 'employee_add.html', add_context)

    # 获取用户提交的数据
    submit_name = request.POST.get('submit_name')
    submit_passwd = request.POST.get('submit_passwd')
    submit_age = request.POST.get('submit_age')
    submit_account = request.POST.get('submit_account')
    submit_ctime = request.POST.get('submit_ctime')
    submit_gender = request.POST.get('submit_gender')
    submit_department_id = request.POST.get('submit_department')

    # 将获取的数据添加到数据库中
    models.EmployeeInfo.objects.create(employee_name=submit_name, employee_password=submit_passwd,
                                       employee_age=submit_age,
                                       employee_account=submit_account, create_time=submit_ctime, gender=submit_gender,
                                       department_id=submit_department_id)

    # 数据添加成功后,返回到员工列表页面
    return redirect("/employee/list/")


def employee_model_form_add(request):
    """ 添加员工 (ModelForm版本)"""
    if request.method == "GET":
        form_a = EmployeeModelForm()
        return render(request, 'employee_model_form_add.html', {"form": form_a})

    # 用户POST提交数据,数据校验.
    form_a = EmployeeModelForm(data=request.POST)
    if form_a.is_valid():
        # 如果数据合法,然后保存到数据库
        # {'employee_name': 'jason', 'employee_password': '12366', 'employee_age': 23, 'employee_account': Decimal('1200'), 'create_time': datetime.datetime(2016, 8, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'gender': 1, 'department': <Department: IT运维部>}
        # print(form_a.cleaned_data)
        form_a.save()  # form_a会将数据存储到上面定义的model这个类里面
        return redirect('/employee/list/')
    # 校验失败(在页面上显示错误信息)
    return render(request, 'employee_model_form_add.html', {"form": form_a})


def employee_edit(request, nid):
    """编辑员工信息"""
    row_object_b = models.EmployeeInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据(对象)
        # row_object_b = models.EmployeeInfo.objects.filter(id=nid).first()

        form_b = EmployeeModelForm(instance=row_object_b)  # instance=row_object_b 加上这个参数,在编辑的时候就会显示出之前的默认值
        return render(request, 'employee_edit.html', {"form": form_b})

    # row_object_b = models.EmployeeInfo.objects.filter(id=nid).first()
    form_c = EmployeeModelForm(data=request.POST, instance=row_object_b)  # 将用户提交是数据更新到form_c
    if form_c.is_valid():
        # 默认保存的是用户输入的所有数据, 如果想要在用户输入以外增加一些值,可通过以下代码实现.
        # form_c.instance.字段名 = 1123(某个值)
        form_c.save()
        return redirect('/employee/list/')
    return render(request, 'employee_edit.html', {"form": form_c})


def employee_delete(request):  # , nid
    """ 员工删除 """

    # 新加功能:在点击删除按钮后,要弹出确认是否要删除的提示框.
    # 获取到要删除管理员的ID
    employee_id = request.GET.get('employee_id')

    # 校验要删除的管理员是否存在?
    employee_exists = models.EmployeeInfo.objects.filter(id=employee_id).exists()
    # 如果在库中查询到不存在,就返回错误信息
    if not employee_exists:
        return JsonResponse({"status": False, 'error': "员工数据不存在, 删除失败"})
    # 管理员数据存在就到数据库中进行删除
    models.EmployeeInfo.objects.filter(id=employee_id).delete()
    return JsonResponse({"status": True})


    # models.EmployeeInfo.objects.filter(id=nid).delete()
    # return redirect('/employee/list/')


