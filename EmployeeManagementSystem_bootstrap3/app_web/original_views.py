"""
    django项目中原始的view视图函数
"""

from django.shortcuts import render, redirect
from app_web import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from app_web.utils.pagination import Pagination
from app_web.utils.bootstrap_mf import BootStrapModelForm
from app_web.utils.model_form import EmployeeModelForm, PrettyNumModelForm, PrettyNumEditModelForm

# Create your views here.


def department_list(request):
    """ 部门列表 """

    # 去数据库中获取所有的部门列表
    # queryset类型是:列表中放多个对象,每个对象中封装着他的一行的数据    [对象,对象]
    queryset_a = models.Department.objects.all()

    paginate_object_a = Pagination(request, queryset_a, page_size=3)

    page_context = {"queryset_a": paginate_object_a.paginate_queryset,
                    "page_string": paginate_object_a.html_pagination(),
                    }

    return render(request, 'department_list.html', page_context)
    # 把queryset_a当做参数传递给render,django在内部模版渲染的时候就会取到queryset_a


def department_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, 'department_add.html')

    # 获取用户通过POST提交过来的数据(暂时忽略title内容为空)
    submit_title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=submit_title)

    # 重定向回到部门列表页面
    return redirect("/department/list/")


def department_delete(request):
    """删除部门"""
    # 删除ID   http://127.0.0.1:8000/department/delete/?nid=1
    nid = request.GET.get('nid')

    # 删除
    models.Department.objects.filter(id=nid).delete()

    # 重定向回到部门列表
    return redirect("/department/list/")


def department_edit(request, nid):
    """ 修改部门 """

    if request.method == "GET":
        # 根据nid获取当前部门的数据信息
        row_object = models.Department.objects.filter(id=nid).first()
        # print(row_object.id, row_object.title)
        return render(request, 'department_edit.html', {"row_object": row_object})

    # 获取用户提交的标题
    post_title = request.POST.get("title")

    # 根据ID找到数据库中的数据并进行更新.
    models.Department.objects.filter(id=nid).update(title=post_title)

    # 重定向回到部门列表
    return redirect("/department/list/")


def employee_list(request):
    """ 用户/员工管理 """

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


# ################################# ModelForm示例 #################################


class EmployeeModelForm(BootStrapModelForm):
    employee_name = forms.CharField(
        min_length=2,
        max_length=30,
        label="姓名"
    )  # 对于表单上需要提交的每一个字段进行合法校验

    class Meta:
        model = models.EmployeeInfo
        fields = ["employee_name",
                  "employee_password",
                  "employee_age",
                  "employee_account",
                  "create_time",
                  "gender",
                  "department"
                  ]
        """
        直接的比较麻烦的方法:
        widgets = {
            "employee_name": forms.TextInput(attrs={"class": "form-control"}),
            "employee_password": forms.PasswordInput(attrs={"class": "form-control"}),
            "employee_age": forms.TextInput(attrs={"class": "form-control"})
        }
        """

    # # 重新定义init方法
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)  # 执行init父类的方法
    #
    #     # 循环找到所有的插件,添加"class": "form-control"的样式
    #     for field_name, fields_a in self.fields.items():
    #         # print(field_name, fields_a)
    #         """
    #         打印出的内容如下:
    #         employee_name <django.forms.fields.CharField object at 0x0000027CB2703580>
    #         employee_password <django.forms.fields.CharField object at 0x0000027CB27035B0>
    #         employee_age <django.forms.fields.IntegerField object at 0x0000027CB27034C0>
    #         employee_account <django.forms.fields.DecimalField object at 0x0000027CB2703670>
    #         create_time <django.forms.fields.DateTimeField object at 0x0000027CB2703730>
    #         gender <django.forms.fields.TypedChoiceField object at 0x0000027CB27037C0>
    #         department <django.forms.models.ModelChoiceField object at 0x0000027CB2703910>
    #         """
    #         """
    #         也可以通过判断让某个字段不加样式
    #         if field_name == "employee_password":
    #             continue
    #         """
    #
    #         # 通过for循环,找到所有字段中的插件,给所有的字段加上一个"class": "form-control"参数
    #         # 字段中有属性,保留原来的属性,如果没有属性,我们再给他增加属性
    #         if fields_a.widget.attrs:
    #             fields_a.widget.attrs["class"] = "form-control"
    #             fields_a.widget.attrs["placeholder"] = fields_a.label
    #
    #         else:
    #             fields_a.widget.attrs = {
    #                 "class": "form-control",
    #                 "placeholder": fields_a.label
    #             }


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


def employee_delete(request, nid):
    """ 员工删除 """
    models.EmployeeInfo.objects.filter(id=nid).delete()
    return redirect('/employee/list/')


def prettynum_list(request):
    """ 靓号列表 """

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


