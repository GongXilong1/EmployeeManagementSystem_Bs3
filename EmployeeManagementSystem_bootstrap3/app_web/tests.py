""" 各种功能实验代码 区域 """

# class Example(object):
#
#     def __init__(self, name):
#         self.name = name
#
#     def __str__(self):
#         return self.name
#
#
# ojb_a = Example("IT部")
# print(ojb_a)  # 输出对象时,如果想要定制显示的内容. 在类中用__str__方法
#
#
# ojb_b = Example("销售部")
# print(ojb_b)




# from PIL import Image, ImageDraw, ImageFont
#
# # 生成一张图片到内存中
# image_a = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
#
# # 创建一个画笔
# draw_a = ImageDraw.Draw(image_a, mode='RGB')
#
# # 创建一个字体
# font_a = ImageFont.truetype("../Monaco.ttf", 28)
#
# draw_a.text([0, 0], 'python', "red", font=font_a)  # 画笔的开始坐标为00,内容是python,颜色是红色.
#
#
# # 保存到本地
# with open('code.png', 'wb') as f:  # 以open的方式打开一个code.png文件,以wb的方式写入,
#     image_a.save(f, format='png')  # 把image_a的内容写入到f这个文件中,以png的格式.
#
#


""" 生成验证码图片的代码 """


import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def captcha(width=120, height=30, char_length=5, font_file='../Monaco.ttf', font_size=28):
    code_a = []
    image_a = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw_a = ImageDraw.Draw(image_a, mode='RGB')

    def random_char():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def random_color():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 写文字
    font_a = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char_a = random_char()
        code_a.append(char_a)
        int_range = random.randint(0, 4)
        draw_a.text([i * width / char_length, int_range], char_a, font=font_a, fill=random_color())

    # 写干扰点
    for i in range(40):
        draw_a.point([random.randint(0, width), random.randint(0, height)], fill=random_color())

    # 写干扰圆圈
    for i in range(40):
        draw_a.point([random.randint(0, width), random.randint(0, height)], fill=random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_a.arc((x, y, x + 4, y + 4), 0, 90, fill=random_color())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw_a.line((x1, y1, x2, y2), fill=random_color())

    image_b = image_a.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return image_b, ''.join(code_a)


if __name__ == '__main__':
    # 1. 直接打开
    # img,code = check_code()
    # img.show()

    # 2. 写入文件
    # img,code = check_code()
    # with open('code.png','wb') as f:
    #     img.save(f,format='png')

    # 3. 写入内存(Python3)
    # from io import BytesIO
    # stream = BytesIO()
    # img.save(stream, 'png')
    # stream.getvalue()

    # 4. 写入内存（Python2）
    # import StringIO
    # stream = StringIO.StringIO()
    # img.save(stream, 'png')
    # stream.getvalue()

    img, captcha_str = captcha()
    print(captcha_str)

    # 保存在本地
    with open('code.png', 'wb') as f:
        img.save(f, format='png')


