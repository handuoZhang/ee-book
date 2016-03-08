# -*- coding: utf-8 -*-
import re


class ParserTools(object):
    @staticmethod
    def match_content(patten, content, default=""):
        result = re.search(patten, str(content))
        if result is None:
            return default
        return result.group(0)

    @staticmethod
    def match_int(content):
        u"""
        返回文本形式的文字中的最长数字串, 若没有则返回'0'
        :param content:
        :return:
        """
        return ParserTools.match_content("\d+", content, "0")

    @staticmethod
    def get_tag_content(tag):
        u"""
        用于提取bs中tag.contents的内容
        需要对<br>进行预处理，将<br>换成<br/>,否则会爆栈，参考http://palydawn.blog.163.com/blog/static/1829690562012112285248753/
        """
        return "".join([unicode(x) for x in tag.contents])

    @staticmethod
    def get_attr(dom, attr, defaultValue=""):
        u"""
        获取bs中tag.content的指定属性
        若content为空或者没有指定属性则返回默认值
        """
        if dom is None:
            return defaultValue
        return dom.get(attr, defaultValue)