"""
# 关于数字条件判断的代码:
models.PrettyNum.objects.filter(id=6)       # 等于6
models.PrettyNum.objects.filter(id__gt=6)   # 大于6
models.PrettyNum.objects.filter(id__gte=6)  # 大于等于6
models.PrettyNum.objects.filter(id__lt=6)   # 小于6
models.PrettyNum.objects.filter(id__lte=6)  # 小于等于6
# 写法二
data_dict2 = {"id__lte": 6}
models.PrettyNum.objects.filter(**data_dict2)



# 关于字符串条件判断代码:
models.PrettyNum.objects.filter(mobile_number="185")  # 表示等于185的筛选出来
models.PrettyNum.objects.filter(mobile_number__startswith="185")  # __startswith表示以185开头的筛选出来
models.PrettyNum.objects.filter(mobile_number__endswith="185")  # __endswith表示以185结尾的筛选出来
models.PrettyNum.objects.filter(mobile_number__contains="185")  # __contains表示包含185的筛选出来
# 写法二:
data_dict3 = {"mobile_number__contains": "185"}
models.PrettyNum.objects.filter(**data_dict3)
"""

"""
# 分页
# 第一页
queryset_f1 = models.PrettyNum.objects.all()[0:10]
# 第二页
queryset_f2 = models.PrettyNum.objects.all()[10:20]
# 第三页
queryset_f3 = models.PrettyNum.objects.all()[20:30]
"""


class PrettyNumModelForm(BootStrapModelForm):
    # 提交信息的验证: 方式一:字段＋正则表达式
    mobile_number = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误,必须以1开头的11位数字')],  # ^1[3-9]\d{9}$  是正则表达式
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile_number", "price", "level", "status"]  # 写法一:写出指定字段
        # fields = "__all__"  # 写法二:所有字段
        # exclude = ['level']  # 写法三: 排除某个字段,其他的都显示

    # # 重新定义init方法
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)  # 执行init父类的方法
    #
    #     # 循环找到所有的插件,添加"class": "form-control"的样式
    #     for field_name, fields_a in self.fields.items():
    #         # 通过for循环,找到所有字段中的插件,给所有的字段加上一个"class": "form-control"参数
    #         fields_a.widget.attrs = {"class": "form-control", "placeholder": fields_a.label}

    # 提交信息的验证: 方式二:钩子方法
    def clean_mobile_number(self):  # 上面class meta定义了字段名后,这里可用clean_字段名  来定义钩子方法
        import_mobile_number = self.cleaned_data["mobile_number"]
        # import_mobile_number是用户传入的数据    self.cleaned_data是用户输入的所有的值,这里只获取"mobile_number"

        import_exists = models.PrettyNum.objects.filter(mobile_number=import_mobile_number).exists()
        if import_exists:
            raise ValidationError("手机号已存在")
        # if len(import_mobile_number) != 11:
        #     # 验证不通过提示错误信息
        #     raise ValidationError("手机号格式错误, 不满11位")

        # 验证通过,把用户输入的信息返回
        return import_mobile_number


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


class PrettyNumEditModelForm(BootStrapModelForm):
    # mobile_number = forms.CharField(disabled=True, label="手机号")  # 限制字段mobile_number显示但不可编辑

    mobile_number = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误,必须以1开头的11位数字')],  # ^1[3-9]\d{9}$  是正则表达式
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile_number", "price", "level", "status"]  # 去掉mobile_number字段后, 只允许用户编辑价格 级别 状态  手机号不可编辑

    # # 重新定义init方法
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)  # 执行init父类的方法
    #
    #     # 循环找到所有的插件,添加"class": "form-control"的样式
    #     for field_name, fields_a in self.fields.items():
    #         # 通过for循环,找到所有字段中的插件,给所有的字段加上一个"class": "form-control"参数
    #         fields_a.widget.attrs = {"class": "form-control", "placeholder": fields_a.label}

    def clean_mobile_number(self):
        # print(self.instance.pk)  # 打印出当前编辑那一行的id
        import_mobile_number = self.cleaned_data["mobile_number"]

        import_exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(
            mobile_number=import_mobile_number).exists()
        if import_exists:
            raise ValidationError("手机号已存在")
        # 验证通过,把用户输入的信息返回
        return import_mobile_number


"""
没有用modelform的函数--已经可以运行使用
def prettynum_edit(request, nid):
    # 编辑靓号 
    row_object_d = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据(对象)
        # row_object_b = models.EmployeeInfo.objects.filter(id=nid).first()

        form_d = PrettyNumModelForm(instance=row_object_d)  # instance=row_object_b 加上这个参数,在编辑的时候就会显示出之前的默认值
        return render(request, 'prettynum_edit.html', {"form": form_d})

    # row_object_b = models.EmployeeInfo.objects.filter(id=nid).first()
    form_d = PrettyNumModelForm(data=request.POST, instance=row_object_d)  # 将用户提交是数据更新到form_c
    if form_d.is_valid():
        # 默认保存的是用户输入的所有数据, 如果想要在用户输入以外增加一些值,可通过以下代码实现.
        # form_d.instance.字段名 = 1123(某个值)
        form_d.save()
        return redirect('/prettynum/list/')

    return render(request, 'prettynum_edit.html', {"form": form_d})
"""


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


def prettynum_delete(request, nid):
    """ 删除靓号 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/prettynum/list/')
