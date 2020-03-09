# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:author: 郑晓芬
:description: 可视化ui

"""
import argparse
from ie import TripleIE
from classify import Classify
from cli import parse_args
import sys
import re
from untitled5 import Ui_Dialog
import jieba.posseg as pseg
from PyQt5.Qt import *

class Window(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def activity(self):
        self.output.setText("请稍等几秒钟......")
        sentence = self.input.text()
        print(self.input.text())
        args = parse_args()
        print("ok")
        IE = TripleIE(sentence, args.ltp, args.clean)
        out = IE.run()
        if re.search(r"句子结构不完整", out, flags=0) == None:
            CL = Classify(sentence,out)
            out += "句子类型：" + CL.SentenceType()
        self.output.setText(out)

app = QApplication(sys.argv)  # 建立application对象

first_window = Window()  # 建立窗体对象

first_window.show()  # 显示窗体

sys.exit(app.exec())  # 运行程序




