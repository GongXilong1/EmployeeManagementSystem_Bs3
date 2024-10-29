"""
URL configuration for EmployeeManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from app_web.views import department_views, employee_views, prettynum_views, admin_views, account_views, task_views, order_views, chart_views, upload_views, city_views


urlpatterns = [
    # path('admin/', admin.site.urls),

    # 启用media目录
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # re_path是正则表达式

    # 部门管理
    path('department/list/', department_views.department_list),
    path('department/add/', department_views.department_add),
    path('department/model/form/add/', department_views.department_model_form_add),
    path('department/delete/', department_views.department_delete),
    path('department/edit/', department_views.department_edit),
    path('department/<int:nid>/edit/', department_views.department_edit),   # 通过url传递id
    path('department/batch_upload/', department_views.department_batch_upload),

    # 员工管理
    path('employee/list/', employee_views.employee_list),
    path('employee/add/', employee_views.employee_add),
    path('employee/model/form/add/', employee_views.employee_model_form_add),
    path('employee/<int:nid>/edit/', employee_views.employee_edit),
    # path('employee/<int:nid>/delete/', employee_views.employee_delete),
    path('employee/delete/', employee_views.employee_delete),


    # 靓号管理
    path('prettynum/list/', prettynum_views.prettynum_list),
    path('prettynum/model/form/add/', prettynum_views.prettynum_model_form_add),
    path('prettynum/<int:nid>/edit/', prettynum_views.prettynum_edit),
    # path('prettynum/<int:nid>/delete/', prettynum_views.prettynum_delete),
    path('prettynum/delete/', prettynum_views.prettynum_delete),


    # 管理员的管理
    path('admin/list/', admin_views.admin_list),
    path('admin/add/', admin_views.admin_add),
    path('admin/<int:nid>/edit/', admin_views.admin_edit),
    # path('admin/<int:nid>/delete/', admin_views.admin_delete),  # 用nid传参删除
    path('admin/delete/', admin_views.admin_delete),  # 用ajax传参删除
    path('admin/<int:nid>/reset_password/', admin_views.admin_reset_password),

    # 用户登录
    path('login/', account_views.login),
    path('logout/', account_views.logout),
    path('image/captcha/', account_views.image_captcha),

    # 任务管理
    path('task/list/', task_views.task_list),
    path('task/ajax/', task_views.task_ajax),  # 学习Ajax用到的路由
    path('task/add/', task_views.task_add),
    path('task/detail/', task_views.task_detail),
    path('task/edit/', task_views.task_edit),
    path('task/delete/', task_views.task_delete),


    # 订单管理
    path('order/list/', order_views.order_list),
    path('order/add/', order_views.order_add),
    path('order/delete/', order_views.order_delete),
    path('order/detail/', order_views.order_detail),
    path('order/edit/', order_views.order_edit),

    # 数据统计图表
    path('chart/list/', chart_views.chart_list),
    path('chart/line/', chart_views.chart_line),
    path('chart/bar/', chart_views.chart_bar),
    path('chart/pie/', chart_views.chart_pie),
    path('chart/highcharts/', chart_views.highcharts_example),

    # 上传文件
    path('upload/list/', upload_views.upload_list),
    path('upload/form/', upload_views.upload_form),
    path('upload/model/form/', upload_views.upload_model_form),

    # 城市列表
    path('city/list/', city_views.city_list),
    path('city/add/', city_views.city_add),

]



