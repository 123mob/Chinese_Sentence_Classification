# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
:author: 郑晓芬
:description: 结合LTP平台实现简单三元组抽取相关参数设置

"""


import argparse
from ie import TripleIE
from classify import Classify
def parse_args():
    parser = argparse.ArgumentParser('TripleIE')

    parser.add_argument('--ltp', type=str, default='E:\python\ltp_data_v3.4.0',
                            help='the path to LTP model')
    parser.add_argument('--clean', action='store_true',
                            help='output the clean relation(no tips)')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # sentence = "国务院总理李克强积极地快乐地调研美丽的上海"
    sentence = "什么时候放假呢"

    IE = TripleIE(sentence,args.ltp, args.clean)
    result = IE.run()
    if result !="句子结构不完整":
        CL = Classify(sentence,result)
        result += "句子类型："+CL.SentenceType()

    print(result)
