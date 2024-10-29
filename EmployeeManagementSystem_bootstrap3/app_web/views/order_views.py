""" 订单管理 视图函数 """
import json
import random
from datetime import datetime
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app_web import models
from app_web.utils.bootstrap_mf import BootStrapModelForm
from app_web.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["order_number", "order_creator"]  # 排除order_number  order_creator 字段


def order_list(request):
    """ 订单列表 """
    # 获取订单库中的数据
    queryset_g = models.Order.objects.all().order_by('-id')
    # 实例化OrderModelForm
    form_r = OrderModelForm()

    # 分页功能
    paginate_object = Pagination(request, queryset_g)

    order_context = {
        "form_r": form_r,
        "queryset_g": paginate_object.paginate_queryset,  # 分完页的数据
        "page_string": paginate_object.html_pagination()  # 生成的页码
    }

    return render(request, 'order_list.html', order_context)


@csrf_exempt  # 免除csrf_token验证, 网页端的post请求就可以发送到服务端
def order_add(request):
    """ 新建订单 (Ajax请求)"""
    form_s = OrderModelForm(data=request.POST)
    if form_s.is_valid():
        # print(form_s.cleaned_data)  # 此时没有报错, order_number这个字段,默认为空,需要通过下方代码添加.
        # {'product_name': 'A笔记本电脑', 'order_price': 6000, 'order_status': 1, 'order_creator': < Admin: jason_5 >}

        # 生成动态订单号
        # datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # 额外增加一些不是用户输入的值,--在form_s表单中加入order_number
        form_s.instance.order_number = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # 设置当前已登录系统的管理员为订单创建者,不需要手动选择
        # form_s.instance.order_creator_id = 当前已登录系统的管理员的ID
        form_s.instance.order_creator_id = request.session["login_info"]["id"]

        # 保存到数据库中
        form_s.save()
        return JsonResponse({"status": True})
        # return HttpResponse(json.dumps({"status": True}))  # 与上方JsonResponse的用法代码等效

    return JsonResponse({"status": False, 'error': form_s.errors})


def order_delete(request):
    """ 删除订单 """
    # 获取到要删除订单的ID
    order_id = request.GET.get('orderid')
    # 校验要删除的订单是否存在?
    order_exists = models.Order.objects.filter(id=order_id).exists()
    # 如果在库中查询到不存在,就返回错误信息
    if not order_exists:
        return JsonResponse({"status": False, 'error': "订单数据不存在, 删除失败"})
    # 订单数据存在就到数据库中进行删除
    models.Order.objects.filter(id=order_id).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """ 根据订单ID获取订单详情 """

    """
    方式一:
    # 获取当前订单的id
    order_id = request.GET.get("orderid")
    # 到数据库中拿当前这个id的对象
    row_object = models.Order.objects.filter(id=order_id).first()
    # 校验在库中是否存在
    if not row_object:
        return JsonResponse({"status": False, 'error': "订单数据不存在, 编辑失败"})

    # 数据存在,在数据库中获取到一个对象row_object,
    result = {
        "status": True,
        "data": {
            "product_name": row_object.product_name,
            "order_price": row_object.order_price,
            "order_status": row_object.order_status,
        }
    }
    return JsonResponse(result)
    
    """

    # 方式二:
    # 获取当前订单的id
    order_id = request.GET.get("orderid")
    # 到数据库中拿当前这个id的对象的值,通过.values获取对应字段和其值,形成一个字典.
    row_dict = models.Order.objects.filter(id=order_id).values("product_name", "order_price", "order_status").first()
    # print(row_dict)  # 前端页面点击编辑按钮后,项目后台日志打印出: {'product_name': 'A牌2U服务器', 'order_price': 50000, 'order_status': 2}
    # 校验获取的数据是否存在
    if not row_dict:
        return JsonResponse({"status": False, 'error': "订单数据不存在, 编辑失败"})
    # 数据存在,
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """ 订单编辑 """
    # 获取ID
    order_id = request.GET.get("orderid")
    # 获取对象
    row_object = models.Order.objects.filter(id=order_id).first()
    # 判断对象是否存在
    if not row_object:
        return JsonResponse({"status": False, 'tips': "订单数据不存在, 编辑失败"})

    form_t = OrderModelForm(data=request.POST, instance=row_object)
    # 校验form_s
    if form_t.is_valid():
        # form_s OK的话,保存并返回
        form_t.save()
        return JsonResponse({"status": True})
    # form_s 有问题的话,
    return JsonResponse({"status": False, 'error': form_t.errors})




