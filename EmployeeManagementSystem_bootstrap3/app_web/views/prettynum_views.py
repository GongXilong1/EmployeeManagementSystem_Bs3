"""
    项目中靓号管理相关业务功能用到的views视图函数
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from app_web import models
from app_web.utils.pagination import Pagination
from app_web.utils.model_form import PrettyNumModelForm, PrettyNumEditModelForm


def prettynum_list(request):
    """ 靓号列表 """
    # # 检查用户是否已经登录,已登录再继续执行代码,未登录的话跳转到登录页面.
    # login_info = request.session.get("login_info")  # 获取存储登录信息的字典里面的信息
    # if not login_info:
    #     return redirect('/login/')


    # from django.http.request import QueryDict
    # import copy
    # query_dict = copy.deepcopy(request.GET)
    # query_dict._mutable = True
    #
    # query_dict.setlist('current_page', [11])
    # print(query_dict.urlencode())


    # for i in range(20):
    #     models.PrettyNum.objects.create(mobile_number="18816795566", price=10, level=1, status=2)

    # # 写法一
    # queryset_f1 = models.PrettyNum.objects.filter(mobile_number="18513567897", id=6)
    # print(queryset_f1)  # [<PrettyNum: PrettyNum object (6)>]
    # # 写法二:
    # data_dict1 = {"mobile_number": "18513567897", "id": 6}   # 字典为空时,相当于获取所有的
    # queryset_f2 = models.PrettyNum.objects.filter(**data_dict1)
    # print(queryset_f2)  # [<PrettyNum: PrettyNum object (6)>]

    data_dict2 = {}
    search_data = request.GET.get('user_search', "")  # http://127.0.0.1:8000/prettynum/list/?user_search=186
    if search_data:
        data_dict2["mobile_number__contains"] = search_data
    # queryset_f3 = models.PrettyNum.objects.filter(**data_dict2)
    # print(queryset_f3)  # [<PrettyNum: PrettyNum object (6)>]

    queryset_d = models.PrettyNum.objects.filter(**data_dict2).order_by("-level")

    paginate_object = Pagination(request, queryset_d)  # 如果需要每页显示多行,传参加入 page_size=20

    # paginate_queryset_d = paginate_object.paginate_queryset
    # page_string = paginate_object.html_pagination()

    # # 1.根据用户想要访问的页码,计算出起止位置.
    # current_page = int(request.GET.get('current_page', 1))  # http://127.0.0.1:8000/prettynum/list/?current_page=1
    # page_size = 10  # 每页显示10条数据
    # start_value = (current_page - 1) * page_size
    # end_value = current_page * page_size

    # [paginate_object.start_value: paginate_object.end_value]
    # queryset_d = models.PrettyNum.objects.filter(**data_dict2).order_by("-level")[paginate_object.start_value:paginate_object.end_value]
    # Django中.order_by("level")表示按照level字段的asc排序, .order_by("-level")表示level字段的desc排序.

    # # 数据总条数
    # total_count = models.PrettyNum.objects.filter(**data_dict2).order_by("-level").count()
    #
    # # 计算总页数
    # total_page_count, div = divmod(total_count, page_size)
    # if div:
    #     total_page_count += 1

    # # 计算出, 显示当前页的前五页和后五页
    # plus = 5
    # if total_page_count <= 2 * plus + 1:
    #     # 数据库中数据比较少
    #     start_page = 1
    #     end_page = total_page_count
    # else:
    #     # 数据库中数据比较多
    #
    #     # 当前页小于5时(小极值)
    #     if current_page <= plus:
    #         start_page = 1
    #         end_page = 2 * plus + 1  # 前取后不取 +1
    #     else:
    #         # 当前页大于5时
    #         # 当前页 +5 大于总页数时,显示就有问题
    #         if (current_page + plus) > total_page_count:
    #             start_page = total_page_count - 2 * plus
    #             end_page = total_page_count
    #         else:
    #             start_page = current_page - plus
    #             end_page = current_page + plus
    #
    #
    # """
    #         <li><a href="/prettynum/list/?current_page=1">1></a></li>
    #         <li><a href="/prettynum/list/?current_page=2">2</a></li>
    #         <li><a href="/prettynum/list/?current_page=3">3</a></li>
    #         <li><a href="/prettynum/list/?current_page=4">4</a></li>
    #         <li><a href="?current_page=5">5</a></li>
    # """
    #
    # # 页码
    # page_str_list = []
    #
    # # 页码首页
    # page_str_list.append('<li><a href="?current_page={}">首页</a></li>'.format(1))
    #
    # # 上一页
    # if current_page > 1:
    #     previous_page = '<li><a href="?current_page={}">上一页</a></li>'.format(current_page - 1)
    # else:
    #     previous_page = '<li><a href="?current_page={}">上一页</a></li>'.format(1)
    # page_str_list.append(previous_page)
    #
    # # 页码
    # for i in range(start_page, end_page + 1):  # range是前取后不取,所以需要加1
    #     if i == current_page:
    #         ele = '<li class="active"><a href="?current_page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = '<li><a href="?current_page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(ele)
    #
    # # 下一页
    # if current_page > total_page_count:
    #     next_page = '<li><a href="?current_page={}">下一页</a></li>'.format(current_page + 1)
    # else:
    #     next_page = '<li><a href="?current_page={}">下一页</a></li>'.format(total_page_count)
    # page_str_list.append(next_page)
    #
    # # 尾页
    # page_str_list.append('<li><a href="?current_page={}">尾页</a></li>'.format(total_page_count))
    #
    # # 页码跳转框
    # search_string = """
    #             <li>
    #                 <form style="float: left; margin-left: -1px" method="get">
    #                     <input  name="current_page" style="position: relative; float: left; display: inline-block; width: 80px; border-radius: 0;"
    #                             type="text" class="form-control" placeholder="页码">
    #                 <button class="btn btn-default" type="submit">跳转</button>
    #                 </form>
    #             </li>
    # """
    #
    # page_str_list.append(search_string)
    #
    # page_string = mark_safe("".join(page_str_list))

    page_context = {
        "search_data": search_data,
        "queryset_d": paginate_object.paginate_queryset,  # 分完页的数据
        "page_string": paginate_object.html_pagination()  # 生成的页码
    }

    return render(request, 'prettynum_list.html', page_context)


