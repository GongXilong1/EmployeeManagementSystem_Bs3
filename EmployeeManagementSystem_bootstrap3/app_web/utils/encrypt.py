""" 管理员密码 MD5加密方法 """

from django.conf import settings
import hashlib


def admin_pwd_md5(data_string):

    object_a = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))   # 加盐 settings.SECRET_KEY这个盐
    object_a.update(data_string.encode('utf-8'))
    return object_a.hexdigest()



