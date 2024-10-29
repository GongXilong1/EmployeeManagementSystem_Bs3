""" 生成图片验证码函数 """


import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def captcha(width=120, height=30, char_length=5, font_file='./Monaco.ttf', font_size=28):
    code_a = []
    image_a = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw_a = ImageDraw.Draw(image_a, mode='RGB')

    def random_char():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))
        # return str(random.randint(0, 9))  # 生成随机数字

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