def prettynum_model_form_add(request):
    """ 新建靓号/添加靓号 """
    if request.method == "GET":
        form_d = PrettyNumModelForm()
        return render(request, 'prettynum_model_form_add.html', {"form": form_d})

    # 用户POST提交数据,数据校验.
    form_d = PrettyNumModelForm(data=request.POST)
    if form_d.is_valid():
        # 如果数据合法,然后保存到数据库
        # {'employee_name': 'jason', 'employee_password': '12366', 'employee_age': 23, 'employee_account': Decimal('1200'), 'create_time': datetime.datetime(2016, 8, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'gender': 1, 'department': <Department: IT运维部>}
        # print(form_a.cleaned_data)
        form_d.save()  # form_a会将数据存储到上面定义的model这个类里面
        return redirect('/prettynum/list/')
    # 校验失败(在页面上显示错误信息)

    return render(request, 'prettynum_model_form_add.html', {"form": form_d})


def prettynum_edit(request, nid):
    """ 编辑靓号 对接class PrettyNumEditModelForm 不可编辑手机号 """
    row_object_d = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form_d = PrettyNumEditModelForm(instance=row_object_d)  # instance=row_object_b 加上这个参数,在编辑的时候就会显示出之前的默认值
        return render(request, 'prettynum_edit.html', {"form": form_d})

    form_d = PrettyNumEditModelForm(data=request.POST, instance=row_object_d)  # 将用户提交是数据更新到form_c
    if form_d.is_valid():
        form_d.save()
        return redirect('/prettynum/list/')

    return render(request, 'prettynum_edit.html', {"form": form_d})


def prettynum_delete(request):  # , nid
    """ 删除靓号 """

    # 新加功能:在点击删除按钮后,要弹出确认是否要删除的提示框.
    # 获取到要删除管理员的ID
    prettynum_id = request.GET.get('prettynum_id')

    # 校验要删除的管理员是否存在?
    prettynum_exists = models.PrettyNum.objects.filter(id=prettynum_id).exists()
    # 如果在库中查询到不存在,就返回错误信息
    if not prettynum_exists:
        return JsonResponse({"status": False, 'error': "靓号数据不存在, 删除失败"})
    # 管理员数据存在就到数据库中进行删除
    models.PrettyNum.objects.filter(id=prettynum_id).delete()
    return JsonResponse({"status": True})

    # models.PrettyNum.objects.filter(id=nid).delete()
    # return redirect('/prettynum/list/')

