# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
:author: 郑晓芬
:description: 结合LTP平台实现简单三元组抽取

"""
# coding: utf-8

import regex
import logging
import sys
import re
if sys.version_info[0] == 2:
    # reload(sys)
    sys.setdefaultencoding("utf8")

class Classify(object):
    def __init__(self, sentence,res_ie):
        self.logger = logging.getLogger("Classify")
        self.sentense = sentence
        self.res_ie = res_ie

    def SentenceType(self):
        result = "无"

        if re.search( r"？|如何 |怎么|什么|怎样|怎能|莫非|难不成|咋|何时|啥|是不是|是否|能不能|会不会|信不信|怕不怕|算不算|能否|可不可以|吗|有没有|对不对|呢|到底|多少|多大|难道|谁|哪儿|哪里|难道不",self.sentense, flags=0) != None:
            result = "疑问句"
        elif re.search(r"哎呦|呦|哎|天哪|啊|呀",self.sentense, flags=0 )!= None:
            result = "感叹句"
        elif re.match(r"麻烦|请|帮我|不准|不要|别|请勿|帮帮|不许",self.sentense, flags=0 )!= None or re.search(r"吧",self.res_ie, flags=0)!= None:
            result = "祈使句"
        elif re.search(r"主语",self.res_ie, flags=0)!= None:
            if re.search(r"谓语",self.res_ie, flags=0)!= None:
                result ="陈述句"
        else:
            result="未识别出来，期待补充！"


        return result

