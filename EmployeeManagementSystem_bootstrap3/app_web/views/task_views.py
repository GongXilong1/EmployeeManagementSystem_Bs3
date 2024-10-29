""" 任务管理视图函数 """
import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app_web import models
from app_web.utils.bootstrap_mf import BootStrapModelForm
from app_web.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    """ 任务列表函数的ModelForm类 """
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "task_detail": forms.Textarea,  # 文本输入框区域比较大
            "task_detail": forms.TextInput,  # 普通的一行输入框
        }


def task_list(request):
    """ 任务列表 """
    # 去数据库获取所有的任务
    queryset_f = models.Task.objects.all().order_by('-id')  # 用id倒序排列

    # 分页功能
    paginate_object = Pagination(request, queryset_f)
    # 实例化TaskModelForm
    form_p = TaskModelForm()

    task_context = {
        "form_p": form_p,
        "queryset_f": paginate_object.paginate_queryset,  # 分完页的数据
        "page_string": paginate_object.html_pagination()  # 生成的页码

    }
    return render(request, "task_list.html", task_context)


@csrf_exempt   # 免除csrf_token验证, 网页端的post请求就可以发送到服务端
def task_ajax(request):
    """ Ajax """

    print(request.GET)  # 打印出的内容: <QueryDict: {'n1': ['123'], 'n2': ['456']}>
    print(request.POST)  # 打印出的内容: <QueryDict: {'n1': ['123'], 'n2': ['456']}>

    data_dict = {"status": True, 'data': [11, 22, 33, 44]}
    # json_string = json.dumps(data_dict)
    return HttpResponse(json.dumps(data_dict))  # 前端控制台返回:{"status": true, "data": [11, 22, 33, 44]}

    # return JsonResponse(data_dict)


@csrf_exempt
def task_add(request):
    """ 接受Ajax请求的任务添加界面 """
    # print(request.POST)
    # 项目后台打印出的: <QueryDict: {'task_level': ['1'], 'task_title': ['hhh]'], 'task_detail': ['hasdfhs'], 'task_responsible_person': ['7']}>

    # 1. 用户发送过来的数据进行校验(利用ModelForm进行校验)
    form_q = TaskModelForm(data=request.POST)
    if form_q.is_valid():
        form_q.save()
        data_dict = {"status": True}  # 验证成功后,将"status": True返回给前端
        return HttpResponse(json.dumps(data_dict))

    # print(type())  # 后端打印 <class 'django.forms.utils.ErrorDict'>
    from django.forms.utils import ErrorDict
    data_dict = {"status": False, 'error': form_q.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


"""
    关于xxx_id和xxxid的命名规定:前端代码都使用xxxid命名,后端代码都使用xxx_id命名.
"""


def task_detail(request):
    """ 根据任务ID获取任务详情 """
    # 获取当前订单的id
    task_id = request.GET.get("taskid")
    # print(task_id)
    # 到数据库中拿当前这个id的对象的值,通过.values获取对应字段和其值,形成一个字典.
    row_dict = models.Task.objects.filter(id=task_id).values("task_level", "task_title", "task_detail", "task_responsible_person").first()
    # print(row_dict)  # 前端页面点击编辑按钮后,项目后台日志打印出: {'product_name': 'A牌2U服务器', 'order_price': 50000, 'order_status': 2}
    # 校验获取的数据是否存在
    if not row_dict:
        return JsonResponse({"status": False, 'error': "任务数据不存在, 编辑失败"})
    # 数据存在,
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)   # JsonResponse的的作用是JSON序列化


@csrf_exempt
def task_edit(request):
    """  任务编辑 """
    # 获取ID
    task_id = request.GET.get("taskid")
    print(task_id)
    # 获取对象
    row_object = models.Task.objects.filter(id=task_id).first()
    # print(row_object)
    # 判断对象是否存在
    if not row_object:  # row对象不存在的情况
        return JsonResponse({"status": False, 'tips': "任务数据不存在, 编辑失败"})

    # row对象存在的情况
    form_t = TaskModelForm(data=request.POST, instance=row_object)
    # print(form_t)
    # 校验form_s
    if form_t.is_valid():
        # form_t OK的话,保存并返回
        form_t.save()
        return JsonResponse({"status": True})
    # form_t 有问题的话,
    return JsonResponse({"status": False, 'error': form_t.errors})


def task_delete(request):
    """ 任务删除 """

    # 新加功能:在点击删除按钮后,要弹出确认是否要删除的提示框.
    # 获取到要删除管理员的ID
    task_id = request.GET.get('task_id')

    # 校验要删除的管理员是否存在?
    task_exists = models.Task.objects.filter(id=task_id).exists()
    # 如果在库中查询到不存在,就返回错误信息
    if not task_exists:
        return JsonResponse({"status": False, 'error': "订单数据不存在, 删除失败"})
    # 管理员数据存在就到数据库中进行删除
    models.Task.objects.filter(id=task_id).delete()
    return JsonResponse({"status": True})




