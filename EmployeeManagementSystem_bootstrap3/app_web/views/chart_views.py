""" 数据统计图表 视图函数 """
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def chart_list(request):
    """ 数据统计图表列表 """
    return render(request, 'chart_list.html')


@csrf_exempt
def chart_line(request):
    """ 构造折线图的数据"""

    # 从数据库中获取数据


    # 手动填写数据
    legend = ['上海分公司', '北京分公司', '广州分公司', '深圳分公司', '浙江分公司']

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月', '7月']

    series_list = [
        {
            "name": '上海分公司',
            "type": 'line',  # 类型:line 表示显示折线图
            "stack": 'Total',
            "data": [120, 132, 101, 134, 90, 230, 210]  # x轴上每一个字段对应的值
        },
        {
            "name": '北京分公司',
            "type": 'line',
            "stack": 'Total',
            "data": [220, 182, 191, 234, 290, 330, 310]
        },
        {
            "name": '广州分公司',
            "type": 'line',
            "stack": 'Total',
            "data": [150, 232, 201, 154, 190, 330, 410]
        },
        {
            "name": '深圳分公司',
            "type": 'line',
            "stack": 'Total',
            "data": [320, 332, 301, 334, 390, 330, 320]
        },
        {
            "name": '浙江分公司',
            "type": 'line',
            "stack": 'Total',
            "data": [820, 932, 901, 934, 1290, 1330, 1320]
        }

    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'x_axis': x_axis,
            'series_list': series_list,
        }
    }

    return JsonResponse(result)


@csrf_exempt
def chart_bar(request):
    """ 构造柱状图的数据 """
    # 数据可以到数据库中获取
    legend = ['高露', '王楚然']

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月', '7月']

    series_list = [
        {
            "name": '高露',
            "type": 'bar',  # 类型:bar 表示显示柱状图
            "data": [5, 20, 36, 10, 10, 30, 60]  # x轴上每一个字段对应的值
        },
        {
            "name": '王楚然',
            "type": 'bar',
            "data": [15, 50, 56, 20, 30, 20, 55]
        }
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'x_axis': x_axis,
            'series_list': series_list,
        }
    }

    return JsonResponse(result)


@csrf_exempt
def chart_pie(request):
    """ 构造饼图的数据 """

    db_data_list = [
        {"value": 1048, "name": 'IT部门'},
        {"value": 735, "name": '运营部'},
        {"value": 580, "name": '新媒体部'},
        {"value": 484, "name": '销售部'},
        {"value": 300, "name": '综合部'}
    ]

    result = {
        "status": True,
        "data": db_data_list,
    }

    return JsonResponse(result)


def highcharts_example(request):
    """ highcharts图表示例 """

    return render(request, 'highcharts_example.html')

