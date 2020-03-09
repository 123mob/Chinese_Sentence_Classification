# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
:author: 郑晓芬
:description: 结合LTP平台实现简单三元组抽取

"""
# coding: utf-8
import os
import string
import logging
import sys

if sys.version_info[0] == 2:
    # reload(sys)
    sys.setdefaultencoding("utf8")

from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer




class TripleIE(object):
    def __init__(self, sentence, model_path, clean_output=False):
        self.logger = logging.getLogger("TripleIE")

        self.sentence = sentence
        self.model_path = model_path
        self.clean_output = clean_output  # 输出是否有提示

        self.out_handle = None

        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(self.model_path, "cws.model"))
        self.postagger = Postagger()
        self.postagger.load(os.path.join(self.model_path, "pos.model"))
        self.parser = Parser()
        self.parser.load(os.path.join(self.model_path, "parser.model"))
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(self.model_path, "ner.model"))

    def run(self):
        result = self.extract()
        self.logger.info("done with extracting...")
        return result

    def extract(self):
        # sentence="我是学生"
        result = ""
        words = self.segmentor.segment(self.sentence)
        postags = self.postagger.postag(words)
        ner = self.recognizer.recognize(words, postags)
        arcs = self.parser.parse(words, postags)

        sub_dicts = self._build_sub_dicts(words, postags, arcs)

        flay = ""
        sumt = 0
        # for idx in range(len(postags)):
        #     print(postags[idx])
        #     print(sub_dicts[idx])

        for idx in range(len(postags)):
            # if postags[idx] == 'v':
            # if 1:
            sub_dict = sub_dicts[idx]
                # 主谓宾定状补
            if 'SBV' in sub_dict:
                flay = True

                e1 = self._fill_ent(words, postags, sub_dicts, sub_dict['SBV'][0])
                c1=e1.replace(words[sub_dict['SBV'][0]],"")
                if c1 != '':
                    result += "主语的定语："+ c1 +"\n"
                    sumt +=1
                # print(words[sub_dict['SBV'][0]] )
                # subj  = words[sub_dict['SBV'][0]]
                r = words[idx]
                subj = self._fill_coo(words, postags, sub_dicts, sub_dict['SBV'][0])

                if self.clean_output:
                    result += "%s, %s\n" % (e1, r)
                else:
                    result += "主语："+subj +"\n"+"谓语："+r+"\n"
                    sumt += 2

            # if (flay != True):
            #     result = "句子结构不完整"
            #     return result

            if 'IOB' in sub_dict:
                result +="间接宾语：" + words[sub_dict['IOB'][0]] + "\n"
                sumt += 1
            # if 'RAD' in sub_dict:
            #     result += "右附加关系：" + words[sub_dict['RAD'][0]] + "\n"
            if 'FOB' in sub_dict:
                result +="后置宾语：" + words[sub_dict['COO'][0]] + "\n"
                sumt += 1
            if 'VOB' in sub_dict:
                e2 = self._fill_ent(words, postags, sub_dicts, sub_dict['VOB'][0])
                c2 = e2.replace(words[sub_dict['VOB'][0]], "")
                if c2 != '':
                    result += "宾语的定语：" + c2 + "\n"
                    sumt += 1
                obj = self._fill_coo(words, postags, sub_dicts, sub_dict['VOB'][0])
                result += "宾语："+obj+"\n"
                sumt += 1
            if 'ADV' in sub_dict:
                p=""
                for i in range(len(sub_dict['ADV'])):
                    p += words[sub_dict['ADV'][i]] +" "
                result += "状语："+p+"\n"
                sumt += 1
            if 'CMP' in sub_dict:
                result +="补语：" + words[sub_dict['CMP'][0]] + "\n"
                sumt += 1
            # if 'COO' in sub_dict:
            #     p = ""
            #     for i in range(len(sub_dict['COO'])):
            #         p += "、" + words[sub_dict['COO'][i]]
            #     subj += p + "\n"



            # 定语后置，动宾关系
            if arcs[idx].relation == 'ATT':
                if 'VOB' in sub_dict:
                    e1 = self._fill_ent(words, postags, sub_dicts, arcs[idx].head - 1)
                    r = words[idx]
                    e2 = self._fill_ent(words, postags, sub_dicts, sub_dict['VOB'][0])

                    temp_string = r + e2
                    if temp_string == e1[:len(temp_string)]:
                        e1 = e1[len(temp_string):]
                    if temp_string not in e1:
                        if self.clean_output:
                            self.out_handle.write("%s, %s, %s\n" % (e1, r, e2))
                            # print("%s, %s, %s\n" % (e1, r, e2))
                            result += "%s, %s, %s\n" % (e1, r, e2)
                        else:
                            # print("动宾定语后置\t(%s, %s, %s)\n" % (e1, r, e2))
                            result += "动宾定语后置\t(%s, %s, %s)\n" % (e1, r, e2)

        # print(flay)
        if (flay != True):

            result = "句子结构不完整"
        result += "\n结构个数："+ str(sumt)+"\n"

        return result
    """
    :decription: 为句子中的每个词语维护一个保存句法依存儿子节点的字典
    :args:
        words: 分词列表
        postags: 词性列表
        arcs: 句法依存列表
    """

    def _build_sub_dicts(self, words, postags, arcs):
        sub_dicts = []
        for idx in range(len(words)):
            sub_dict = dict()
            for arc_idx in range(len(arcs)):
                if arcs[arc_idx].head == idx + 1:
                    if arcs[arc_idx].relation in sub_dict:
                        sub_dict[arcs[arc_idx].relation].append(arc_idx)
                    else:
                        sub_dict[arcs[arc_idx].relation] = []
                        sub_dict[arcs[arc_idx].relation].append(arc_idx)
            sub_dicts.append(sub_dict)
        return sub_dicts

    """
    :decription:完善识别的部分实体
    """

    def _fill_ent(self, words, postags, sub_dicts, word_idx):
        sub_dict = sub_dicts[word_idx]
        prefix = ''

        if 'ATT' in sub_dict:
            for i in range(len(sub_dict['ATT'])):
                prefix += self._fill_ent(words, postags, sub_dicts, sub_dict['ATT'][i])
        postfix = ''
        if postags[word_idx] == 'v':
            if 'VOB' in sub_dict:
                postfix += self._fill_ent(words, postags, sub_dicts, sub_dict['VOB'][0])
            if 'SBV' in sub_dict:
                prefix = self._fill_ent(words, postags, sub_dicts, sub_dict['SBV'][0]) + prefix

        return prefix + words[word_idx] + postfix

    def _fill_coo(self, words, postags, sub_dicts, word_idx):
        sub_dict = sub_dicts[word_idx]
        prefix = ''
        if 'COO' in sub_dict:
            for i in range(len(sub_dict['COO'])):
                prefix += self._fill_ent(words, postags, sub_dicts, sub_dict['COO'][i])+ " "

        return prefix + words[word_idx]
        # print("words[word_idx]="+words[word_idx])
        # print("prefix="+prefix)
        # return prefix+words[word_idx]
