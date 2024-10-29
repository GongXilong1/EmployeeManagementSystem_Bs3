from django.db import models


# Create your models here.

class Admin(models.Model):
    """ 管理员 """
    admin_name = models.CharField(verbose_name="管理员用户名", max_length=32)
    admin_password = models.CharField(verbose_name="管理员密码", max_length=64)

    def __str__(self):
        return self.admin_name


class Department(models.Model):
    """ 部门表 """
    # id = models.BigAutoField(verbose_name='ID', primary_key=True)  # BigAutoField指的是Big int类型
    # id = models.AutoField(verbose_name='ID', primary_key=True)  # AutoField指的是int类型
    # id 这列不用手动写,django项目会自动创建自增的ID列, 在apps.py文件中AppWebConfig类中有对应的代码.

    department_name = models.CharField(verbose_name='部门名称', max_length=255)  # 使用CharField函数必须跟max_length参数

    def __str__(self):
        return self.department_name
    # 用 __str__返回对应的title


class EmployeeInfo(models.Model):
    """ 员工表 """
    employee_name = models.CharField(verbose_name='姓名', max_length=64)
    employee_password = models.CharField(verbose_name='密码', max_length=64)
    employee_age = models.IntegerField(verbose_name='年龄')  # 使用IntegerField函数不用跟max_length参数
    employee_account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # max_digits参数表示账户数位是10位, 小数长度为2位. default=0表示默认账户余额为0.
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")  # DateField字段只包含年月日,没有时分秒

    # 无约束写法
    # department_id = models.BigIntegerField(verbose_name='部门ID')

    # 1. 有约束写法:
    # - to: 与哪张表关联
    # - to_field: 与表中的列关联
    # 2. django中自动
    # - 写的department
    # - 使用了ForeignKey函数后, 在生成数据库列的时候department会自动变成department_id.
    # 3. 部门表被删除
    # 3.1 级联删除操作--on_delete=models.CASCADE参数表示采用级联删除.
    department = models.ForeignKey(verbose_name="部门", to="Department", on_delete=models.CASCADE)
    # 3.2 置空操作--null=True, blank=True两个参数表示department_id列可以为空,
    # department = models.ForeignKey(to="Department", to_fields="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django代码中做的约束
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

    """
    department = models.ForeignKey(to="Department", to_fields="id", on_delete=models.CASCADE)  
    改为:
    department = models.ForeignKey(to="Department", on_delete=models.CASCADE)
    """


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile_number = models.CharField(verbose_name="手机号", max_length=32)  # 把手机号存储成字符串类型,方便后期对用户的手机进行正则表达式校验和搜索操作.
    # 想要允许为空, 就在参数中加 null=True, blank=True
    price = models.IntegerField(verbose_name="价格", default=0)  # 价格都是整数

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级")
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)  # 创建靓号时,没有选级别,默认为1级.

    status_choices = (
        (1, "已占用"),
        (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):
    """ 任务管理 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时")
    )
    task_level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    task_title = models.CharField(verbose_name="任务标题", max_length=64)
    task_detail = models.TextField(verbose_name="任务详情")
    # 数据库中会生成task_responsible_person_id字段
    task_responsible_person = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单管理 """
    order_number = models.CharField(verbose_name="订单号", max_length=64)
    product_name = models.CharField(verbose_name="商品名称", max_length=32)
    order_price = models.IntegerField(verbose_name="订单价格")
    order_status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    order_status = models.IntegerField(verbose_name="订单状态", choices=order_status_choices, default=1)
    order_creator = models.ForeignKey(verbose_name="订单创建者", to="Admin", on_delete=models.CASCADE)


class Boss(models.Model):
    """ 老板信息表 """
    boss_name = models.CharField(verbose_name="姓名", max_length=32)
    boss_age = models.IntegerField(verbose_name="年龄")
    boss_image = models.CharField(verbose_name="头像", max_length=128)


class City(models.Model):
    """ 城市信息表 """
    city_name = models.CharField(verbose_name="城市名称", max_length=32)
    city_population = models.IntegerField(verbose_name="城市人口数")
    city_logo = models.FileField(verbose_name="城市Logo", max_length=128, upload_to='city/')
    # FileField字段本质上数据库也是CharField,区别在于用FileField的话文件保存的代码可以不写,django内部自动会做.
    # upload_to=参数表示要上传到media目录下的哪个目录.


class BranchPerformance(models.Model):
    """ 分公司业绩表 """
    branch_name = models.CharField(verbose_name="分公司名称", max_length=32)
    january_performance = models.IntegerField(verbose_name="一月份业绩")
    february_performance = models.IntegerField(verbose_name="二月份业绩")
    march_performance = models.IntegerField(verbose_name="三月份业绩")
    april_performance = models.IntegerField(verbose_name="四月份业绩")
    may_performance = models.IntegerField(verbose_name="五月份业绩")
    june_performance = models.IntegerField(verbose_name="六月份业绩")
    july_performance = models.IntegerField(verbose_name="七月份业绩")
    august_performance = models.IntegerField(verbose_name="八月份业绩")
    september_performance = models.IntegerField(verbose_name="九月份业绩")
    october_performance = models.IntegerField(verbose_name="十月份业绩")
    november_performance = models.IntegerField(verbose_name="十一月份业绩")
    december_performance = models.IntegerField(verbose_name="十二月份业绩")


class EmployeePerformance(models.Model):
    """ 员工业绩表 """



