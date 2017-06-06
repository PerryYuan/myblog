# -*- coding: utf-8 -*-
# @Author: xiaotuo
# @Date:   2016-10-29 22:18:38
# @Last Modified by:   Administrator
# @Last Modified time: 2016-11-21 20:08:31
import string
import random
# pip install Pillow
# Image:是一个画板(context),ImageDraw:是一个画笔, ImageFont:画笔的字体
from PIL import Image,ImageDraw,ImageFont
from django.core.cache import cache

# Captcha验证码

class Captcha(object):
    # 把一些常量抽取成类属性
    #字体的位置
    font_path = 'verdanab.ttf'
    #生成几位数的验证码
    number = 4
    #生成验证码图片的宽度和高度
    size = (100,30)
    #背景颜色，默认为白色 RGB(Re,Green,Blue)
    bgcolor = (255,255,255)
    #随机字体颜色
    # fontcolor = (random.randint(0,100),random.randint(0,100),random.randint(0,100))
    # 验证码字体大小
    fontsize = 25
    #随机干扰线颜色。
    # linecolor = (random.randint(0,200),random.randint(0,220),random.randint(0,255))
    # 是否要加入干扰线
    draw_line = True
    # 是否绘制干扰点
    draw_point = True
    # 加入干扰线的条数
    line_number = 2

    #用来绘制干扰线
    @classmethod
    def __gene_line(cls,draw,width,height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill = cls().get_color(200,220,255))

    # 用来绘制干扰点
    @classmethod
    def __gene_points(cls,draw,point_chance,width,height):
        chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]
        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))
    @classmethod
    def get_text(cls,num):
        sources = list(string.letters)
        [sources.append(str(x)) for x in xrange(0, 10)]
        return ''.join(random.sample(sources, num))

    #生成验证码
    @classmethod
    def gene_code(cls):
        width,height = cls.size #宽和高
        image = Image.new('RGBA',(width,height),cls.bgcolor) #创建图片
        font = ImageFont.truetype(cls.font_path,cls.fontsize) #验证码的字体
        draw = ImageDraw.Draw(image)  #创建画笔
        text = Captcha.get_text(cls.number) #生成字符串
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) / 2),text,font= font,fill=cls().get_color(100,100,100)) #填充字符串
        # 如果需要绘制干扰线
        if cls.draw_line:
            # 遍历line_number次,就是画line_number根线条
            for x in xrange(0,cls.line_number):
                cls.__gene_line(draw,width,height)
        # 如果需要绘制噪点
        if cls.draw_point:
            cls.__gene_points(draw,10,width,height)

        cache.set(text.lower(),text.lower(),120)
        return (text,image)


    @classmethod
    def check_captcha(cls,captcha):
        captcha_lower = captcha.lower()
        captcha_cache = cache.get(captcha_lower)
        if captcha_cache and captcha_cache == captcha_lower:
            cache.delete(captcha_lower)
            return True
        else:
            return False

    def get_color(self,range_r,range_g,range_b):
        return random.randint(0,range_r),random.randint(0,range_g),random.randint(0,range_b)
