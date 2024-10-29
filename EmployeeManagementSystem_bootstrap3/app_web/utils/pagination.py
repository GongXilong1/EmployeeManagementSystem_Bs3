"""
自定义分页组件
以后如果想要使用这个分页组件,你需要做如下几件事:

在视图函数中:
    def prettynum_list(request):
         靓号列表
        # 1.根据自己的情况去筛选自己的数据
        queryset_d = models.PrettyNum.objects.filter(**data_dict2).order_by("-level")

        # 2.实例化分页对象
        paginate_object = Pagination(request, queryset_d)

        page_context = {
            "queryset_d": paginate_object.paginate_queryset,  # 分完页的数据
            "page_string": paginate_object.html_pagination()  # 生成的页码
        }

        return render(request, 'prettynum_list.html', page_context)

在HTML页面中

    {% for obj in queryset_d %}
        {{ obj.xxx }}
    {% endfor %}


    <ul class="pagination">
        {{ page_string }}
    </ul>

"""

import copy
from django.utils.safestring import mark_safe
from django.http.request import QueryDict


class Pagination(object):
    def __init__(self, request, queryset_d, page_size=10, page_param="current_page", plus=5):
        """
        :param request: 请求的对象
        :param queryset_d:符合条件的数据(根据这个数据给他进行分页处理)
        :param page_size:每页显示多少条数据
        :param page_param:在URL中传递的获取分页的参数,例如:xxx/prettynum/list/?current_page=8
        :param plus:显示当前页的向前某几页或向后某几页(根据页码).
        """

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        current_page = request.GET.get(page_param, "1")

        if current_page.isdecimal():  # 判断当前页是否为小数.
            current_page = int(current_page)  # 将字符串转化成整型
        else:
            current_page = 1

        self.current_page = current_page
        # print(current_page, type(current_page))    #   8 <class 'int'>    abc <class 'str'>
        self.page_size = page_size

        self.start_value = (current_page - 1) * page_size
        self.end_value = current_page * page_size

        self.paginate_queryset = queryset_d[self.start_value:self.end_value]

        # 数据总条数
        total_count = queryset_d.count()

        # 计算总页数
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html_pagination(self):
        # 计算出, 显示当前页的前五页和后五页
        # plus = 5
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中数据比较少
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中数据比较多

            # 当前页小于5时(小极值)
            if self.current_page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1  # 前取后不取 +1
            else:
                # 当前页大于5时
                # 当前页 +5 大于总页数时,显示就有问题
                if (self.current_page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.current_page - self.plus
                    end_page = self.current_page + self.plus

        # 页码
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        # print(self.query_dict.urlencode())

        # 页码首页
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.current_page > 1:
            self.query_dict.setlist(self.page_param, [self.current_page - 1])
            previous_page = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            previous_page = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(previous_page)

        # 页码
        for i in range(start_page, end_page + 1):  # range是前取后不取,所以需要加1
            self.query_dict.setlist(self.page_param, [i])
            if i == self.current_page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.current_page < self.total_page_count:
            # 在排查整个项目的漏洞时发现,点击下一页的时候会直接显示到最后一页,仔细对比代码发现:这里的比较符号方向在之前是错的(更新于2024.4.15.16.21),修改后功能正常了.
            self.query_dict.setlist(self.page_param, [self.current_page + 1])
            next_page = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next_page = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next_page)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        # 页码跳转框
        search_string = """
                        <li>
                            <form style="float: left; margin-left: -1px" method="get">
                                <input  name="current_page" style="position: relative; float: left; display: inline-block; width: 80px; border-radius: 0;"
                                        type="text" class="form-control" placeholder="页码">
                            <button class="btn btn-default" type="submit">跳转</button>
                            </form>
                        </li>
            """

        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))

        return page_string




