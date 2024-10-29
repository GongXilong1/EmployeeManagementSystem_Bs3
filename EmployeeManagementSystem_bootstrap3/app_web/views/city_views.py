""" 城市列表 视图函数 """
from django.shortcuts import render, redirect
from app_web import models
from app_web.utils.bootstrap_mf import BootStrapModelForm


def city_list(request):
    """ 城市列表函数 """
    queryset_a = models.City.objects.all()

    return render(request, 'city_list.html', {'queryset_a': queryset_a})


class UploadModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['city_logo']  # 将city_logo字段不使用BootStrapForm样式

    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    """ 基于 ModelForm上传新建城市的文件和数据 """
    upload_title = "新建城市"

    if request.method == "GET":
        form_a = UploadModelForm
        return render(request, 'upload_form.html', {'form_a': form_a, 'upload_title': upload_title})

    form_a = UploadModelForm(data=request.POST, files=request.FILES)
    if form_a.is_valid():
        # 这一句form_a.save()保存代码,对于文件的话会自动保存的
        # 字段 + 上传路径就写入到数据库.
        form_a.save()
        return redirect("/city/list/")

    return render(request, 'upload_form.html', {'form_a': form_a, 'upload_title': upload_title})














