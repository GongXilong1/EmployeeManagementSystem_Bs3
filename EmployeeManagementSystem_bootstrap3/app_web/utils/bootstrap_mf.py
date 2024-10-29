from django import forms


class BootStrapCommon:

    bootstrap_exclude_fields = []

    # 重新定义init方法
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 执行init父类的方法
        # 循环找到所有的插件,添加"class": "form-control"的样式
        for field_name, fields_a in self.fields.items():

            # 将bootstrap_exclude_fields中涉及的字段不设置BootStrap样式
            if field_name in self.bootstrap_exclude_fields:
                continue

            # 字段中有属性,保留原来的属性,如果没有属性,我们再给他增加属性
            if fields_a.widget.attrs:
                fields_a.widget.attrs["class"] = "form-control"
                fields_a.widget.attrs["placeholder"] = fields_a.label
            else:
                fields_a.widget.attrs = {
                    "class": "form-control",
                    "placeholder": fields_a.label
                }


class BootStrapModelForm(BootStrapCommon, forms.ModelForm):
    pass


class BootStrapForm(BootStrapCommon, forms.Form):
    pass


