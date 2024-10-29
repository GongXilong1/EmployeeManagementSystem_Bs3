"""
    项目中用到的所有的的ModelForm类都在这里
"""
from app_web import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app_web.utils.bootstrap_mf import BootStrapModelForm


class DepartmentModelForm(BootStrapModelForm):
    department_name = forms.CharField(
        min_length=2,
        max_length=60,
        label="部门名称"
    )  # 对于表单上需要提交的每一个字段进行合法校验

    class Meta:
        model = models.Department
        fields = ["department_name"]


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



