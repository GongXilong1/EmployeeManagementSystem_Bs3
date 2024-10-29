""" 上传文件 视图函数 """
import os
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.conf import settings
from app_web.utils.bootstrap_mf import BootStrapForm, BootStrapModelForm
from app_web import models


def upload_list(request):
    """ 上传列表函数 """
    if request.method == "GET":

        return render(request, 'upload_list.html')

    # print(request.POST)  # POST是请求体传过来的数据
    # print(request.FILES)  # FILES是请求发过来的文件

    # 前端页面代码没有加enctype="multipart/form-data"属性时,
    # 后台日志打印结果: 'username': ['112'], 'avatar': ['0.jpg']  ,只有图片文件名,没有图片文件

    # 加属性后:
    # <QueryDict: {'csrfmiddlewaretoken': ['s6.............'], 'username': ['666']}>
    # <MultiValueDict: {'avatar': [<InMemoryUploadedFile: 0.jpg (image/jpeg)>]}>
    # [<InMemoryUploadedFile: 0.jpg (image/jpeg)>] 是一个文件对象.

    file_object = request.FILES.get("avatar")
    print(file_object.name)  # 0.jpg

    file_a = open(file_object.name, mode='wb')
    for chunk_a in file_object.chunks():
        file_a.write(chunk_a)
    file_a.close()

    return HttpResponse("...")


class UploadForm(BootStrapForm):

    bootstrap_exclude_fields = ['boss_image']  # 将image字段不使用BootStrapForm样式

    boss_name = forms.CharField(label="姓名")
    boss_age = forms.IntegerField(label="年龄")
    boss_image = forms.FileField(label="头像")


def upload_form(request):
    """ upload Form上传函数 """

    upload_title = "Form上传"

    if request.method == "GET":
        form_a = UploadForm()

        return render(request, 'upload_form.html', {"form_a": form_a, "upload_title": upload_title})

    form_a = UploadForm(data=request.POST, files=request.FILES)
    if form_a.is_valid():
        print(form_a.cleaned_data)  # {'name': '哈哈哈', 'age': 21, 'image': <InMemoryUploadedFile: 0.jpg (image/jpeg)>}

        # 读取到内容,自己处理每个字段的数据,然后存储
        # 1.读取图片内容,写入到文件夹中并获取文件的路径
        image_object = form_a.cleaned_data.get("boss_image")

        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)  # 绝对路径写法
        media_path = os.path.join("media", image_object.name)  # 项目里相对路径写法

        # file_path = os.path.join("app_web", db_file_path)

        file_a = open(media_path, mode='wb')
        for chunk_a in image_object.chunks():
            file_a.write(chunk_a)
        file_a.close()

        # 2. 将图片文件路径写入到数据库
        models.Boss.objects.create(
            boss_name=form_a.cleaned_data['boss_name'],
            boss_age=form_a.cleaned_data['boss_age'],
            boss_image=media_path,
        )

        return HttpResponse("提交成功")

    return render(request, 'upload_form.html', {"form_a": form_a, "upload_title": upload_title})


class UploadModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['city_logo']  # 将city_logo字段不使用BootStrapForm样式

    class Meta:
        model = models.City
        fields = "__all__"


def upload_model_form(request):
    """ 基于 ModelForm 上传文件和数据 """
    upload_title = "ModelForm上传文件"
    if request.method == "GET":
        form_a = UploadModelForm

        return render(request, 'upload_form.html', {'form_a': form_a, 'upload_title': upload_title})

    form_a = UploadModelForm(data=request.POST, files=request.FILES)
    if form_a.is_valid():
        # 这一句form_a.save()保存代码,对于文件的话会自动保存的
        # 字段 + 上传路径就写入到数据库.
        form_a.save()
        return HttpResponse("上传成功")

    return render(request, 'upload_form.html', {'form_a': form_a, 'upload_title': upload_title})



